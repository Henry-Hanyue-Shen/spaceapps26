"""Full (unthresholded) June clue fields and sample sea-height anomaly maps for the deck figures. Runs on the DGX.

Same method as ntr/explore_ssh_gibs.py (Spearman r between the linearly detrended monthly NASA MEaSUREs sea-surface
height in each 2-degree cell and the linearly detrended Oct-Apr count of high-water days), but every ocean cell is kept,
so the maps are continuous. Targets: New York (ntr/data_processed) and Los Angeles (ntr/westcoast/la/data_processed).
Writes fields.npz next to this script.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats as sp

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
g = np.load(ROOT / "ntr/data_processed/ssh_gibs_monthly.npz")
ssh, LAT, LON, months = g["ssh_m"].astype(float), g["lat"], g["lon"], list(g["months"])
idx = {m: k for k, m in enumerate(months)}
years = np.arange(1993, 2019)


def target(csv):
    t = pd.read_csv(csv, parse_dates=["date"], index_col="date").asfreq("MS")["surge_days"]
    y = np.array([t.loc[f"{v}-10":f"{v + 1}-04"].sum() if t.loc[f"{v}-10":f"{v + 1}-04"].count() >= 6 else np.nan for v in years])
    keep = np.isfinite(y); yrs = years[keep]
    return yrs, y[keep] - np.polyval(np.polyfit(yrs, y[keep], 1), yrs)


def field_r(yrs, yd, month=6):
    f = np.stack([ssh[idx[f"{v}-{month:02d}"]] for v in yrs])
    r = np.full(f.shape[1:], np.nan)
    for i in range(f.shape[1]):
        for j in range(f.shape[2]):
            x = f[:, i, j]; ok = np.isfinite(x)
            if ok.sum() < 20 or np.nanstd(x) == 0:
                continue
            xd = x[ok] - np.polyval(np.polyfit(yrs[ok].astype(float), x[ok], 1), yrs[ok])
            r[i, j] = sp.spearmanr(xd, yd[ok]).statistic
    return r


out = {"lat": LAT, "lon": LON}
for name, csv in [("ny", ROOT / "ntr/data_processed/ntr_monthly.csv"), ("la", ROOT / "ntr/westcoast/la/data_processed/ntr_monthly.csv")]:
    yrs, yd = target(csv)
    out[f"r_{name}"] = field_r(yrs, yd)
    n = len(yrs); tc = sp.t.ppf(0.975, n - 2)
    out[f"r05_{name}"] = tc / np.sqrt(n - 2 + tc ** 2)
    out[f"n_{name}"] = n
    print(name, n, "winters; max |r|", np.nanmax(np.abs(out[f"r_{name}"])).round(2))
for m in ["1997-11", "2015-06", "2015-11"]:
    out["ssh_" + m.replace("-", "_")] = ssh[idx[m]]
    print("ssh", m, "range", np.nanmin(ssh[idx[m]]).round(3), np.nanmax(ssh[idx[m]]).round(3), ssh.shape)
np.savez_compressed(OUT / "fields.npz", **out)
print("saved", sorted(out))
