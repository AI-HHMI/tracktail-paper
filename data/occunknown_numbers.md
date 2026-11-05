# Tracktail numbers with unknown query-frame occlusion (QUERY_OCC=unknown)

No GT visibility input at the query frame (occlusion input -1 for all cameras); the model's own predicted occlusion
(σ>0.1) is still carried between windows. Everything else as the paper's vis0.1 runs (n_overlap 8, canonical cams,
same track files, vis thresh 0.1). Source: `/groups/karashchuk/home/karashchukl/results/paper-final-v2/posetail-outputs-vis0.1-occunknown` (+ `main_finetune_vzkjqrys_tapvid3d_official_minival_vis0.1_occunk`).
Units as format_tables_v2.ipynb: AJ/δ/OA ×100; MTE ×100 (cm) DexYCB/Panoptic, ×13 Kubric, ×1 PO. TAPVid-3D: median scaling, 3 decimals.
Full numbers: `scratch/occunknown_numbers.json`. LaTeX rows below have no bold/underline (re-mark by hand).

## Table 1 Tracktail row (Panoptic | DexYCB | Kubric; AJ δ OA MTE)
```
Tracktail (Ours) & MV-Kub+MV-PO & \xmark& 86.5 & 95.5 & 92.7 & 2.7 & 84.9 & 93.8 & 91.5 & 0.6 & 77.4 & 87.0 & 92.3 & 1.1 \\
```
## Table 2 PO (4 cams: human, animal | 9 cams: human, animal)
```
  & 54.2 & 61.1 & 93.5 & 1.6 & 60.9 & 69.0 & 95.1 & 0.9 & 60.9 & 66.5 & 97.0 & 1.1 & 69.7 & 75.6 & 98.4 & 0.7 \\
```
## Ablations (Kubric; Large / ✓ / 512 = main_pretrain_e25w9v86)
```
Base (80M) & 56.5 & 66.6 & 88.7 & 3.4 \\
Large (300M) & 60.2 & 70.4 & 89.4 & 2.8 \\
Giant (1B) & 61.7 & 71.8 & 89.5 & 2.6 \\
Gigantic (2B) & 62.1 & 72.4 & 89.5 & 2.6 \\

\xmark & 49.4 & 59.4 & 86.7 & 5.1 \\
\cmark & 60.2 & 70.4 & 89.4 & 2.8 \\

256 & 56.2 & 66.4 & 88.6 & 3.2 \\
512 & 60.2 & 70.4 & 89.4 & 2.8 \\
1024 & 59.9 & 70.2 & 89.4 & 2.9 \\
```
## n_cams figure, Tracktail AJ (DexYCB)
| N | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| AJ | 67.4 | 79.0 | 83.2 | 83.2 | 84.6 | 86.0 | 86.9 | 87.3 |

## TAPVid-3D (suppl, DriveTrack | ADT | PStudio; AJ APD3D OA)
```
  Tracktail (Ours)
     & $\checkmark$
     & 0.058 & 0.100 & 0.797
     & 0.068 & 0.125 & 0.740
     & 0.228 & 0.353 & 0.797 \\
```

## Survival (PO, threshold 1.2 units, Tracktail): frame 25 / last frame
4 cams: human 0.883 / 0.421, animal 0.893 / 0.382; 9 cams: human 0.945 / 0.502, animal 0.975 / 0.542.

## Figures (regenerated; Tracktail inputs from occunknown, other methods unchanged)
`scratch/figs_occunk/`: n_cams_figure.pdf, po_survival_comparison_1.2.pdf, po_survival_tracktail.pdf
(script `scratch/figs_occunk/make_figs.py`, data in `scratch/figs_occunk/paper_data/`; originals untouched).
