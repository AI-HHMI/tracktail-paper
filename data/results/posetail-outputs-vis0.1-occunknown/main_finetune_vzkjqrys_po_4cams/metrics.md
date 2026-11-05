# Test-set error metrics (query-first)

Metrics via `get_eval_metrics_paper` (the paper protocol: per track, query frame and earlier frames not evaluated, mean of the static and dynamic tracks on kubric / dex_ycb), aggregated over test trials.

## Cameras used

Read from `cam_names_used` in each saved prediction.

| dataset | cameras used |
|---|---|
| po-animal-sub256-motion | view2 view4 view5 view7 |
| point-odyssey-human | view2 view4 view5 view7 |

## Mean over trials

| dataset | #tr | mte | ate | delta-x-avg | survival-rate | occlusion-acc | avg-jaccard |
|---|---|---|---|---|---|---|---|
| po-animal-sub256-motion | 10 | 0.9031 | 0.9609 | 0.6903 | 1.0000 | 0.9515 | 0.6091 |
| point-odyssey-human | 8 | 1.5620 | 1.4802 | 0.6112 | 0.9969 | 0.9346 | 0.5422 |

## Median over trials

| dataset | #tr | mte | ate | delta-x-avg | survival-rate | occlusion-acc | avg-jaccard |
|---|---|---|---|---|---|---|---|
| po-animal-sub256-motion | 10 | 0.8170 | 0.8090 | 0.7198 | 1.0000 | 0.9551 | 0.6321 |
| point-odyssey-human | 8 | 1.1631 | 1.2079 | 0.6320 | 1.0000 | 0.9391 | 0.5720 |

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