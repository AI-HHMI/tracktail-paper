"""Input/output locations for the tracktail-paper scripts and notebooks.

Every location can be set with an environment variable; the names match paper.env of the Tracktail code
(https://github.com/AI-HHMI/tracktail, branch paper). The defaults point inside this repository, so the tables and
figures build from the committed result summaries in data/ with no other setup.

    PAPER_DATA         derived data of the figures (survival curves, n-cams AJ, ...)          default: data/
    TRACKTAIL_RESULTS  root of the result trees, as the Tracktail code writes them            default: data/results
                       (data/results is a sparse copy holding only the small summary files)
    TRACKTAIL_OUTPUTS, COTRACKER_OUTPUTS, MVTRACKER_OUTPUTS, MVTRACKER_SENSORDEPTH_OUTPUTS, ARROW_OUTPUTS
                       one result tree each; default $TRACKTAIL_RESULTS/{tracktail-outputs, cotracker-outputs,
                       mvtracker-outputs, mvtracker-outputs-dexycb-sensordepth, arrow-outputs}
    ARROW_PO9_OUTPUTS  the ARROW MV Point Odyssey 9-camera run, 24-frame windows
                       default: $ARROW_OUTPUTS/paper-po-9cams (what arrow_baseline/arrow_cached_po.sh writes)
    TRACKTAIL_DATA     processed datasets, <TRACKTAIL_DATA>/<dataset>/<split>/<session>/trial/  no default
                       (needed to recompute survival curves / triangulation stats, and for the PO figures)
    TRACKTAIL_CODE     a checkout of the Tracktail code                    default: ../tracktail, else ../posetail-next
    RENDERS_ROOT       rendered videos of the qualitative figure (scripts/render_qualitative_gtvis.sh)   no default
    RAT7M_TRIAL        the processed Rat7M trial of the cover figure (.../rat7m/test/s5-d1/101500)    no default
    RAT7M_RENDERS      optional: rendered Tracktail video of that trial                                no default
    SPEED_RESULTS      speed benchmark jsonl files (benchmark_speed/run_all.sh output)      default: data/speed
    FIG_OUT, TABLE_OUT output folders                                                 default: figures/, tables/

When a result file is missing from a configured tree (e.g. you reran the main results but did not retrain the
ablation models), result() falls back to the committed copy in data/results and prints a warning.
"""
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent


def _env_path(name, default):
    value = os.environ.get(name)
    return Path(value).expanduser() if value else (Path(default) if default is not None else None)


PAPER_DATA = _env_path('PAPER_DATA', REPO / 'data')
TRACKTAIL_RESULTS = _env_path('TRACKTAIL_RESULTS', REPO / 'data' / 'results')

# One tree per method. (On the Janelia file system the Tracktail tree is
# paper-final-v2/posetail-outputs-vis0.1-occunknown; see data/PROVENANCE.md.)
TRACKTAIL_OUTPUTS = _env_path('TRACKTAIL_OUTPUTS', TRACKTAIL_RESULTS / 'tracktail-outputs')
COTRACKER_OUTPUTS = _env_path('COTRACKER_OUTPUTS', TRACKTAIL_RESULTS / 'cotracker-outputs')
MVTRACKER_OUTPUTS = _env_path('MVTRACKER_OUTPUTS', TRACKTAIL_RESULTS / 'mvtracker-outputs')
MVTRACKER_SENSORDEPTH_OUTPUTS = _env_path('MVTRACKER_SENSORDEPTH_OUTPUTS',
                                          TRACKTAIL_RESULTS / 'mvtracker-outputs-dexycb-sensordepth')
ARROW_OUTPUTS = _env_path('ARROW_OUTPUTS', TRACKTAIL_RESULTS / 'arrow-outputs')
# ARROW on MV Point Odyssey with 9 cameras, 24-frame windows (WINDOW=24, the default of arrow_cached_po.sh). The
# committed copy is the Janelia rerun in arrow-outputs-w24/paper-po-9cams (see data/PROVENANCE.md).
ARROW_PO9_OUTPUTS = _env_path('ARROW_PO9_OUTPUTS', ARROW_OUTPUTS / 'paper-po-9cams')

TRACKTAIL_DATA = _env_path('TRACKTAIL_DATA', None)
_code_default = REPO.parent / 'tracktail'
if not _code_default.exists() and (REPO.parent / 'posetail-next').exists():
    _code_default = REPO.parent / 'posetail-next'   # older local folder name of the same repository
TRACKTAIL_CODE = _env_path('TRACKTAIL_CODE', _code_default)
RENDERS_ROOT = _env_path('RENDERS_ROOT', None)
RAT7M_TRIAL = _env_path('RAT7M_TRIAL', None)
RAT7M_RENDERS = _env_path('RAT7M_RENDERS', None)

SPEED_RESULTS = _env_path('SPEED_RESULTS', REPO / 'data' / 'speed')

FIG_OUT = _env_path('FIG_OUT', REPO / 'figures')
TABLE_OUT = _env_path('TABLE_OUT', REPO / 'tables')


def require(path, name):
    """Raise a clear error if an optional location is not set or does not exist."""
    if path is None:
        raise SystemExit(f'{name} is not set; export {name}=/path/to/... (see paths.py)')
    if not Path(path).exists():
        raise SystemExit(f'{name}={path} does not exist')
    return Path(path)


COMMITTED_RESULTS = REPO / 'data' / 'results'
# configured tree -> its committed copy (most specific first)
_COMMITTED = [
    (ARROW_PO9_OUTPUTS, COMMITTED_RESULTS / 'arrow-outputs' / 'paper-po-9cams'),
    (TRACKTAIL_OUTPUTS, COMMITTED_RESULTS / 'tracktail-outputs'),
    (COTRACKER_OUTPUTS, COMMITTED_RESULTS / 'cotracker-outputs'),
    (MVTRACKER_SENSORDEPTH_OUTPUTS, COMMITTED_RESULTS / 'mvtracker-outputs-dexycb-sensordepth'),
    (MVTRACKER_OUTPUTS, COMMITTED_RESULTS / 'mvtracker-outputs'),
    (ARROW_OUTPUTS, COMMITTED_RESULTS / 'arrow-outputs'),
]


def result(path):
    """`path` if it exists, else the same file in the committed data/results copy (with a warning)."""
    path = Path(path)
    if path.exists():
        return path
    for tree, committed in _COMMITTED:
        try:
            rel = path.relative_to(tree)
        except ValueError:
            continue
        fallback = committed / rel
        if fallback != path and fallback.exists():
            print(f'[warn] {path} not found; using the committed copy {fallback.relative_to(REPO)}')
            return fallback
        break
    return path
