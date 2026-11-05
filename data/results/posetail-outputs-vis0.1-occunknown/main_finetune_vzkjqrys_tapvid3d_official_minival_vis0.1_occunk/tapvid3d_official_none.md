# TAPVid-3D official metrics (camera coordinates)

compute_tapvid3d_metrics (depth-adaptive 1-16 px thresholds, scaling=none, all frames, visibility threshold 0.1), mean over trials. Trials: all predictions. Paper: ARROW arXiv 2610.01314 Table 2 (mini-val, no GT intrinsics).

| dataset | #tr | AJ | APD | OA | paper ARROW AJ / APD / OA | paper D4RT AJ / APD / OA |
|---|---|---|---|---|---|---|
| tapvid3d_drivetrack | 50 | 0.076 | 0.134 | 0.797 | 0.241 / 0.350 / 0.816 | 0.257 / 0.345 / 0.875 |
| tapvid3d_adt | 49 | 0.097 | 0.181 | 0.740 | 0.360 / 0.473 / 0.902 | 0.240 / 0.319 / 0.926 |
| tapvid3d_pstudio | 50 | 0.247 | 0.389 | 0.797 | 0.141 / 0.201 / 0.870 | 0.138 / 0.186 / 0.897 |
| avg |  | 0.140 | 0.235 | 0.778 | 0.248 / 0.341 / 0.863 | 0.212 / 0.283 / 0.899 |
