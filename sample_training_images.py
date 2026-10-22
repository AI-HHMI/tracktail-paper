#!/usr/bin/env python3
"""
Sample 10 random frames per trial from both Point Odyssey training datasets
and copy them to a browsable output directory.

Output layout:
  {output_prefix}/{dataset}/{trial}/{frame_filename}
"""

import os
import shutil
import random

DATASETS = {
    'point-odyssey-human': '/groups/karashchuk/karashchuklab/animal-datasets-processed/posetail-pretraining-v6/point-odyssey-human/train',
    'po-animal-sub256-motion': '/groups/karashchuk/karashchuklab/animal-datasets-processed/posetail-pretraining-v6/po-animal-sub256-motion/train',
}

OUTPUT_PREFIX = '/home/ruppk2@hhmi.org/tracktail-paper/training_samples'
VIEW = 'view0'
N_FRAMES = 10
SEED = 42

random.seed(SEED)

for dataset_name, train_dir in DATASETS.items():
    try:
        trials = sorted(os.listdir(train_dir))
    except PermissionError as e:
        print(f"Cannot list {train_dir}: {e}")
        continue

    print(f"\n=== {dataset_name} ({len(trials)} trials) ===")

    for trial in trials:
        img_dir = os.path.join(train_dir, trial, 'trial', 'img', VIEW)
        if not os.path.isdir(img_dir):
            print(f"  [{trial}] skipped — no image dir at {img_dir}")
            continue

        frames = sorted(f for f in os.listdir(img_dir) if f.endswith('.jpg'))
        if not frames:
            print(f"  [{trial}] skipped — no .jpg frames in {img_dir}")
            continue

        sampled = random.sample(frames, min(N_FRAMES, len(frames)))
        sampled.sort()

        out_dir = os.path.join(OUTPUT_PREFIX, dataset_name, trial)
        os.makedirs(out_dir, exist_ok=True)

        for frame_file in sampled:
            src = os.path.join(img_dir, frame_file)
            dst = os.path.join(out_dir, frame_file)
            shutil.copy2(src, dst)

        print(f"  [{trial}] saved {len(sampled)} frames")

print("\nDone.")
