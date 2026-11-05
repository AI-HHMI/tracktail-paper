#!/usr/bin/env python
"""Draw the paper's line-plot figures from data/ into figures/.

    python build_figures.py [n_cams] [survival_comparison] [survival_tracktail]   (default: all three)

    n_cams_figure.pdf                 Fig. n_cams: DexYCB AJ vs number of views      <- data/dexycb_ncam_results.csv
    po_survival_comparison_1.2.pdf    suppl. Fig.: survival, 4 views, threshold 1.2  <- data/survival_curves.csv
    po_survival_tracktail.pdf         suppl. Fig.: Tracktail survival, 4 views, all thresholds

Both csv files are made by build_paper_data.py. Inputs from PAPER_DATA, outputs to FIG_OUT (see paths.py).
"""
import os
import sys

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

matplotlib.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
PALETTE = sns.color_palette('colorblind', n_colors=12)
COLORS = {'tracktail': PALETTE[2], 'cotracker': PALETTE[9], 'mvtracker': PALETTE[3], 'arrow': PALETTE[4]}


def save(fig, name):
    paths.FIG_OUT.mkdir(parents=True, exist_ok=True)
    out = paths.FIG_OUT / name
    fig.savefig(out, dpi=800, bbox_inches='tight')
    plt.close(fig)
    print(f'wrote {out}')


def n_cams():
    data = pd.read_csv(paths.PAPER_DATA / 'dexycb_ncam_results.csv')
    method_dict = {'Tracktail': 'Tracktail', 'CoTracker3 Baseline': 'CoTracker3 Baseline',
                   'MVTracker Baseline': 'MVTracker (DUST3R)', 'ARROW': 'ARROW'}
    method_order = list(method_dict)
    colors = [COLORS['tracktail'], COLORS['cotracker'], COLORS['mvtracker'], COLORS['arrow']]

    sns.set_style('ticks', {'font.family': 'STIXGeneral'})
    df = data.melt(id_vars='n_views', var_name='method', value_name='avg_jaccard')
    df['method'] = pd.Categorical(df['method'], categories=method_order, ordered=True)
    df = df.sort_values('method')

    fs = 17
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    sns.lineplot(data=df, x='n_views', y='avg_jaccard', hue='method', marker='o', markersize=7, palette=colors, ax=ax)
    ax.set_xlabel('Number of Views', fontsize=fs)
    ax.set_ylabel('Avg Jaccard (AJ)', fontsize=fs)
    ax.set_title('Performance on DexYCB', fontsize=fs)
    ax.set_xticks(sorted(df['n_views'].unique()))
    ax.tick_params(axis='both', labelsize=fs)
    ax.get_legend().remove()
    ax.grid(True, linestyle=':', color='k', linewidth=0.5, alpha=0.8)
    ax.set_ylim([0, 90])
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, [method_dict[m] for m in labels], loc='lower right',
              framealpha=0.7, facecolor='white', edgecolor='lightgray', fontsize=fs - 3)
    plt.tight_layout()
    sns.despine()
    save(fig, 'n_cams_figure.pdf')


