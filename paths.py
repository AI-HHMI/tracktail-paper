"""Input/output locations for the tracktail-paper scripts and notebooks.

Every location can be set with an environment variable. The defaults point inside this repository, so the tables and
figures build from the committed result summaries in data/ with no other setup.

    PAPER_DATA       derived data of the figures (survival curves, n-cams AJ, triangulation stats)   default: data/
    RESULTS_ROOT     root of the result trees, laid out as posetail-next writes them              default: data/results
                     (data/results is a sparse copy with only the small summary files)
    TRACKTAIL_RESULTS, COTRACKER_RESULTS, MVTRACKER_RESULTS, MVTRACKER_SENSORDEPTH_RESULTS, ARROW_RESULTS
                     one result tree each, default: $RESULTS_ROOT/<tree name below>
    ARROW_PO9_RESULTS  the ARROW Point Odyssey 9-camera run (see TODO below)
    DATA_ROOT        processed datasets (<DATA_ROOT>/<dataset>/test/<session>/trial/{metadata.yaml,pose3d*.npz,img/})
                     only needed to recompute survival curves and CoTracker triangulation stats from predictions
    POSETAIL_NEXT    a posetail-next checkout (paper branch)                                       default: ../posetail-next
    RENDERS_ROOT     rendered tracking videos of the qualitative figure (render_qualitative_gtvis.sh) no default
    RAT7M_TRIAL      the processed Rat7M trial of the cover figure (.../rat7m/test/s5-d1/101500)   no default
    RAT7M_RENDERS    optional: Tracktail render of that trial (posetail-next render_video)         no default
    FIG_OUT, TABLE_OUT  output folders                                                             default: figures/, tables/
"""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent


def _env_path(name, default):
    value = os.environ.get(name)
    return Path(value).expanduser() if value else (Path(default) if default is not None else None)


PAPER_DATA = _env_path('PAPER_DATA', REPO / 'data')
RESULTS_ROOT = _env_path('RESULTS_ROOT', REPO / 'data' / 'results')

# result tree names (the folder names used on the Janelia file system and in the posetail-next drivers)
TRACKTAIL_RESULTS = _env_path('TRACKTAIL_RESULTS', RESULTS_ROOT / 'posetail-outputs-vis0.1-occunknown')
COTRACKER_RESULTS = _env_path('COTRACKER_RESULTS', RESULTS_ROOT / 'cotracker-outputs')
MVTRACKER_RESULTS = _env_path('MVTRACKER_RESULTS', RESULTS_ROOT / 'mvtracker-outputs')
MVTRACKER_SENSORDEPTH_RESULTS = _env_path('MVTRACKER_SENSORDEPTH_RESULTS',
                                          RESULTS_ROOT / 'mvtracker-outputs-dexycb-sensordepth')
ARROW_RESULTS = _env_path('ARROW_RESULTS', RESULTS_ROOT / 'arrow-outputs')
# TODO(arrow-w24): the paper's ARROW PO 9-camera numbers are being rerun with 24-frame windows into
# arrow-outputs-w24/paper-po-9cams. Switch this default to RESULTS_ROOT / 'arrow-outputs-w24' / 'paper-po-9cams'
# once that run is final (and copied into data/results with `python build_paper_data.py collect`).
ARROW_PO9_RESULTS = _env_path('ARROW_PO9_RESULTS', ARROW_RESULTS / 'paper-po-9cams')

DATA_ROOT = _env_path('DATA_ROOT', None)
POSETAIL_NEXT = _env_path('POSETAIL_NEXT', REPO.parent / 'posetail-next')
RENDERS_ROOT = _env_path('RENDERS_ROOT', None)
RAT7M_TRIAL = _env_path('RAT7M_TRIAL', None)
RAT7M_RENDERS = _env_path('RAT7M_RENDERS', None)

FIG_OUT = _env_path('FIG_OUT', REPO / 'figures')
TABLE_OUT = _env_path('TABLE_OUT', REPO / 'tables')


def require(path, name):
    """Raise a clear error if an optional location is not set or does not exist."""
    if path is None:
        raise SystemExit(f'{name} is not set; export {name}=/path/to/... (see paths.py)')
    if not Path(path).exists():
        raise SystemExit(f'{name}={path} does not exist')
    return Path(path)
