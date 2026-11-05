# Provenance of data/

Copied on 2026-11-05 from the Janelia file system. The paper's protocol for all Tracktail numbers:
**visibility threshold 0.1, query-frame occlusion unknown** (`QUERY_OCC=unknown`, no GT visibility input at the query
frame), paper metrics of `eval_metrics_paper.py` in the Tracktail code (mean of per-trial means).
Paths in the "made by" column are relative to the Tracktail code repository (branch `paper`). Code: Tracktail code repository, branch `paper`; see its README for the commands that produce each tree.

`data/results/` is a sparse copy of the result trees (the Tracktail tree, `posetail-outputs-vis0.1-occunknown` on disk, is stored as `tracktail-outputs`, the name the current drivers write): only the `*.json`, `*.md`, `*.csv` files (< 2 MB) of the runs used in
the paper, with the same relative paths. Per-trial prediction files (`*_trial.npz`, `cotracker_3d.npz`) are not included.
`python build_paper_data.py collect` refreshes it (list of runs: `PAPER_RUNS` in that script).

| data/ path | source (Janelia) | made by | date | notes |
|---|---|---|---|---|
| `results/tracktail-outputs/<run>/{summary.json,metrics.md,…}` | `/groups/karashchuk/home/karashchukl/results/paper-final-v2/posetail-outputs-vis0.1-occunknown/` | `scripts/tracktail_cached.sh`, `scripts/tracktail_cached_po.sh` → `scripts/eval_testset_metrics.py` (`QUERY_OCC=unknown`, vis 0.1) | 2026-10-28 (temporal-attn ablations `b3de55ap`, `cnmw9dcf`: 2026-11-05) | Tracktail rows of all tables. Runs: `main_finetune_vzkjqrys_*` (paper model, ckpt 2314240), `main_pretrain_e25w9v86_*` and `ablation_*` (pretraining stage, 800k it.) |
| `results/tracktail-outputs/ncam_ablation_dexycb/` | same tree | `scripts/eval_ncam_ablation.sh` | 2026-10-28 | Fig. n_cams, Tracktail curve |
| `results/tracktail-outputs/main_finetune_vzkjqrys_tapvid3d_official_minival_vis0.1_occunk/tapvid3d_official_{median,none}.{json,md}` | same tree | `scripts/tracktail_tapvid3d_official.sh` → `scripts/tapvid3d_official_metrics.py` | 2026-10-28 | Tab. tapvid3D_results uses `median` (per-sequence median scaling). ADT: 49 of 50 videos |
| `results/cotracker-outputs/{paper-canonical-cached,paper-po-4cams,paper-po-9cams,ncam-ablation-dexycb}/` | `/groups/karashchuk/home/ruppk2/results/paper-final-v2/cotracker-outputs/` | `cotracker_baseline/cotracker_cached.sh`, `cotracker_cached_po.sh`, `cotracker_ncam_ablation.sh` → `mvtracker_baseline/mvtracker_metrics.py` | 2026-10-20/21 | CoTracker3 visibility from the predictor (> 0.9) |
| `results/mvtracker-outputs/paper-canonical-cached-{duster,gt}/` | `/groups/karashchuk/home/ruppk2/results/paper-final-v2/mvtracker-outputs/` | `mvtracker_baseline/mvtracker_cached.sh` | 2026-10-19 | official vis thresholds (Kubric 0.5, DexYCB/Panoptic 0.01). No GT depth for DexYCB |
| `results/mvtracker-outputs/paper-po-{4,9}cams-{duster,gt}_0.5/` | same | `mvtracker_baseline/mvtracker_cached_po.sh` with `VIS_THRESHOLD=0.5` | 2026-10-22 | Tab. po_results |
| `results/mvtracker-outputs/ncam-ablation-dexycb/` | same | `mvtracker_baseline/mvtracker_ncam_ablation_native.sh` (DUSt3R depth) | 2026-10-21 | Fig. n_cams |
| `results/mvtracker-outputs-dexycb-sensordepth/paper-canonical-cached-sensor-linear/` | `/groups/karashchuk/home/karashchukl/results/paper-final-v2/mvtracker-outputs-dexycb-sensordepth/` | `mvtracker_baseline/mvtracker_dexycb_sensordepth.sh` (Kinect depth, linear interpolation) | 2026-10-28 | MVTracker "GT depth" DexYCB cells (†) |
| `results/arrow-outputs/{paper-canonical-cached,paper-po-4cams,ncam-ablation-dexycb}/` | `/groups/karashchuk/home/karashchukl/results/paper-final-v2/arrow-outputs/` | `arrow_baseline/arrow_cached.sh`, `arrow_cached_po.sh`, `arrow_ncam_ablation.sh` (`SCALE_MODE=gt-tracks`, `MAX_ANCHORS=24`, window 24) | 2026-10-26 | main_results ARROW row, po_results 4-view columns, n_cams |
| `results/arrow-outputs-w24/paper-po-9cams/` | `/groups/karashchuk/home/karashchukl/results/paper-final-v2/arrow-outputs-w24/paper-po-9cams/` | `arrow_baseline/arrow_cached_po.sh 9` with `WINDOW=24` (other settings as above) | 2026-11-05 | po_results 9-view columns (`ARROW_PO9_OUTPUTS`). Replaces the window-12 run `arrow-outputs/paper-po-9cams` (not in data/) |
| `survival_curves.csv` | computed | `build_paper_data.py survival` from the per-trial npz of the trees above (Tracktail `main_finetune_vzkjqrys_po_{4,9}cams`, CoTracker `paper-po-*`, MVTracker `paper-po-*-{gt,duster}` (no `_0.5`; GT visibility is used), ARROW `paper-po-4cams` + `arrow-outputs-w24/paper-po-9cams`) and `TRACKTAIL_DATA=/groups/karashchuk/karashchuklab/animal-datasets-processed/posetail-pretraining-v6` | 2026-11-05 | thresholds 0.3–15 PO units. Equal (to float precision) to `/groups/karashchuk/home/karashchukl/projects/posetail/posetail-next/scratch/figs_occunk/paper_data/survival_curves.csv`, which made the overleaf PDFs; adds the ARROW rows |
| `dexycb_ncam_results.csv` | computed | `build_paper_data.py ncam` from the 4 `ncam*` summaries | 2026-11-05 | AJ (%), 1 decimal |
| `cotracker_triangulation_stats{,_detail}.csv` | `/home/ruppk2@hhmi.org/tracktail-paper/data/v2/` | `cotracker_triangulation_stats.py` | 2026-10-26 | Tab. cotracker_triangulation |
| `speed/*.jsonl`, `speed/summary.{csv,md}`, `speed/nvidia-smi.txt` | `benchmark_speed/results/a100_mvtracker_20261026_133500/` of the Tracktail code (tracked there) | `benchmark_speed/bench.py` on one A100 | 2026-10-26 | Figs. speed_memory, speed_memory_tracktail |
| `rat7m/cloud.npz` | `/groups/karashchuk/home/karashchukl/projects/posetail/posetail-next/dev/scratch/pointcloud/out/cover_script/cloud.npz` | `scripts/cover_rat7m_demo.py --stages cloud` (SAM + visual hull + VGGT) | 2026-11-04 | cover figure point cloud at frame 670 |
| `rat7m/tracktail_output.npz`, `rat7m/render_info.json` | `/home/ruppk2@hhmi.org/posetail/paper_figures/rat7m_movement/s5-d1__101500__670/` | Tracktail on Rat7M `s5-d1/101500` from frame 670 | 2026-10-01 | cover figure tracks |
| `occunknown_numbers.{json,md}` | `/groups/karashchuk/home/karashchukl/projects/posetail/posetail-next/scratch/occunknown_numbers.{json,md}` | the 2026-10-28 occ-unknown evaluation | 2026-10-28 | historical record of the table rows; `tables.py` reproduces them |

`archive/make_figs_occunk_2026-10-28.py` is the script (from `/groups/karashchuk/home/karashchukl/projects/posetail/posetail-next/scratch/figs_occunk/make_figs.py`) that made
the overleaf `n_cams_figure.pdf` and both survival PDFs; `build_paper_data.py` + `build_figures.py` replace it.
