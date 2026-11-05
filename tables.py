#!/usr/bin/env python
"""Write the LaTeX tabulars of the paper's result tables into tables/, from the result summaries.

    python tables.py                          # reads data/results (or TRACKTAIL_RESULTS / the variables in paths.py)
    python tables.py --check ../tracktail-overleaf   # also compare every number and bold/underline mark with the
                                                     # tables in sec/4_experiments.tex and sec/7_suppl.tex

One file per table, named after its LaTeX label: main_results, po_results, ablation_camattn, ablation_encoder,
ablation_latent, cotracker_triangulation, tapvid3D_results. Each holds the `tabular` (header and rows); the
`table` environment and caption stay in the paper. Bold = best, underline = second best (distinct rounded values,
ties share the mark), as in the paper. Rows taken from other papers are constants below (LITERATURE_*).

Units (as in the paper): AJ, delta_avg and OA in %; MTE in cm on Panoptic Studio and DexYCB (results are in m),
times 13 on Multi-view Kubric (the MVTracker paper's unit), Point Odyssey scene units on Point Odyssey.
TAPVid-3D: fractions, 3 decimals.
"""
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

METRICS = ['avg_jaccard', 'delta_x_avg', 'occlusion_acc', 'mte']   # AJ, delta_avg, OA, MTE
HIGHER = [True, True, True, False]
MTE_SCALE = {'cmupanoptic_3dgs': 100, 'dex_ycb': 100, 'kubric-multiview': 13,
             'point-odyssey-human': 1, 'po-animal-sub256-motion': 1}
MAIN_DATASETS = ['cmupanoptic_3dgs', 'dex_ycb', 'kubric-multiview']
PO_DATASETS = ['point-odyssey-human', 'po-animal-sub256-motion']


def to_units(values, dataset):
    """[AJ, delta_avg, OA, MTE] fractions / world units -> table units."""
    return [v * 100 for v in values[:3]] + [values[3] * MTE_SCALE[dataset]]


def tracktail(run, dataset):
    """Tracktail metrics (mean over trials) from summary.json of scripts/eval_testset_metrics.py (Tracktail code)."""
    s = json.load(open(paths.TRACKTAIL_OUTPUTS / run / 'summary.json'))[dataset]
    return to_units([s[f'{m}_mean'] for m in METRICS], dataset)


def baseline(run_dir, prefix, dataset):
    """Baseline metrics (mean over trials) from combined_summary_metrics.csv of mvtracker_baseline/mvtracker_metrics.py (Tracktail code)."""
    df = pd.read_csv(run_dir / 'combined_summary_metrics.csv').set_index('dataset')
    return to_units([df.loc[dataset, f'{prefix}_{m}'] for m in METRICS], dataset)


# ---------------------------------------------------------------------------------------------------------------------
# formatting

class Cell:
    """A number with its formatting: decimals, optional suffix (e.g. a dagger), excluded from ranking or not."""

    def __init__(self, value, decimals=1, suffix='', rank=True):
        self.value, self.decimals, self.suffix, self.rank = value, decimals, suffix, rank
        self.mark = ''

    @property
    def rounded(self):
        return round(float(self.value), self.decimals)

    def tex(self):
        s = f'{self.value:.{self.decimals}f}'
        if self.mark == 'bold':
            s = rf'\textbf{{{s}}}'
        elif self.mark == 'underline':
            s = rf'\underline{{{s}}}'
        return s + self.suffix


def cells(values, **kw):
    return [Cell(v, **kw) for v in values]


def mark_best(rows, higher, underline=True):
    """Bold the best and underline the second best distinct rounded value of every column (in place)."""
    for j, hi in enumerate(higher):
        col = [r[j] for r in rows if r is not None and r[j] is not None and r[j].rank]
        vals = sorted({c.rounded for c in col}, reverse=hi)
        for c in col:
            if c.rounded == vals[0]:
                c.mark = 'bold'
            elif underline and len(vals) > 1 and c.rounded == vals[1]:
                c.mark = 'underline'


