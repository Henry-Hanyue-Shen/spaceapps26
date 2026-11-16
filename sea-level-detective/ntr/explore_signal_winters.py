"""Every signal, every read-month, every winter: leave-one-winter-out predictions of surge days at the Battery.

For the "Test a winter" timeline on the site. Same data, anomalies and model as explore_analyze.py Part 4 (the ENSO
lead-time curve), applied to all 29 signals instead of the two ENSO indices:
    surge days in cool season Oct Y..Apr Y+1  ~  quasi-Poisson(log link) on  time + signal read in month m of year Y
for m = 1..12 (m = 10..12 falls inside the season, so it is not a forecast). Each winter is predicted by a model fitted
without that winter. The trend-only model (time alone) is the baseline.

Output: results/signal_winters.json
    seasons, observed, trend_loo                     one value per winter (1981..2025)
    signals[name][m] = {pred: [...], mae, closer, loo_skill, rr, p}   per read-month
This is exploratory: 29 signals x 12 months are compared, so the best month of a signal is picked from many tries;
only ENSO passed the held-out test in explore_analyze.py.
"""
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from config_ntr import PROCESSED, RESULTS, ensure_dirs
from explore_analyze import SEASON_TRAIN, SEASON_TEST, TRAIN, anomaly, in_period, qp_fit, poisson_dev, season_totals

warnings.filterwarnings("ignore")


def loo(df, cols):
    out = pd.Series(np.nan, index=df.index)
    for s in df.index:
        rest, one = df.drop(s), df.loc[[s]]
        out[s] = float(qp_fit(rest, cols).predict(sm.add_constant(one[cols], has_constant="add")).iloc[0])
    return out


def main():
    ensure_dirs()
    raw = pd.read_csv(PROCESSED / "explore_monthly.csv", parse_dates=["date"], index_col="date").asfreq("MS")
    tgt = pd.read_csv(PROCESSED / "ntr_monthly.csv", parse_dates=["date"], index_col="date").asfreq("MS")
    z = {}
    for k in ("iceland", "azores"):
        s = raw[f"slp_{k}_power"]
        tr = s[in_period(s.index, TRAIN)]
        g = tr.groupby(tr.index.month).agg(["mean", "std"])
        z[k] = (s - g["mean"].reindex(s.index.month).to_numpy()) / g["std"].reindex(s.index.month).to_numpy()
    raw["nao_power"] = z["azores"] - z["iceland"]
    raw = raw.drop(columns=["slp_iceland_power", "slp_azores_power"])
    preds = {c: a for c in raw.columns if (a := anomaly(raw[c])) is not None}

    seasons = pd.DataFrame({"y": season_totals(tgt["surge_days"])})
    seasons["t"] = seasons.index - 2000
    seasons = seasons.loc[SEASON_TRAIN[0]:SEASON_TEST[1]].dropna()
    years = list(seasons.index)
    trend = loo(seasons, ["t"])
    out = {"seasons": [int(y) for y in years], "observed": [float(v) for v in seasons.y],
           "trend_loo": [round(float(v), 2) for v in trend], "signals": {},
           "note": "leave-one-winter-out predictions; quasi-Poisson surge days ~ time + signal in read-month m; exploratory"}
    for name, x in preds.items():
        months = {}
        for m in range(1, 13):
            xs = pd.Series({y: x.get(pd.Timestamp(y, m, 1), np.nan) for y in years})
            d = seasons.assign(x=xs).dropna()
            if len(d) < 30:
                continue
            try:
                p = loo(d, ["t", "x"])
                fa = qp_fit(d, ["t", "x"])
            except Exception:
                continue
            obs, base = d.y, trend.reindex(d.index)
            em, et = (obs - p).abs(), (obs - base).abs()
            months[m] = {"pred": [round(float(p[y]), 2) if y in p.index else None for y in years],
                         "mae": round(float(em.mean()), 3), "mae_trend": round(float(et.mean()), 3),
                         "closer": int((em < et).sum()), "n": int(len(d)),
                         "loo_skill": round(1 - poisson_dev(obs, p) / poisson_dev(obs, base), 4),
                         "rr": round(float(np.exp(fa.params["x"])), 4), "p": float(fa.pvalues["x"])}
        if months:
            out["signals"][name] = months
        best = max(months.items(), key=lambda kv: kv[1]["loo_skill"]) if months else None
        if best:
            print(f"{name:28s} best month {best[0]:2d}  loo_skill {best[1]['loo_skill']:+.3f}  closer {best[1]['closer']}/{best[1]['n']}")
    (RESULTS / "signal_winters.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"wrote signal_winters.json: {len(out['signals'])} signals, {len(years)} winters")


if __name__ == "__main__":
    main()
