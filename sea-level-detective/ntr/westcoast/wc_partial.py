"""Is the West Coast ENSO -> surge-day link storms, or just the El Nino sea-level hump that the 365-day running mean
does not fully remove? Refit surge days ~ t + ENSO(Aug ONI) + the same season's mean NTR (all winters).
If ENSO's rate ratio drops to ~1 once the season mean is in, the surge-day signal is mostly the raised mean level.
Reads results/wc_seasons.csv; writes results/wc_partial.md. Diagnostic only (season mean NTR is not known in advance).
"""
import numpy as np
import pandas as pd
from pathlib import Path
from explore_analyze import qp_fit

RES = Path(__file__).resolve().parent / "results"
s = pd.read_csv(RES / "wc_seasons.csv", index_col="season_start_year")
L = ["# Surge days ~ t + Aug ONI (+ season mean NTR, cm): ENSO rate ratio per SD", ""]
for st in ("san_francisco", "los_angeles", "la_jolla", "seattle"):
    for tgt in ("surge_030", "surge_p98"):
        d = pd.DataFrame({"y": s[f"{st}:{tgt}"], "x": s["oni_aug"], "m": s[f"{st}:mean_ntr_cm"]}).dropna()
        d["t"] = d.index - 2000
        if d.y.sum() < 10:
            continue
        f0, f1 = qp_fit(d, ["t", "x"]), qp_fit(d, ["t", "x", "m"])
        ci = np.exp(f1.conf_int().loc["x"])
        L.append(f"- {st} {tgt}: ENSO RR {np.exp(f0.params['x']):.2f} (p {f0.pvalues['x']:.4f}) -> with season mean "
                 f"{np.exp(f1.params['x']):.2f} [{ci[0]:.2f}, {ci[1]:.2f}] (p {f1.pvalues['x']:.3f}); "
                 f"RR per cm of season mean {np.exp(f1.params['m']):.3f} (p {f1.pvalues['m']:.4f})")
(RES / "wc_partial.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