def row_tex(label, row_cells, gray=False):
    line = ' & '.join([label] + [c.tex() for c in row_cells]) + r' \\'
    return (r'\rowcolor{rowgray}' + '\n' if gray else '') + line


def write(name, text):
    paths.TABLE_OUT.mkdir(parents=True, exist_ok=True)
    path = paths.TABLE_OUT / f'{name}.tex'
    path.write_text(text.strip() + '\n')
    print(f'wrote {path}')


HEADER4 = r'AJ$\uparrow$ & $\delta_\text{avg}\uparrow$ & OA$\uparrow$ & MTE$\downarrow$'

# ---------------------------------------------------------------------------------------------------------------------
# Tab. main_results

# rows copied from the MVTracker paper (Rajic et al. 2025, Tab. 1): Panoptic | DexYCB | Kubric, AJ dAvg OA MTE
LITERATURE_MAIN = [
    (r'Dynamic 3DGS~\cite{luiten2023dynamic}', r'$\times$', r'\xmark',
     [66.5, 92.4, 74.1, 3.9, 45.7, 57.1, 81.3, 11.3, 30.4, 48.6, 68.3, 11.2]),
    (r'Shape of Motion~\cite{som2024}', r'$\times$', r'\cmark',
     [72.6, 89.2, 82.1, 4.8, 36.2, 53.6, 63.3, 8.0, 57.8, 63.4, 86.2, 5.3]),
    (r'CoTracker3~\cite{karaev24cotracker3}', 'Kub+15k', r'\cmark',
     [74.5, 84.5, 86.4, 8.6, 29.4, 40.3, 78.6, 22.0, 55.1, 60.6, 77.7, 11.9]),
    (r'SpaTrackerV2~\cite{xiao2025spatialtrackerv2}', r'See~\cite{xiao2025spatialtrackerv2}', r'\cmark',
     [75.3, 85.1, 91.2, 6.9, 35.5, 45.1, 91.3, 9.8, 58.6, 69.3, 86.3, 3.9]),
    (r'TAPIP3D~\cite{tapip3d}', 'Kub', r'\cmark',
     [84.3, 93.8, 91.4, 3.1, 38.8, 50.0, 90.1, 8.2, 72.4, 86.5, 85.4, 1.3]),
]