def survival_comparison(thresh=1.2):
    data = pd.read_csv(paths.PAPER_DATA / 'survival_curves.csv')
    label_dict = {'tracktail-4cams': 'Tracktail', 'cotracker-4cams': 'CoTracker Baseline',
                  'mvtracker-4cams-duster': 'MVTracker', 'arrow-4cams': 'ARROW'}
    color_dict = dict(zip(label_dict, [COLORS['tracktail'], COLORS['cotracker'], COLORS['mvtracker'],
                                       COLORS['arrow']]))

    sns.set_style('ticks', {'font.family': 'STIXGeneral'})
    fs = 20
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    threshold_df = data[(data['threshold'] == thresh) & data['model'].isin(label_dict)]
    for i, (ax, dataset) in enumerate(zip(axs, ['human', 'animal'])):
        dataset_df = threshold_df[threshold_df['dataset'] == dataset]
        sns.lineplot(data=dataset_df, x='frame', y='survival_mean', hue='model', hue_order=list(label_dict),
                     linewidth=2, palette=color_dict, ax=ax)
        for model in label_dict:
            sub = dataset_df[dataset_df['model'] == model].sort_values('frame')
            ax.fill_between(sub['frame'], sub['survival_mean'] - sub['survival_std'],
                            sub['survival_mean'] + sub['survival_std'], color=color_dict[model], alpha=0.15,
                            linewidth=0)
        ax.set_xlabel('Frame', fontsize=fs)
        ax.set_ylabel('Survival Rate' if i == 0 else '', fontsize=fs)
        ax.set_title(f'Multiview Point Odyssey {dataset.capitalize()}', fontsize=fs)
        ax.tick_params(axis='both', labelsize=fs)
        ax.get_legend().remove()
        ax.grid(True, linestyle=':', color='k', linewidth=0.5, alpha=0.8)
        ax.set_xlim([0, 500])
        ax.set_ylim([0, 1])
    handles, labels = axs[-1].get_legend_handles_labels()
    fig.legend(handles, [label_dict[lab] for lab in labels], loc='upper center', bbox_to_anchor=(0.365, 0.92),
               framealpha=0.7, facecolor='white', edgecolor='lightgray', fontsize=fs - 2)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.15)
    sns.despine()
    save(fig, f'po_survival_comparison_{thresh}.pdf')


def survival_tracktail():
    data = pd.read_csv(paths.PAPER_DATA / 'survival_curves.csv')
    sns.set_style('ticks', {'font.family': 'STIXGeneral'})
    fs = 20
    fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    palette = sns.color_palette('rainbow', n_colors=6)
    tracktail_df = data[data['model'] == 'tracktail-4cams']
    for i, (ax, dataset) in enumerate(zip(axs, ['human', 'animal'])):
        sub_df = tracktail_df[tracktail_df['dataset'] == dataset]
        sns.lineplot(data=sub_df, x='frame', y='survival_mean', hue='threshold', linewidth=2, palette=palette, ax=ax)
        for thr, color in zip(sub_df['threshold'].unique(), palette):
            thresh_df = sub_df[sub_df['threshold'] == thr].sort_values('frame')
            ax.fill_between(thresh_df['frame'], thresh_df['survival_mean'] - thresh_df['survival_std'],
                            thresh_df['survival_mean'] + thresh_df['survival_std'], color=color, alpha=0.15,
                            linewidth=0)
        ax.set_xlabel('Frame', fontsize=fs)
        ax.set_ylabel('Survival Rate' if i == 0 else '', fontsize=fs)
        ax.set_title(f'Multiview Point Odyssey {dataset.capitalize()}', fontsize=fs)
        ax.tick_params(axis='both', labelsize=fs)
        ax.get_legend().remove()
        ax.grid(True, linestyle=':', color='k', linewidth=0.5, alpha=0.8)
        ax.set_ylim([-0.02, 1.02])
    handles, labels = axs[-1].get_legend_handles_labels()
    fig.legend(handles, labels, title='Distance Threshold', title_fontsize=fs - 1, loc='upper center',
               bbox_to_anchor=(1.07, 0.73), frameon=False, fontsize=fs - 1)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1)
    sns.despine()
    save(fig, 'po_survival_tracktail.pdf')


FIGURES = {'n_cams': n_cams, 'survival_comparison': survival_comparison, 'survival_tracktail': survival_tracktail}

if __name__ == '__main__':
    if any(a in ('-h', '--help') for a in sys.argv[1:]):
        print(__doc__)
        sys.exit(0)
    names = sys.argv[1:] or list(FIGURES)
    for name in names:
        if name not in FIGURES:
            sys.exit(f'unknown figure {name!r}; choose from {list(FIGURES)}')
        FIGURES[name]()
