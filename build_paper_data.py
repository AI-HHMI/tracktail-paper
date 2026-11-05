#!/usr/bin/env python
"""Build the derived data of the paper's figures and the sparse result copy in data/.

Steps:

    collect    copy the small summary files (summary.json, metrics.md, combined_*metrics.csv, ...) of every paper run
               from the result trees into data/results/. Needs the real result trees (TRACKTAIL_OUTPUTS, ... set to
               them, see paths.py); skipped for a tree that already is the data/results copy.
    ncam       data/dexycb_ncam_results.csv: DexYCB AJ vs number of views (Fig. n_cams), from the ncam_ablation_summary
               .csv of each method. Runs from data/results.
    survival   data/survival_curves.csv: survival rate per frame on MV Point Odyssey (Figs. po_survival_*), computed
               from the per-trial prediction files. Needs the full result trees and TRACKTAIL_DATA (for the CoTracker runs).

    python build_paper_data.py collect ncam survival     # full path (Janelia result trees or your own reruns)
    python build_paper_data.py ncam                       # quick path, from data/results

Without the full result trees only `ncam` can run; the committed data/survival_curves.csv is then used as is.
"""
import argparse
import glob
import os
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

# ---------------------------------------------------------------------------------------------------------------------
# collect

# result tree -> runs used in the paper (folders below the tree). Only small text files are copied.
PAPER_RUNS = {
    'TRACKTAIL_OUTPUTS': [
        'main_finetune_vzkjqrys_canonical_cached',          # Tab. main_results
        'main_finetune_vzkjqrys_po_4cams',                  # Tab. po_results, Fig. survival
        'main_finetune_vzkjqrys_po_9cams',
        'main_pretrain_e25w9v86_canonical_cached',          # ablation tables (Large / both attn / 512)
        'ablation_cam_self_attn_folhop3e_canonical_cached',
        'ablation_temporal_self_attn_b3de55ap_canonical_cached',
        'ablation_cam_temporal_self_attn_cnmw9dcf_canonical_cached',
        'ablation_encoder_size_base_hv8nguwx_canonical_cached',
        'ablation_encoder_size_giant_ubk4lvez_canonical_cached',
        'ablation_encoder_size_gigantic_u1c34ou7_canonical_cached',
        'ablation_latent_dim_256_lczwsdx3_canonical_cached',
        'ablation_latent_dim_1024_wk2i4o1u_canonical_cached',
        'ncam_ablation_dexycb',                             # Fig. n_cams
        'main_finetune_vzkjqrys_tapvid3d_official_minival_vis0.1_occunk',   # Tab. tapvid3D_results
    ],
    'COTRACKER_OUTPUTS': ['paper-canonical-cached', 'paper-po-4cams', 'paper-po-9cams', 'ncam-ablation-dexycb'],
    'MVTRACKER_OUTPUTS': ['paper-canonical-cached-duster', 'paper-canonical-cached-gt',
                          'paper-po-4cams-duster_0.5', 'paper-po-4cams-gt_0.5',
                          'paper-po-9cams-duster_0.5', 'paper-po-9cams-gt_0.5', 'ncam-ablation-dexycb'],
    'MVTRACKER_SENSORDEPTH_OUTPUTS': ['paper-canonical-cached-sensor-linear'],
    'ARROW_OUTPUTS': ['paper-canonical-cached', 'paper-po-4cams', 'ncam-ablation-dexycb'],
}
# folder of each tree in data/results (= the defaults in paths.py)
TREE_NAMES = {'TRACKTAIL_OUTPUTS': 'tracktail-outputs', 'COTRACKER_OUTPUTS': 'cotracker-outputs',
              'MVTRACKER_OUTPUTS': 'mvtracker-outputs',
              'MVTRACKER_SENSORDEPTH_OUTPUTS': 'mvtracker-outputs-dexycb-sensordepth', 'ARROW_OUTPUTS': 'arrow-outputs'}
SUMMARY_SUFFIXES = ('.json', '.md', '.csv')
MAX_FILE_BYTES = 2_000_000


def _copy_run(src, dst):
    n = 0
    for root, _, files in os.walk(src):
        for name in files:
            p = Path(root) / name
            if p.suffix in SUMMARY_SUFFIXES and p.stat().st_size <= MAX_FILE_BYTES:
                out = dst / p.relative_to(src)
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, out)
                n += 1
    return n