def main_results():
    cot, mvt, arrow = paths.COTRACKER_OUTPUTS, paths.MVTRACKER_OUTPUTS, paths.ARROW_OUTPUTS
    ours = [
        (r'MVTracker (DUSt3R depth)~\cite{rajic2025mvtracker}', 'MV-Kub', r'\cmark',
         cells(sum((baseline(mvt / 'paper-canonical-cached-duster', 'mvtracker', d) for d in MAIN_DATASETS), []))),
        # GT depth on Panoptic and Kubric; DexYCB has no GT depth: Kinect sensor depth (dagger)
        (r'MVTracker (GT Depth) ~\cite{rajic2025mvtracker}', 'MV-Kub', r'\cmark',
         cells(baseline(mvt / 'paper-canonical-cached-gt', 'mvtracker', 'cmupanoptic_3dgs'))
         + cells(baseline(paths.MVTRACKER_SENSORDEPTH_OUTPUTS / 'paper-canonical-cached-sensor-linear',
                          'mvtracker', 'dex_ycb'), suffix=r'$^\dagger$')
         + cells(baseline(mvt / 'paper-canonical-cached-gt', 'mvtracker', 'kubric-multiview'))),
        ('CoTracker3 Baseline', 'Kub+15k', r'\xmark',
         cells(sum((baseline(cot / 'paper-canonical-cached', 'cotracker', d) for d in MAIN_DATASETS), []))),
        (r'ARROW~\cite{fradlin2026arrow}', r'See~\cite{fradlin2026arrow}', r'\xmark',
         cells(sum((baseline(arrow / 'paper-canonical-cached', 'arrow', d) for d in MAIN_DATASETS), []))),
        ('Tracktail (Ours)', 'MV-Kub+MV-PO', r'\xmark',
         cells(sum((tracktail('main_finetune_vzkjqrys_canonical_cached', d) for d in MAIN_DATASETS), []))),
    ]
    lit = [(n, t, d, cells(v)) for n, t, d, v in LITERATURE_MAIN]
    rows = lit + ours
    mark_best([r[3] for r in rows], HIGHER * 3)
    fmt = lambda i, gray: row_tex(f'{rows[i][0]} & {rows[i][1]} & {rows[i][2]}', rows[i][3], gray)
    body = '\n'.join([
        fmt(0, True), fmt(1, False), r'\midrule',
        fmt(2, True), fmt(3, False), fmt(4, True), fmt(5, False), fmt(6, True), r'\midrule',
        fmt(7, False), fmt(8, True), fmt(9, False)])
    write('main_results', rf"""
\begin{{tabular}}{{lll cccc cccc cccc}}
\toprule
\multirow{{2}}{{*}}{{Method}} & \multirow{{2}}{{*}}{{Train}} & \multirow{{2}}{{*}}{{Depth}}
  & \multicolumn{{4}}{{c}}{{Panoptic Studio~\cite{{joo2015panoptic}}}}
  & \multicolumn{{4}}{{c}}{{DexYCB~\cite{{chao2021dexycb}}}}
  & \multicolumn{{4}}{{c}}{{Multi-View Kubric~\cite{{rajic2025mvtracker}}}} \\
\cmidrule(lr){{4-7}}\cmidrule(lr){{8-11}}\cmidrule(lr){{12-15}}
  & & & {HEADER4}
      & {HEADER4}
      & {HEADER4} \\
\midrule
{body}
\bottomrule
\end{{tabular}}""")


# ---------------------------------------------------------------------------------------------------------------------
# Tab. po_results

def po_results():
    cot, mvt, arrow = paths.COTRACKER_OUTPUTS, paths.MVTRACKER_OUTPUTS, paths.ARROW_OUTPUTS

    def both(run4, run9, prefix):
        return cells([v for run in (run4, run9) for d in PO_DATASETS for v in
                      (tracktail(run, d) if prefix is None else baseline(run, prefix, d))])

    rows = [
        (r'CoTracker3 Baseline~\cite{karaev24cotracker3}', both(cot / 'paper-po-4cams', cot / 'paper-po-9cams', 'cotracker')),
        # MVTracker on Point Odyssey with visibility threshold 0.5 (mvtracker_cached_po.sh VIS_THRESHOLD=0.5)
        (r'MVTracker~\cite{rajic2025mvtracker} (DUSt3R depth)',
         both(mvt / 'paper-po-4cams-duster_0.5', mvt / 'paper-po-9cams-duster_0.5', 'mvtracker')),
        (r'MVTracker~\cite{rajic2025mvtracker} (GT depth)',
         both(mvt / 'paper-po-4cams-gt_0.5', mvt / 'paper-po-9cams-gt_0.5', 'mvtracker')),
        # 9 views: paths.ARROW_PO9_OUTPUTS (the rerun with 24-frame windows, arrow-outputs-w24)
        (r'ARROW~\cite{fradlin2026arrow}', both(arrow / 'paper-po-4cams', paths.ARROW_PO9_OUTPUTS, 'arrow')),
        ('Tracktail (Ours)', both('main_finetune_vzkjqrys_po_4cams', 'main_finetune_vzkjqrys_po_9cams', None)),
    ]
    mark_best([r[1] for r in rows], HIGHER * 4)
    body = '\n'.join(row_tex(f'{name}\n ', c, gray=(i % 2 == 0)) for i, (name, c) in enumerate(rows))
    write('po_results', rf"""
\begin{{tabular}}{{l cccc cccc cccc cccc}}
\toprule
\multirow{{3}}{{*}}{{Method}}
  & \multicolumn{{8}}{{c}}{{4 Camera Views}}
  & \multicolumn{{8}}{{c}}{{9 Camera Views (all)}} \\
\cmidrule(lr){{2-9}}\cmidrule(lr){{10-17}}
  & \multicolumn{{4}}{{c}}{{Human}}
  & \multicolumn{{4}}{{c}}{{Animal}}
  & \multicolumn{{4}}{{c}}{{Human}}
  & \multicolumn{{4}}{{c}}{{Animal}} \\
\cmidrule(lr){{2-5}}\cmidrule(lr){{6-9}}\cmidrule(lr){{10-13}}\cmidrule(lr){{14-17}}
  & {HEADER4}
  & {HEADER4}
  & {HEADER4}
  & {HEADER4} \\
\midrule
{body}
\bottomrule
\end{{tabular}}""")


