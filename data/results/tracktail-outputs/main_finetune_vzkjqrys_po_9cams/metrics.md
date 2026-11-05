# Test-set error metrics (query-first)

Metrics via `get_eval_metrics_paper` (the paper protocol: per track, query frame and earlier frames not evaluated, mean of the static and dynamic tracks on kubric / dex_ycb), aggregated over test trials.

## Cameras used

Read from `cam_names_used` in each saved prediction.

| dataset | cameras used |
|---|---|
| po-animal-sub256-motion | view0 view1 view2 view3 view4 view5 view6 view7 view8 |
| point-odyssey-human | view0 view1 view2 view3 view4 view5 view6 view7 view8 |

## Mean over trials

| dataset | #tr | mte | ate | delta-x-avg | survival-rate | occlusion-acc | avg-jaccard |
|---|---|---|---|---|---|---|---|
| po-animal-sub256-motion | 10 | 0.6732 | 0.7344 | 0.7559 | 1.0000 | 0.9839 | 0.6968 |
| point-odyssey-human | 8 | 1.0926 | 1.0805 | 0.6646 | 0.9991 | 0.9702 | 0.6092 |

## Median over trials

| dataset | #tr | mte | ate | delta-x-avg | survival-rate | occlusion-acc | avg-jaccard |
|---|---|---|---|---|---|---|---|
| po-animal-sub256-motion | 10 | 0.5944 | 0.5805 | 0.7789 | 1.0000 | 0.9867 | 0.7286 |
| point-odyssey-human | 8 | 1.0912 | 1.0785 | 0.6883 | 1.0000 | 0.9687 | 0.6294 |

Thresholds (world units): po-animal-sub256-motion [0.3, 0.6, 1.2, 2.4, 4.8] surv=50; point-odyssey-human [0.3, 0.6, 1.2, 2.4, 4.8] surv=50. Per-trial breakdowns in `<dataset>/metrics.json`.

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