def collect():
    dest_root = paths.REPO / 'data' / 'results'
    jobs = [(getattr(paths, var), run, dest_root / TREE_NAMES[var] / run)
            for var, runs in PAPER_RUNS.items() for run in runs]
    po9 = Path(paths.ARROW_PO9_OUTPUTS)
    jobs.append((po9.parent, po9.name, dest_root / 'arrow-outputs' / 'paper-po-9cams'))
    for tree, run, dst in jobs:
        src = Path(tree) / run
        if src.resolve() == dst.resolve():
            print(f'[collect] {dst.relative_to(paths.REPO)} is the data/ copy itself, skipped')
            continue
        if not src.exists():
            print(f'[collect] missing {src}, skipped')
            continue
        print(f'[collect] {src} -> {dst.relative_to(paths.REPO)}: {_copy_run(src, dst)} files')


# ---------------------------------------------------------------------------------------------------------------------
# ncam

def ncam():
    """DexYCB AJ (%) per number of views for each method, one column per method."""
    sources = {   # column: (summary csv, AJ column)
        'CoTracker3 Baseline': (paths.COTRACKER_OUTPUTS / 'ncam-ablation-dexycb', 'cotracker_avg_jaccard'),
        'MVTracker Baseline': (paths.MVTRACKER_OUTPUTS / 'ncam-ablation-dexycb', 'mvtracker_avg_jaccard'),
        'Tracktail': (paths.TRACKTAIL_OUTPUTS / 'ncam_ablation_dexycb', 'avg_jaccard'),
        'ARROW': (paths.ARROW_OUTPUTS / 'ncam-ablation-dexycb', 'arrow_avg_jaccard'),
    }
    cols = []
    for name, (folder, col) in sources.items():
        df = pd.read_csv(paths.result(folder / 'ncam_ablation_summary.csv'))
        cols.append(pd.Series(np.round(df[col].to_numpy() * 100, 1), index=df['n_views'], name=name))
    out = pd.concat(cols, axis=1, sort=True)
    out.index.name = 'n_views'
    path = paths.PAPER_DATA / 'dexycb_ncam_results.csv'
    out.to_csv(path)
    print(out.to_string())
    print(f'[ncam] wrote {path}')


# ---------------------------------------------------------------------------------------------------------------------
# survival (same computation as scripts/compute_survival.py of the Tracktail code)

THRESHOLDS = [0.30, 0.60, 1.20, 2.40, 4.80, 15.00]   # failure distances, Point Odyssey scene units
PO_DATASETS = {   # name in the output: (dataset folder, trial prefix)
    'human': ('point-odyssey-human', 'hum'),
    'animal': ('po-animal-sub256-motion', 'ani'),
}


def survival_configs(cams=(4, 9)):
    configs = []
    for n in cams:
        arrow_run = paths.ARROW_OUTPUTS / 'paper-po-4cams' if n == 4 else Path(paths.ARROW_PO9_OUTPUTS)
        for dataset, (folder, prefix) in PO_DATASETS.items():
            configs.append(dict(model=f'tracktail-{n}cams', dataset=dataset, pattern=str(
                paths.TRACKTAIL_OUTPUTS / f'main_finetune_vzkjqrys_po_{n}cams' / folder / f'{prefix}*_trial.npz')))
            configs.append(dict(model=f'cotracker-{n}cams', dataset=dataset, cotracker=True, pattern=str(
                paths.COTRACKER_OUTPUTS / f'paper-po-{n}cams' / folder / 'test' / f'{prefix}*' / 'trial' /
                'cotracker_3d.npz')))
            for depth in ('gt', 'duster'):
                configs.append(dict(model=f'mvtracker-{n}cams-{depth}', dataset=dataset, pattern=str(
                    paths.MVTRACKER_OUTPUTS / f'paper-po-{n}cams-{depth}' / folder / f'{prefix}*_trial.npz')))
            configs.append(dict(model=f'arrow-{n}cams', dataset=dataset,
                                pattern=str(arrow_run / folder / f'{prefix}*_trial.npz')))
    return configs


def _cam_indices(metadata_path, cam_names):
    with open(metadata_path) as f:
        names = list(yaml.safe_load(f)['intrinsic_matrices'].keys())
    names = sorted(names, key=int) if all(n.isdigit() for n in names) else sorted(names)
    return [names.index(n) for n in cam_names]