# ---------------------------------------------------------------------------------------------------------------------
# ablations (Multi-view Kubric, pretraining stage only)

PRETRAIN = 'main_pretrain_e25w9v86_canonical_cached'   # Large encoder, both attentions, latent 512


def kubric(run):
    return cells(tracktail(run, 'kubric-multiview'))


def ablation_table(name, first_col_spec, header_cols, rows, label_cols):
    mark_best([r[1] for r in rows], HIGHER, underline=False)
    body = '\n'.join(row_tex(label, c, gray=(i % 2 == gray0)) for i, (label, c) in enumerate(rows)
                     for gray0 in [ABLATION_GRAY_START[name]])
    write(name, rf"""
\begin{{tabular}}{{{first_col_spec} cccc}}
\toprule
{header_cols}
  & \multicolumn{{4}}{{c}}{{Multi-View Kubric~\cite{{rajic2025mvtracker}}}} \\
\cmidrule(lr){{{label_cols + 1}-{label_cols + 4}}}
  {'& ' * label_cols}{HEADER4} \\
\midrule
{body}
\bottomrule
\end{{tabular}}""")


# row index parity that gets \rowcolor{rowgray} (as in the paper)
ABLATION_GRAY_START = {'ablation_camattn': 1, 'ablation_encoder': 0, 'ablation_latent': 0}


def ablation_camattn():
    rows = [
        (r'\cmark & \cmark', kubric(PRETRAIN)),
        (r'\xmark & \cmark', kubric('ablation_temporal_self_attn_b3de55ap_canonical_cached')),
        (r'\cmark & \xmark', kubric('ablation_cam_self_attn_folhop3e_canonical_cached')),
        (r'\xmark & \xmark', kubric('ablation_cam_temporal_self_attn_cnmw9dcf_canonical_cached')),
    ]
    ablation_table('ablation_camattn', 'cc',
                   r'\multirow{2}{*}{\shortstack{Temporal\\Self-Attn.}} & '
                   r'\multirow{2}{*}{\shortstack{Camera\\Self-Attn.}}', rows, 2)


def ablation_encoder():
    rows = [
        ('Base (86M)', kubric('ablation_encoder_size_base_hv8nguwx_canonical_cached')),
        ('Large (300M)', kubric(PRETRAIN)),
        ('Giant (1B)', kubric('ablation_encoder_size_giant_ubk4lvez_canonical_cached')),
        ('Gigantic (2B)', kubric('ablation_encoder_size_gigantic_u1c34ou7_canonical_cached')),
    ]
    ablation_table('ablation_encoder', 'l', r'\multirow{2}{*}{Encoder Size}', rows, 1)


def ablation_latent():
    rows = [
        ('256', kubric('ablation_latent_dim_256_lczwsdx3_canonical_cached')),
        ('512', kubric(PRETRAIN)),
        ('1024', kubric('ablation_latent_dim_1024_wk2i4o1u_canonical_cached')),
    ]
    ablation_table('ablation_latent', 'c', r'\multirow{2}{*}{Latent Dim }', rows, 1)


