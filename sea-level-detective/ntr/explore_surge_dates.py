"""List the largest surge days at the Battery since NASA true-colour imagery begins (2015-11-24), for the website presets.

Same definition as build_ntr.py: daily-mean NTR minus its 365-day centred running mean, threshold 0.30 m.
Writes results/surge_dates.json: the top days (date, surge in m), keeping at most one day per storm (7-day spacing).
"""
import json
import pandas as pd
from config_ntr import PROCESSED, RESULTS, SURGE_THRESHOLD_M

h = pd.read_csv(PROCESSED / "ntr_hourly.csv", parse_dates=["time"]).set_index("time")["ntr_m"]
ok = h.resample("D").count() >= 20
dm = h.resample("D").mean().where(ok)
surge = (dm - dm.rolling(365, center=True, min_periods=300).mean()).dropna()
recent = surge.loc["2015-11-24":].sort_values(ascending=False)
picked = []
for day, v in recent.items():
    if v <= SURGE_THRESHOLD_M:
        break
    if all(abs((day - p[0]).days) > 7 for p in picked):
        picked.append((day, float(v)))
    if len(picked) == 10:
        break
out = {"threshold_m": SURGE_THRESHOLD_M, "since": "2015-11-24",
       "top_days": [{"date": d.strftime("%Y-%m-%d"), "surge_m": round(v, 3)} for d, v in picked],
       "check_2016_01_23": float(surge.get(pd.Timestamp("2016-01-23"), float("nan"))),
       "n_surge_days_since": int((surge.loc["2015-11-24":] > SURGE_THRESHOLD_M).sum())}
(RESULTS / "surge_dates.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
