"""Why does the CoTracker baseline lose points? Fractions of (track, frame) pairs without a triangulated position.

CoTracker tracks each camera in 2D and triangulates the cameras that mark the point visible. A frame with fewer than 2
such cameras has no 3D position (nan). That happens for two different reasons, which this separates with the ground-truth
visibility of the cameras that were used:

    visible enough      the point is visible in at least 2 of the cameras in the ground truth, so a position could have
                        been triangulated, but CoTracker marked fewer than 2 of them visible
    not visible enough  the point is visible in fewer than 2 cameras (1 or 0) in the ground truth: no 3D position can be
                        expected (split into exactly 1 camera and 0 cameras, the latter is not scored by the metrics)

Only the frames after each track's query frame are counted, as in the metrics. Counts are pooled over all trials.

Two files are written, with one row per run:
    cotracker_triangulation_stats.csv         pct_pairs_failed, the share of all (track, frame) pairs without a position,
                                              and the split of those failures into the two reasons, which add to 100:
                                              pct_of_failures_not_visible_enough + pct_of_failures_visible_enough
    cotracker_triangulation_stats_detail.csv  everything else (rates within each group, the 1 and 0 camera parts, counts)

The runs are those of cotracker_cached.sh (canonical cameras of the MVTracker tables) and cotracker_cached_po.sh (Point
Odyssey, 4 and 9 cameras). Run it with any python that has numpy, pandas and pyyaml:

    python cotracker_triangulation_stats.py [--out data/v2/cotracker_triangulation_stats.csv]
"""
import argparse
import glob
import os

import numpy as np
import pandas as pd
import yaml

RESULTS = '/groups/karashchuk/home/ruppk2/results/paper-final-v2/cotracker-outputs'
DATASET_ROOT = '/groups/karashchuk/karashchuklab/animal-datasets-processed/posetail-pretraining-v6'

# label, folder of the run, dataset folder, pose file the run was made with
RUNS = [
    ('kubric-multiview',        'paper-canonical-cached', 'kubric-multiview',        'pose3d_cached.npz', '4 (canonical)'),
    ('dex_ycb',                 'paper-canonical-cached', 'dex_ycb',                 'pose3d_cached.npz', '4 (canonical)'),
    ('cmupanoptic_3dgs',        'paper-canonical-cached', 'cmupanoptic_3dgs',        'pose3d_cached.npz', '4 (canonical)'),
    ('point-odyssey-human',     'paper-po-4cams',         'point-odyssey-human',     'pose3d.npz',        '4'),
    ('point-odyssey-human',     'paper-po-9cams',         'point-odyssey-human',     'pose3d.npz',        '9'),
    ('po-animal-sub256-motion', 'paper-po-4cams',         'po-animal-sub256-motion', 'pose3d.npz',        '4'),
    ('po-animal-sub256-motion', 'paper-po-9cams',         'po-animal-sub256-motion', 'pose3d.npz',        '9'),
]


def camera_indices(metadata_path, cam_names):
    """Positions of cam_names among the cameras of metadata.yaml, the columns of vis in the pose file."""
    with open(metadata_path) as f:
        names = list(yaml.safe_load(f)['intrinsic_matrices'].keys())
    names = sorted(names, key=int) if all(n.isdigit() for n in names) else sorted(names)
    return [names.index(str(c)) for c in cam_names]