# ---------------------------------------------------------------------------------------------------------------------
# Tab. cotracker_triangulation (data/cotracker_triangulation_stats.csv, from cotracker_triangulation_stats.py)

TRIANGULATION_ROWS = [   # (dataset, cameras in the csv, label)
    ('kubric-multiview', '4 (canonical)', 'Multi-view Kubric'),
    ('dex_ycb', '4 (canonical)', 'DexYCB'),
    ('cmupanoptic_3dgs', '4 (canonical)', 'Panoptic Studio'),
    None,
    ('point-odyssey-human', '4', 'Multi-view Point Odyssey - Human'),
    ('point-odyssey-human', '9', 'Multi-view Point Odyssey - Human'),
    ('po-animal-sub256-motion', '4', 'Multi-view Point Odyssey - Animal'),
    ('po-animal-sub256-motion', '9', 'Multi-view Point Odyssey - Animal'),
]


def cotracker_triangulation():
    df = pd.read_csv(paths.PAPER_DATA / 'cotracker_triangulation_stats.csv', dtype={'cameras': str})
    df = df.set_index(['dataset', 'cameras'])
    lines, i = [], 0
    for spec in TRIANGULATION_ROWS:
        if spec is None:
            lines.append(r'\midrule')
            i = 0
            continue
        ds, cams, label = spec
        r = df.loc[(ds, cams)]
        c = cells([r['pct_pairs_failed'], r['pct_of_failures_not_visible_enough'], r['pct_of_failures_visible_enough']])
        lines.append(row_tex(f'{label} & {cams.split()[0]}', c, gray=(i % 2 == 0)))
        i += 1
    body = '\n'.join(lines)
    write('cotracker_triangulation', rf"""
\begin{{tabular}}{{llccc}}
\toprule
 & & & \multicolumn{{2}}{{c}}{{Cause of the triangulation failures (\%)}} \\
\cmidrule(lr){{4-5}}
Dataset & Number of Views & Total failures (\%) & Not visible enough & Visible enough \\
\midrule
{body}
\bottomrule
\end{{tabular}}""")


# ---------------------------------------------------------------------------------------------------------------------
# Tab. tapvid3D_results (official TAPVid-3D metrics, median scaling)

TAPVID_DATASETS = ['tapvid3d_drivetrack', 'tapvid3d_adt', 'tapvid3d_pstudio']
# from the D4RT (Zhang et al. 2026) and ARROW (Fradlin et al. 2026) papers: DriveTrack | ADT | PStudio, AJ APD OA
LITERATURE_TAPVID = [
    (r'D4RT~\cite{zhang2026d4rt}', r'$\times$',
     [0.257, 0.345, 0.875, 0.240, 0.319, 0.926, 0.138, 0.186, 0.897], False),
    (r'ARROW~\cite{fradlin2026arrow}', r'$\times$',
     [0.241, 0.350, 0.816, 0.360, 0.473, 0.902, 0.141, 0.201, 0.870], False),
    None,
    (r'D4RT~\cite{zhang2026d4rt}', r'$\checkmark$',
     [0.304, 0.410, 0.875, 0.307, 0.408, 0.926, 0.372, 0.498, 0.897], True),
]
TAPVID_RUN = 'main_finetune_vzkjqrys_tapvid3d_official_minival_vis0.1_occunk'


