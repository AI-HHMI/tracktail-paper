# Test-set error metrics (query-first)

Metrics via `get_eval_metrics_paper` (the paper protocol: per track, query frame and earlier frames not evaluated, mean of the static and dynamic tracks on kubric / dex_ycb), aggregated over test trials.

## Cameras used

Read from `cam_names_used` in each saved prediction.

| dataset | cameras used |
|---|---|
| cmupanoptic_3dgs | 1 7 14 20 |
| dex_ycb | view_00 view_01 view_02 view_03 |
| kubric-multiview | view_0 view_1 view_2 view_3 |

## Mean over trials

| dataset | #tr | mte | ate | delta-x-avg | survival-rate | occlusion-acc | avg-jaccard |
|---|---|---|---|---|---|---|---|
| cmupanoptic_3dgs | 6 | 0.0274 | 0.0284 | 0.9549 | 0.9997 | 0.9274 | 0.8652 |
| dex_ycb | 10 | 0.0058 | 0.0056 | 0.9384 | 0.9996 | 0.9155 | 0.8489 |
| kubric-multiview | 30 | 0.0829 | 0.0922 | 0.8695 | 0.9699 | 0.9232 | 0.7740 |

## Median over trials

| dataset | #tr | mte | ate | delta-x-avg | survival-rate | occlusion-acc | avg-jaccard |
|---|---|---|---|---|---|---|---|
| cmupanoptic_3dgs | 6 | 0.0292 | 0.0297 | 0.9534 | 1.0000 | 0.9363 | 0.8689 |
| dex_ycb | 10 | 0.0054 | 0.0053 | 0.9446 | 1.0000 | 0.9159 | 0.8451 |
| kubric-multiview | 30 | 0.0729 | 0.0811 | 0.8716 | 0.9723 | 0.9232 | 0.7769 |

Thresholds (world units): cmupanoptic_3dgs [0.05, 0.1, 0.2, 0.4] surv=1.0; dex_ycb [0.01, 0.02, 0.05, 0.1, 0.2] surv=0.1; kubric-multiview [0.05, 0.1, 0.2, 0.4, 0.8] surv=0.5. Per-trial breakdowns in `<dataset>/metrics.json`.

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