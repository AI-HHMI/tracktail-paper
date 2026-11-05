# tracktail-paper

Figures and tables of the Tracktail paper. The model, training and evaluation code is in
the [Tracktail code repository](https://github.com/AI-HHMI/tracktail) (branch `paper`); dataset converters are in
[tracktail-preprocessing](https://github.com/AI-HHMI/tracktail-preprocessing).

Two ways to use this repository:
- **Quick path** (no GPU, no datasets): rebuild every result table and the plotted figures from the result summaries
  committed in `data/`.
- **Full path**: rerun the evaluations with the Tracktail code (branch `paper`), point this repository at your result trees, and rebuild
  `data/` and then the tables and figures.

## Environment

[pixi](https://pixi.sh):

```bash
pixi install
pixi run paper          # = tables + figures + speed (quick path)
```

Without pixi: Python 3.12 with `numpy pandas matplotlib seaborn pyyaml scipy opencv-python jupyter aniposelib`
(see `pixi.toml`), then run the same commands with `python`.

## Quick path: data/ -> tables/ and figures/

```bash
pixi run python tables.py --check ../tracktail-overleaf   # tables/*.tex; --check compares every number with the paper
pixi run python build_figures.py                         # figures/n_cams_figure.pdf, po_survival_*.pdf
pixi run speed                                           # figures/speed_memory*_figure.pdf (runs figure_speed.ipynb)
```

`--check` is optional (needs the paper source). All seven tables currently match the paper, numbers and bold/underline.

## Paper item -> producer

| Paper item | Label | Producer | Inputs | Output |
|---|---|---|---|---|
| Cover figure, Rat7M panels | `fig:rat7m` | `figure_rat7m.ipynb` (composited by hand in `cover_figure_draft_liliedit2.svg`, overleaf) | Rat7M trial (`RAT7M_TRIAL`), `data/rat7m/{cloud,tracktail_output}.npz` | `figures/rat7m/*.pdf` |
| MV Point Odyssey examples | `fig:po_examples` | `figure_po_examples.ipynb` | MV-PO train split (`TRACKTAIL_DATA`) | `figures/po_examples.pdf` |
| Architecture (image crops) | `fig:architecture` | `figure_po_architecture.ipynb` (crops only; the diagram is a hand-made SVG in overleaf) | MV-PO train split (`TRACKTAIL_DATA`) | `figures/architecture/` |
| Main results | `tab:main_results` | `tables.py` | `data/results` | `tables/main_results.tex` |
| MV Point Odyssey results | `tab:po_results` | `tables.py` | `data/results` | `tables/po_results.tex` |
| Temporal / camera self-attention ablation | `tab:ablation_camattn` | `tables.py` | `data/results` | `tables/ablation_camattn.tex` |
| Qualitative comparison | `fig:qualitative_comparison` | `figure_qualitative.ipynb` | rendered videos (`RENDERS_ROOT`) | `figures/qualitative_comparison.pdf` |
| AJ vs number of views (DexYCB) | `fig:ncams` | `build_figures.py n_cams` | `data/dexycb_ncam_results.csv` | `figures/n_cams_figure.pdf` |
| Loss weights | `tab:loss_weights` | hand-written; values from `configs/paper/*.toml` of the Tracktail code (λ_3D = `coords_loss_weight` + `coords_loss_direct_weight`, λ_rep = config value / 16) | – | – |
| Survival, all methods (suppl.) | `fig:po_survival_comparison` | `build_figures.py survival_comparison` | `data/survival_curves.csv` | `figures/po_survival_comparison_1.2.pdf` |
| Survival, Tracktail thresholds (suppl.) | `fig:po_survival_tracktail` | `build_figures.py survival_tracktail` | `data/survival_curves.csv` | `figures/po_survival_tracktail.pdf` |
| CoTracker3 triangulation failures (suppl.) | `tab:cotracker_triangulation` | `tables.py` | `data/cotracker_triangulation_stats.csv` | `tables/cotracker_triangulation.tex` |
| Encoder size ablation (suppl.) | `tab:ablation_encoder` | `tables.py` | `data/results` | `tables/ablation_encoder.tex` |
| Latent dimension ablation (suppl.) | `tab:ablation_latent` | `tables.py` | `data/results` | `tables/ablation_latent.tex` |
| TAPVid-3D (suppl.) | `tab:tapvid3D_results` | `tables.py` | `data/results/.../tapvid3d_official_median.json` | `tables/tapvid3D_results.tex` |
| Speed and memory (suppl.) | `fig:speed_memory`, `fig:speed_memory_tracktail` | `figure_speed.ipynb` | `data/speed/*.jsonl` | `figures/speed_memory_figure.pdf`, `figures/speed_memory_tracktail_figure.pdf` |

The `tables/*.tex` files hold the `tabular` only; captions stay in the paper. Rows quoted from other papers
(MVTracker's Tab. 1 rows, D4RT and ARROW on TAPVid-3D) are constants in `tables.py`.

Units: AJ, δ_avg and OA in %; MTE in cm on Panoptic Studio and DexYCB (results are stored in m), ×13 on
Multi-view Kubric (MVTracker's unit), Point Odyssey scene units on MV Point Odyssey. TAPVid-3D: fractions.

The notebooks marked with `TRACKTAIL_DATA`, `RAT7M_TRIAL` or `RENDERS_ROOT` need raw data or renders that are not in this
repository (MV Point Odyssey download: see the README of the Tracktail code, branch `paper`; Rat7M: tracktail-preprocessing).
Run them with e.g. `TRACKTAIL_DATA=/data/tracktail pixi run jupyter nbconvert --to notebook --execute --inplace figure_po_examples.ipynb`.

## Paths

All inputs and outputs are set by environment variables, read in `paths.py` (see its docstring). The names match
`paper.env` of the Tracktail code.

| Variable | Default | Used for |
|---|---|---|
| `PAPER_DATA` | `data/` | survival / n-cams / triangulation csv files, speed results, Rat7M npz |
| `TRACKTAIL_RESULTS` | `data/results` | root of the result trees |
| `TRACKTAIL_OUTPUTS` | `$TRACKTAIL_RESULTS/tracktail-outputs` | Tracktail runs |
| `COTRACKER_OUTPUTS`, `MVTRACKER_OUTPUTS`, `ARROW_OUTPUTS` | `$TRACKTAIL_RESULTS/{cotracker,mvtracker,arrow}-outputs` | baselines |
| `MVTRACKER_SENSORDEPTH_OUTPUTS` | `$TRACKTAIL_RESULTS/mvtracker-outputs-dexycb-sensordepth` | MVTracker with DexYCB Kinect depth |
| `ARROW_PO9_OUTPUTS` | `$TRACKTAIL_RESULTS/arrow-outputs-w24/paper-po-9cams` | ARROW on MV-PO with 9 views (24-frame windows) |
| `TRACKTAIL_DATA` | – | processed datasets `<TRACKTAIL_DATA>/<dataset>/<split>/<session>/trial/` |
| `RENDERS_ROOT`, `RAT7M_TRIAL`, `RAT7M_RENDERS` | – | qualitative and cover figures |
| `TRACKTAIL_CODE` | `../tracktail` | checkout of the Tracktail code |
| `FIG_OUT`, `TABLE_OUT` | `figures/`, `tables/` | outputs |

## Full path: rerun the evaluations

1. Get the Tracktail code and follow its README (data, models, baseline environments, evaluation drivers):
   ```bash
   git clone -b paper https://github.com/AI-HHMI/tracktail ../tracktail
   ```
   The drivers use the paper protocol (visibility threshold 0.1, query occlusion unknown) and write
   `$TRACKTAIL_RESULTS/tracktail-outputs/<run>/summary.json` and
   `$TRACKTAIL_RESULTS/{cotracker,mvtracker,arrow}-outputs/<run>/combined_summary_metrics.csv`, the layout above.
   `data/PROVENANCE.md` lists which driver made each run.
2. Point this repository at the same folders (e.g. `source ../tracktail/paper.env`) and rebuild `data/`:
   ```bash
   pixi run python build_paper_data.py collect          # copy the small summary files into data/results
   pixi run python build_paper_data.py ncam survival    # data/dexycb_ncam_results.csv, data/survival_curves.csv
   pixi run python cotracker_triangulation_stats.py     # data/cotracker_triangulation_stats*.csv
   cp ../tracktail/benchmark_speed/results/<run>/*.jsonl data/speed/   # speed benchmark
   ```
3. Run the quick path.

Execution order: evaluations with the Tracktail code -> `build_paper_data.py` (+ `cotracker_triangulation_stats.py`) ->
`tables.py`, `build_figures.py`, `figure_speed.ipynb` -> the notebooks that need raw data
(`figure_qualitative.ipynb`, `figure_po_examples.ipynb`, `figure_po_architecture.ipynb`, `figure_rat7m.ipynb`).

## Other files

- `data/PROVENANCE.md`: where every file in `data/` came from (source path, flags, date).
- `sample_training_images.py`: browsing helper, copies random MV-PO training frames into `training_samples/` to pick
  examples for `figure_po_examples.ipynb`; not used for any figure.
- `archive/`: superseded notebooks (`format_tables*.ipynb`, `format_arrow.ipynb`, `figure_ncams.ipynb`,
  `figure_survival.ipynb`, `figure_qualitative_comparison.ipynb`, `format_fps_table.ipynb`), see `archive/README.md`.