def tapvid3d_results():
    res = json.load(open(paths.TRACKTAIL_OUTPUTS / TAPVID_RUN / 'tapvid3d_official_median.json'))
    ours = [res[d]['summary'][k] for d in TAPVID_DATASETS
            for k in ('average_jaccard', 'average_pts_within_thresh', 'occlusion_accuracy')]
    rows = LITERATURE_TAPVID + [('Tracktail (Ours)', r'$\checkmark$', ours, False)]
    lines = []
    for r in rows:
        if r is None:
            lines.append(r'\midrule')
            continue
        name, intr, vals, gray = r
        c = cells(vals, decimals=3)
        groups = [' & '.join(x.tex() for x in c[i:i + 3]) for i in (0, 3, 6)]
        lines.append((r'\rowcolor{rowgray}' + '\n' if gray else '') + f'{name}\n  & {intr}\n  & '
                     + '\n  & '.join(groups) + r' \\')
    body = '\n'.join(lines)
    n_adt = res['tapvid3d_adt']['summary']['n_trials']
    write('tapvid3D_results', rf"""
% Tracktail: {TAPVID_RUN}/tapvid3d_official_median.json; ADT on {n_adt} of the 50 mini-val videos
\begin{{tabular}}{{l c ccc ccc ccc}}
\toprule
\multirow{{2}}{{*}}{{Method}}
  & \multirow{{2}}{{*}}{{GT intr.}}
  & \multicolumn{{3}}{{c}}{{DriveTrack}}
  & \multicolumn{{3}}{{c}}{{Aria Digital Twin}}
  & \multicolumn{{3}}{{c}}{{Panoptic Studio}} \\
\cmidrule(lr){{3-5}}\cmidrule(lr){{6-8}}\cmidrule(lr){{9-11}}
  &
  & AJ$\uparrow$ & APD$_\text{{3D}}\uparrow$ & OA$\uparrow$
  & AJ$\uparrow$ & APD$_\text{{3D}}\uparrow$ & OA$\uparrow$
  & AJ$\uparrow$ & APD$_\text{{3D}}\uparrow$ & OA$\uparrow$ \\
\midrule
{body}
\bottomrule
\end{{tabular}}""")


def _body_tokens(tex):
    """Numbers of the rows of a tabular (after the first midrule), with their bold (B) / underline (U) mark."""
    import re
    tex = '\n'.join(re.sub(r'(?<!\\)%.*', '', line) for line in tex.split('\n'))
    tab = re.search(r'\\begin\{tabular\}.*?\\end\{tabular\}', tex, re.S).group(0)
    body = tab.split(r'\midrule', 1)[1].split(r'\bottomrule')[0]
    body = re.sub(r'\\cite\{[^}]*\}|\\rowcolor\{rowgray\}', '', body)
    toks = re.findall(r'\\textbf\{([\d.]+)\}|\\underline\{([\d.]+)\}|(?<![\w.])(\d+\.?\d*)', body)
    return [('B' + b if b else 'U' + u if u else n) for b, u, n in toks]


def check(overleaf):
    """Compare tables/*.tex with the tables of the paper source; returns the number of tables that differ."""
    import re
    from pathlib import Path
    src = ''.join(Path(overleaf, 'sec', f).read_text() for f in ('4_experiments.tex', '7_suppl.tex'))
    n_bad = 0
    for table in TABLES:
        name = table.__name__.replace('tapvid3d_results', 'tapvid3D_results')
        m = re.search(r'\\begin\{table\*?\}((?:(?!\\end\{table).)*?\\label\{tab:' + name + r'\}.*?)\\end\{table\*?\}',
                      src, re.S)
        paper = _body_tokens(m.group(1))
        ours = _body_tokens((paths.TABLE_OUT / f'{name}.tex').read_text())
        diffs = [(i, p, o) for i, (p, o) in enumerate(zip(paper, ours)) if p != o]
        ok = not diffs and len(paper) == len(ours)
        n_bad += not ok
        print(f"[check] {name:24s} {'OK' if ok else 'DIFFERS'} ({len(ours)} numbers)"
              + ('' if ok else f' paper vs ours (index, paper, ours): {diffs[:10]}, lengths {len(paper)}/{len(ours)}'))
    return n_bad


TABLES = [main_results, po_results, ablation_camattn, ablation_encoder, ablation_latent, cotracker_triangulation,
          tapvid3d_results]

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', metavar='OVERLEAF_DIR', help='paper source to compare the numbers with')
    args = ap.parse_args()
    for table in TABLES:
        table()
    if args.check:
        sys.exit(check(args.check) > 0)
