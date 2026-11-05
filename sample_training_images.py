#!/usr/bin/env python3
"""
Browsing helper (not used for any paper figure): sample 10 random frames per trial from both Point Odyssey training
datasets and copy them to a browsable output directory, e.g. to pick examples for figure_po_examples.ipynb.

    TRACKTAIL_DATA=/path/to/processed/datasets python sample_training_images.py [OUTPUT_DIR]   (default: training_samples/)

Output layout:
  {output_prefix}/{dataset}/{trial}/{frame_filename}
"""

import os
import random
import shutil
import sys

import paths

TRACKTAIL_DATA = paths.require(paths.TRACKTAIL_DATA, 'TRACKTAIL_DATA')
DATASETS = {
    'point-odyssey-human': os.path.join(TRACKTAIL_DATA, 'point-odyssey-human', 'train'),
    'po-animal-sub256-motion': os.path.join(TRACKTAIL_DATA, 'po-animal-sub256-motion', 'train'),
}

OUTPUT_PREFIX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(paths.REPO, 'training_samples')
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