def trial_counts(path, pose_file):
    """Counts of scored (track, frame) pairs by the number of cameras that see the point, and how many have no position."""
    d = np.load(path)
    coords = d['coords_3d']                                                   # (T, N, 3)
    T, N, _ = coords.shape
    qt = d['query_times'] if 'query_times' in d.files else np.zeros(N, dtype=int)

    ds, _, session, _ = path.split(os.sep)[-5:-1]
    trial_dir = os.path.join(DATASET_ROOT, ds, 'test', session, 'trial')
    vis = np.load(os.path.join(trial_dir, pose_file))['vis'][0]               # (T_full, N_full, C)
    idx = camera_indices(os.path.join(trial_dir, 'metadata.yaml'), d['cam_names'])
    n_seen = vis[d['frame_numbers']][:, d['valid_mask']][..., idx].sum(-1)    # (T, N) cameras that see the point

    scored = np.arange(T)[:, None] > qt[None, :]
    failed = ~np.isfinite(coords).all(-1)
    out = {}
    for name, sel in (('0', n_seen == 0), ('1', n_seen == 1), ('2plus', n_seen >= 2)):
        out[f'n_{name}'] = int((sel & scored).sum())
        out[f'failed_{name}'] = int((sel & scored & failed).sum())
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--results', default=RESULTS)
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  'data', 'v2', 'cotracker_triangulation_stats.csv'))
    args = ap.parse_args()

    rows, details = [], []
    for label, folder, ds, pose_file, cams in RUNS:
        files = sorted(glob.glob(os.path.join(args.results, folder, ds, 'test', '*', '*', 'cotracker_3d.npz')))
        if not files:
            print(f'[skip] no outputs for {label} in {folder}')
            continue
        tot = {}
        for f in files:
            for k, v in trial_counts(f, pose_file).items():
                tot[k] = tot.get(k, 0) + v
        n = {k: tot[f'n_{k}'] for k in ('0', '1', '2plus')}
        fl = {k: tot[f'failed_{k}'] for k in ('0', '1', '2plus')}
        n_all, f_all = sum(n.values()), sum(fl.values())
        n_lt2, f_lt2 = n['0'] + n['1'], fl['0'] + fl['1']
        frac = lambda a, b: a / b if b else float('nan')
        detail = {
            'dataset': label,
            'cameras': cams,
            'n_trials': len(files),
            'n_pairs': n_all,
            'frac_pairs_failed': frac(f_all, n_all),
            # 1. visible in enough cameras (at least 2) in the ground truth
            'frac_pairs_visible_enough': frac(n['2plus'], n_all),
            'frac_failed_when_visible_enough': frac(fl['2plus'], n['2plus']),
            # 2. not visible in enough cameras (fewer than 2), and its two parts
            'frac_pairs_not_visible_enough': frac(n_lt2, n_all),
            'frac_failed_when_not_visible_enough': frac(f_lt2, n_lt2),
            'frac_failed_when_visible_in_1_camera': frac(fl['1'], n['1']),
            'frac_failed_when_visible_in_0_cameras': frac(fl['0'], n['0']),
            'n_pairs_visible_enough': n['2plus'], 'n_failed_visible_enough': fl['2plus'],
            'n_pairs_not_visible_enough': n_lt2, 'n_failed_not_visible_enough': f_lt2,
            'n_pairs_visible_in_1_camera': n['1'], 'n_failed_visible_in_1_camera': fl['1'],
            'n_pairs_visible_in_0_cameras': n['0'], 'n_failed_visible_in_0_cameras': fl['0'],
        }
        details.append(detail)
        rows.append({
            'dataset': label,
            'cameras': cams,
            'n_trials': len(files),
            'n_pairs': n_all,
            'n_pairs_failed': f_all,
            'pct_pairs_failed': 100 * frac(f_all, n_all),
            # of the failed pairs (these two add to 100)
            'pct_of_failures_not_visible_enough': 100 * frac(f_lt2, f_all),
            'pct_of_failures_visible_enough': 100 * frac(fl['2plus'], f_all),
        })
        print(f'{label:26s} {cams:14s} {len(files):3d} trials  {n_all:>9d} pairs')

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df.to_csv(args.out, index=False)
    detail_out = args.out.replace('.csv', '_detail.csv')
    pd.DataFrame(details).to_csv(detail_out, index=False)
    print(f'saved {len(df)} rows to {args.out} and the detail to {detail_out}')


if __name__ == '__main__':
    main()
