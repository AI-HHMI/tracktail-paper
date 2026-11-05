
import json, sys, os, re
import pandas as pd
REF_PD="/groups/karashchuk/home/karashchukl/results/paper-final-v2/posetail-outputs-vis0.1/paper_data"; NEW="/groups/karashchuk/home/karashchukl/results/paper-final-v2/posetail-outputs-vis0.1-occunknown"; FD="/groups/karashchuk/home/karashchukl/projects/posetail/posetail-next/scratch/figs_occunk"; PD=FD+"/paper_data"
sys.path.insert(0, "/groups/karashchuk/home/karashchukl/projects/posetail/posetail-next/scripts")
import compute_survival as cs
# 1. survival: replace the tracktail rows with the occunknown runs
ref = pd.read_csv(REF_PD + "/survival_curves.csv")
thrs = sorted(ref["threshold"].unique())
rows = []
for n in (4, 9):
    for dataset, (folder, prefix) in cs.DATASETS.items():
        cfg = dict(model=f"posetail-{n}cams", dataset=dataset, pattern=f"{NEW}/main_finetune_vzkjqrys_po_{n}cams/{folder}/{prefix}*_trial.npz")
        for thr in thrs:
            rows += [dict(r, threshold=thr) for r in cs.process_config(cfg, thr)]
new = pd.DataFrame(rows)
surv = pd.concat([ref[~ref["model"].str.startswith("posetail")], new], ignore_index=True)
surv.to_csv(PD + "/survival_curves.csv", index=False)
# 2. ncam: tracktail column from occunknown
nc = pd.read_csv(REF_PD + "/dexycb_ncam_results.csv")
s = pd.read_csv(NEW + "/ncam_ablation_dexycb/ncam_ablation_summary.csv").set_index("n_views")["avg_jaccard"]
nc["Tracktail"] = [round(s[n] * 100, 1) for n in nc["n_views"]]
nc.to_csv(PD + "/dexycb_ncam_results.csv", index=False)
print(nc)
# survival summary at 1.2
for (m, d), g in new[new.threshold == 1.2].groupby(["model", "dataset"]):
    g = g.set_index("frame")["survival_mean"]; print(m, d, "t25", round(g.get(25), 3), "last", round(g.iloc[-1], 3))
# 3. figures: run the notebook cells with the paths swapped
import matplotlib; matplotlib.use("Agg")
TP = "/groups/karashchuk/home/karashchukl/projects/posetail/tracktail-paper"
def cells(nb, idx):
    c = json.load(open(f"{TP}/{nb}"))["cells"]
    return ["".join(c[i]["source"]) for i in idx]
g = {}
for src in cells("format_arrow.ipynb", [0, 4, 5, 6]):
    src = src.replace("PAPER_DATA = '/groups/karashchuk/home/karashchukl/results/paper-final-v2/posetail-outputs-vis0.1/paper_data'", "PAPER_DATA = PD").replace("FIG_OUT = 'figures/arrow'", "FIG_OUT = FD")
    g.update(PD=PD, FD=FD); exec(src, g)
g = {}
for src in cells("figure_survival.ipynb", [0, 1, 2]):
    src = src.replace("data_path = '/groups/karashchuk/home/karashchukl/results/paper-final-v2/posetail-outputs-vis0.1/paper_data/survival_curves.csv'", "data_path = PD + '/survival_curves.csv'").replace("outpath = 'figures'", "outpath = FD")
    g.update(PD=PD, FD=FD); exec(src, g)
print(sorted(os.listdir(FD)))