def load_trial(path, cotracker=False, pose_file='pose3d.npz'):
    """(coords_pred (T,N,3), coords_true (T,N,3), vis_true (T,N) bool, query_times (N,)) of a prediction file.

    vis_true is restricted to the cameras that were used: from vis_true_cams in Tracktail/MVTracker/ARROW files, and
    rebuilt from the trial's pose file (under TRACKTAIL_DATA) for CoTracker files.
    """
    d = np.load(path, allow_pickle=True)
    coords_pred = np.asarray(d['coords_pred']).squeeze(0)
    coords_true = np.asarray(d['coords_true']).squeeze(0)
    vis_true = np.asarray(d['vis_true']).squeeze((0, -1)).astype(bool)
    if 'vis_true_cams' in d.files:
        vtc = np.asarray(d['vis_true_cams']).squeeze(0).astype(np.float64)
        vis_true = (np.isfinite(vtc) & (vtc > 0.5)).any(axis=-1)
    elif cotracker and 'cam_names' in d.files:
        data_root = paths.require(paths.TRACKTAIL_DATA, 'TRACKTAIL_DATA')
        trial_dir = os.path.dirname(path)                                   # .../<dataset>/test/<session>/trial
        pose_dir = os.path.join(data_root, *trial_dir.split(os.sep)[-4:])
        vis_all = np.load(os.path.join(pose_dir, pose_file))['vis'][0]      # (T_full, N_full, C)
        idx = _cam_indices(os.path.join(pose_dir, 'metadata.yaml'), [str(c) for c in d['cam_names']])
        vis_true = vis_all[..., idx].any(-1)[d['frame_numbers']][:, d['valid_mask']]
    if 'query_times' in d.files:
        query_times = np.asarray(d['query_times']).astype(np.int32)
    else:
        query_times = np.zeros(coords_pred.shape[1], dtype=np.int32)
    return coords_pred, coords_true, vis_true, query_times


def survival_rate_per_frame(coords_pred, coords_true, vis_true, query_times, threshold):
    """Fraction of tracks that have not failed by each frame.

    A track fails at the first frame at or after its query frame where it is visible, the GT is finite and the
    prediction is more than `threshold` from the GT. Frames without a prediction (nan) are ignored. Tracks without any
    such scored frame are left out.
    """
    T, N = vis_true.shape
    dist = np.linalg.norm(coords_pred - coords_true, axis=-1)
    gt_finite = np.isfinite(coords_true).all(axis=-1)
    failure_frames = []
    for n in range(N):
        qt = int(query_times[n])
        active = vis_true[qt:, n] & gt_finite[qt:, n]
        if not np.any(active):
            continue
        failed = np.where((dist[qt:, n] > threshold) & active)[0]
        failure_frames.append(int(failed[0]) + qt if len(failed) else T)
    if not failure_frames:
        return np.full(T, np.nan)
    fa = np.array(failure_frames)
    return np.array([np.mean(fa > t) for t in range(T)])


def survival_rows(cfg, thresholds):
    paths_ = sorted(glob.glob(cfg['pattern']))
    if not paths_:
        print(f"  WARNING: no files for {cfg['model']} / {cfg['dataset']}: {cfg['pattern']}")
        return []
    trials = [load_trial(p, cotracker=cfg.get('cotracker', False)) for p in paths_]
    rows = []
    for thr in thresholds:
        curves = [survival_rate_per_frame(*t, thr) for t in trials]
        T = min(len(c) for c in curves)
        curves = np.stack([c[:T] for c in curves])
        mean, std = np.nanmean(curves, 0), np.nanstd(curves, 0)
        rows += [dict(model=cfg['model'], dataset=cfg['dataset'], frame=t, survival_mean=float(mean[t]),
                      survival_std=float(std[t]), n_trials=len(curves), threshold=thr) for t in range(T)]
    print(f"  {cfg['model']:24s} {cfg['dataset']:7s} {len(paths_):3d} trials")
    return rows


def survival():
    rows = []
    for cfg in survival_configs():
        rows += survival_rows(cfg, THRESHOLDS)
    df = pd.DataFrame(rows)
    path = paths.PAPER_DATA / 'survival_curves.csv'
    df.to_csv(path, index=False)
    print(f'[survival] wrote {len(df)} rows to {path}')


STEPS = {'collect': collect, 'ncam': ncam, 'survival': survival}

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('steps', nargs='+', metavar='STEP', help=' | '.join(STEPS))
    args = ap.parse_args()
    for step in args.steps:
        if step not in STEPS:
            ap.error(f'unknown step {step!r}; choose from {list(STEPS)}')
    for step in args.steps:
        STEPS[step]()
