# Test-set error metrics (query-first)

Metrics via `get_eval_metrics_paper` (the paper protocol: per track, query frame and earlier frames not evaluated, mean of the static and dynamic tracks on kubric / dex_ycb), aggregated over test trials.

## Cameras used

Read from `cam_names_used` in each saved prediction.

| dataset | cameras used |
|---|---|
| kubric-multiview | view_0 view_1 view_2 view_3 |

## Mean over trials

| dataset | #tr | mte | ate | delta-x-avg | survival-rate | occlusion-acc | avg-jaccard |
|---|---|---|---|---|---|---|---|
| kubric-multiview | 30 | 0.2202 | 0.2299 | 0.7020 | 0.8880 | 0.8942 | 0.5995 |

## Median over trials

| dataset | #tr | mte | ate | delta-x-avg | survival-rate | occlusion-acc | avg-jaccard |
|---|---|---|---|---|---|---|---|
| kubric-multiview | 30 | 0.1977 | 0.2040 | 0.6960 | 0.8890 | 0.8989 | 0.5866 |

Thresholds (world units): kubric-multiview [0.05, 0.1, 0.2, 0.4, 0.8] surv=0.5. Per-trial breakdowns in `<dataset>/metrics.json`.

## TAPVid-3D camera-coordinate metrics (per-frame depth, mean)

Thresholds [0.01, 0.04, 0.16, 0.64, 2.56]; a point passes when dist/Z_depth < threshold. Survival threshold 0.5. Z_depth = per-point per-frame Z_cam.

_none_

## TAPVid-3D camera-coordinate metrics (per-frame depth, median)

_none_

## TAPVid-3D world-coordinate metrics (per-trajectory depth, mean)

Thresholds [0.01, 0.04, 0.16, 0.64, 2.56]; a point passes when dist/Z_depth < threshold. Survival threshold 0.5. Z_depth = per-trajectory mean Z_cam (adt + drivetrack only).

_none_

## TAPVid-3D world-coordinate metrics (per-trajectory depth, median)

_none_

## TAPVid-2D per-trajectory metrics (MVTracker "Our Metrics", mean)

Each track weighted equally (vs all-points-pooled in the standard table above). avg-jaccard-pertraj == avg-jaccard (get_average_jaccard is already per-trajectory).

_none_

## TAPVid-2D per-trajectory metrics (MVTracker "Our Metrics", median)

_none_