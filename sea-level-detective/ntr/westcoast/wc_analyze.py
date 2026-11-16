"""Does "the Pacific tells the winter ahead" (Battery: August ENSO -> Oct-Apr surge days) hold on the U.S. West Coast?

Same definitions and model as ntr/explore_analyze.py (functions imported from it, NY scripts untouched):
  daily-mean NTR (days with >= 20 hourly values); background = 365-day centred running mean (>= 300 days);
  months with < 80% of hours are NaN; season = Oct Y..Apr Y+1 with >= 6 valid months, start years 1980-2025;
  ENSO = NOAA ONI / NASA GISTEMP Nino3.4, train climatology + train trend removed, standardized (anomaly());
  quasi-Poisson GLM surge days ~ t + ENSO; train seasons 1981-2009, test 2010-2025; LOO skill vs trend-only.

Targets per station
  surge_030    days with daily-mean NTR > 0.30 m above its running mean (Sweet & Zervas; the Battery definition)
  surge_p98    same residual, threshold = its 98th percentile over train days 1981-2010 (station-relative)
  high_p98     days with daily-mean NTR above a FIXED baseline (train monthly climatology + train linear trend) by more
               than its train 98th percentile; unlike the running mean this keeps ENSO's months-long sea-level rise
  mean_ntr_cm  season mean of monthly mean NTR (cm), OLS ~ t + ENSO (effect in cm per SD)
The Battery row (surge_030 from ntr/data_processed/ntr_monthly.csv) is recomputed here as a check on the code.
"""
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from config_ntr import PROCESSED as NY_PROCESSED
from explore_analyze import (TRAIN, SEASON_TRAIN, SEASON_TEST, anomaly, in_period, season_eval, season_totals)

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
PROC, RES = HERE / "data_processed", HERE / "results"
STATIONS = {"san_francisco": "9414290", "los_angeles": "9410660", "la_jolla": "9410230", "seattle": "9447130"}
INDICES = {"oni": "NOAA ONI", "nino34_giss": "NASA GISTEMP Nino3.4"}
HEADLINE = {"oni": 8, "nino34_giss": 6}          # August ONI, June NASA Nino3.4 (as reported for New York)
FORECAST_MONTHS = range(1, 10)                   # Jan..Sep: known before the season starts


def station_monthly(st):
    h = pd.read_csv(PROC / f"{st}_hourly.csv", parse_dates=["time"]).set_index("time")["ntr_m"]
    hours = h.resample("MS").count()
    valid = hours >= 0.8 * hours.index.days_in_month * 24
    ok = h.resample("D").count() >= 20
    dm = h.resample("D").mean().where(ok)
    resid = dm - dm.rolling(365, center=True, min_periods=300).mean()
    tr = in_period(resid.index, TRAIN)
    p98 = float(resid[tr].quantile(0.98))
    # fixed baseline: train monthly climatology + train linear trend of the daily means
    dtr = dm[tr].dropna()
    clim = dtr.groupby(dtr.index.month).mean()
    a = dm - clim.reindex(dm.index.month).to_numpy()
    t = (a.index.year + (a.index.dayofyear - 1) / 365.25).to_numpy()
    okt = tr & a.notna().to_numpy()
    slope, icept = np.polyfit(t[okt], a.to_numpy()[okt], 1)
    fixed = a - (icept + slope * t)
    hp98 = float(fixed[tr].quantile(0.98))
    count = lambda mask: (mask & ok).resample("MS").sum().astype(float).where(valid)
    out = pd.DataFrame({"surge_030": count(resid > 0.30), "surge_p98": count(resid > p98), "high_p98": count(fixed > hp98),
                        "mean_ntr_cm": (h.resample("MS").mean() * 100).where(valid)})
    info = {"p98_resid_m": p98, "p98_fixed_m": hp98, "trend_mm_per_yr": slope * 1000,
            "valid_months": int(valid.sum()), "first": str(h.first_valid_index()), "last": str(h.last_valid_index()),
            "invalid_months_1980_2026": [f"{d:%Y-%m}" for d in valid.index[~valid] if d.year >= 1980]}
    return out, info


def season_means(m):
    rows = {}
    for y in range(1980, 2026):
        s = m.loc[f"{y}-10":f"{y + 1}-04"]
        rows[y] = s.mean() if s.count() >= 6 else np.nan
    return pd.Series(rows)


def ols_eval(df, xcols):
    df = df[["y", "t"] + xcols].dropna()
    tr, te = df.loc[SEASON_TRAIN[0]:SEASON_TRAIN[1]], df.loc[SEASON_TEST[0]:SEASON_TEST[1]]
    if len(tr) < 15 or len(te) < 6:
        return None
    X = lambda d, c: sm.add_constant(d[c], has_constant="add")
    f1, f0 = sm.OLS(tr.y, X(tr, ["t"] + xcols)).fit(), sm.OLS(tr.y, X(tr, ["t"])).fit()
    sse = lambda d, f, c: float(((d.y - f.predict(X(d, c))) ** 2).sum())
    out = {"n_train": len(tr), "n_test": len(te), "n_all": len(df),
           "test_skill": 1 - sse(te, f1, ["t"] + xcols) / sse(te, f0, ["t"])}
    l1 = l0 = 0.0
    for s in df.index:
        rest, one = df.drop(s), df.loc[[s]]
        l1 += sse(one, sm.OLS(rest.y, X(rest, ["t"] + xcols)).fit(), ["t"] + xcols)
        l0 += sse(one, sm.OLS(rest.y, X(rest, ["t"])).fit(), ["t"])
    out["loo_skill"] = 1 - l1 / l0
    fa = sm.OLS(df.y, X(df, ["t"] + xcols)).fit()
    ci = fa.conf_int().loc[xcols[0]]
    out.update(coef_all=float(fa.params[xcols[0]]), coef_all_ci=[float(ci[0]), float(ci[1])], p_all=float(fa.pvalues[xcols[0]]),
               r_partial=float(np.sign(fa.params[xcols[0]]) * np.sqrt(fa.tvalues[xcols[0]] ** 2 / (fa.tvalues[xcols[0]] ** 2 + fa.df_resid))))
    return out


def enso_at(preds, idx, m, years):
    return pd.Series({y: preds[idx].get(pd.Timestamp(y, m, 1), np.nan) for y in years})


def fmt_row(r, kind):
    if r is None:
        return "fit failed"
    if kind == "count":
        return (f"RR {r['rr_all']:.2f} [{r['rr_all_ci'][0]:.2f}, {r['rr_all_ci'][1]:.2f}], p {r['p_all']:.4f}, "
                f"test {r['test_skill']:+.3f}, LOO {r['loo_skill']:+.3f}")
    return (f"{r['coef_all']:+.2f} cm/SD [{r['coef_all_ci'][0]:+.2f}, {r['coef_all_ci'][1]:+.2f}], p {r['p_all']:.4f}, "
            f"test {r['test_skill']:+.3f}, LOO {r['loo_skill']:+.3f}")


def main():
    RES.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(NY_PROCESSED / "explore_monthly.csv", parse_dates=["date"], index_col="date").asfreq("MS")
    preds = {k: anomaly(raw[k]) for k in INDICES}
    ny = pd.read_csv(NY_PROCESSED / "ntr_monthly.csv", parse_dates=["date"], index_col="date").asfreq("MS")

    targets, info = {}, {}
    for name, st in STATIONS.items():
        m, i = station_monthly(st)
        info[name] = {"station": st, **i}
        for col in m.columns:
            targets[(name, col)] = m[col]
    targets[("the_battery_check", "surge_030")] = ny["surge_days"]

    seasons_tbl, results, curve = {}, [], []
    for (name, col), mser in targets.items():
        kind = "mean" if col == "mean_ntr_cm" else "count"
        y = season_means(mser) if kind == "mean" else season_totals(mser)
        seasons_tbl[f"{name}:{col}"] = y
        base = pd.DataFrame({"y": y})
        base["t"] = base.index - 2000
        ev = ols_eval if kind == "mean" else season_eval
        row = {"station": name, "target": col, "n_winters": int(y.count()), "mean": float(y.mean()), "sd": float(y.std()),
               "zero_winters": int((y == 0).sum()) if kind == "count" else None,
               "missing_winters": [int(s) for s in y.index[y.isna()]]}
        for idx in INDICES:
            lc = []
            for mo in range(1, 13):
                r = ev(base.assign(x=enso_at(preds, idx, mo, y.index)), ["x"])
                if r:
                    lc.append({"station": name, "target": col, "index": idx, "month": mo, **r})
            curve += lc
            row[f"{idx}_m{HEADLINE[idx]}"] = next((c for c in lc if c["month"] == HEADLINE[idx]), None)
            fc = [c for c in lc if c["month"] in FORECAST_MONTHS]
            if fc:
                b = max(fc, key=lambda c: c["loo_skill"])
                row[f"{idx}_best"] = {"month": b["month"], "loo_skill": b["loo_skill"], "test_skill": b["test_skill"],
                                      "p_all": b["p_all"], "effect": b.get("rr_all", b.get("coef_all"))}
        results.append(row)

    pd.DataFrame(seasons_tbl).assign(oni_aug=enso_at(preds, "oni", 8, range(1980, 2026)),
                                     nino34_giss_jun=enso_at(preds, "nino34_giss", 6, range(1980, 2026))
                                     ).to_csv(RES / "wc_seasons.csv", index_label="season_start_year")
    cdf = pd.DataFrame(curve)
    cdf.to_csv(RES / "wc_lead_curves.csv", index=False)
    (RES / "wc_results.json").write_text(json.dumps({"stations": info, "results": results}, indent=1,
                                                    default=lambda o: None if isinstance(o, float) and not np.isfinite(o) else float(o)))

    # figure: lead curves, surge_p98 RR (top) and mean NTR cm/SD (bottom), ONI vs NASA Nino3.4
    names = list(STATIONS)
    fig, axes = plt.subplots(2, len(names), figsize=(3.2 * len(names), 5.6), sharex=True)
    for j, name in enumerate(names):
        for i, (col, key, lab) in enumerate((("surge_p98", "rr_all", "RR per SD (p98 surge days)"),
                                             ("mean_ntr_cm", "coef_all", "cm per SD (season mean NTR)"))):
            ax = axes[i, j]
            for idx, colr in (("oni", "#2a78d6"), ("nino34_giss", "#eb6834")):
                c = cdf[(cdf.station == name) & (cdf.target == col) & (cdf["index"] == idx)]
                if not len(c):
                    continue
                lo, hi = c[f"{key}_ci"].str[0], c[f"{key}_ci"].str[1]
                ax.errorbar(c.month, c[key], yerr=[c[key] - lo, hi - c[key]], marker="o", ms=3, color=colr, capsize=2,
                            label=INDICES[idx])
            ax.axhline(1 if key == "rr_all" else 0, color="#898781", lw=0.8)
            ax.axvline(9.5, color="#898781", ls=":")
            ax.set_xticks(range(1, 13)); ax.set_xticklabels("J F M A M J J A S O N D".split(), fontsize=7)
            if j == 0:
                ax.set_ylabel(lab, fontsize=8)
            if i == 0:
                ax.set_title(f"{name} {STATIONS[name]}", fontsize=9)
    axes[0, 0].legend(fontsize=7, frameon=False)
    fig.suptitle("West Coast: ENSO read in month m of the start year -> Oct-Apr season (all winters, 95% CI)", fontsize=9)
    fig.tight_layout(); fig.savefig(RES / "wc_enso_lead_curve.png", dpi=150); plt.close(fig)

    # summary
    L = ["# West Coast check of 'the Pacific tells the winter ahead'", "",
         "Seasons Oct Y..Apr Y+1, start years 1980-2025, >= 6 valid months. Effects use all winters; test = fit 1981-2009, "
         "score 2010-2025; LOO = leave-one-winter-out; skill = 1 - deviance(or SSE)/trend-only. Best lead = month Jan..Sep "
         "with the highest LOO skill (picked from 9, so optimistic).", ""]
    for name, i in info.items():
        L.append(f"- {name} {i['station']}: {i['first'][:10]}..{i['last'][:10]}, {i['valid_months']} valid months, "
                 f"p98 residual {i['p98_resid_m']:.3f} m, p98 fixed-baseline {i['p98_fixed_m']:.3f} m, NTR trend {i['trend_mm_per_yr']:.2f} mm/yr; "
                 f"invalid months since 1980: {len(i['invalid_months_1980_2026'])}")
    L.append("")
    for r in results:
        kind = "mean" if r["target"] == "mean_ntr_cm" else "count"
        L.append(f"## {r['station']} / {r['target']}: n {r['n_winters']}, mean {r['mean']:.2f}, sd {r['sd']:.2f}"
                 + (f", zero winters {r['zero_winters']}" if kind == "count" else "")
                 + (f", missing {r['missing_winters']}" if r["missing_winters"] else ""))
        for idx in INDICES:
            L.append(f"- {INDICES[idx]} month {HEADLINE[idx]}: {fmt_row(r.get(f'{idx}_m{HEADLINE[idx]}'), kind)}")
            b = r.get(f"{idx}_best")
            if b:
                L.append(f"  best lead month {b['month']}: effect {b['effect']:.2f}, LOO {b['loo_skill']:+.3f}, test {b['test_skill']:+.3f}, p {b['p_all']:.4f}")
        L.append("")
    L += ["## Lead curves (all winters): station / target / index: month effect (p)"]
    for (name, col, idx), c in cdf.groupby(["station", "target", "index"], sort=False):
        key = "coef_all" if col == "mean_ntr_cm" else "rr_all"
        L.append(f"- {name} / {col} / {idx}: " + "  ".join(f"{int(m)}:{e:.2f}({p:.3f})" for m, e, p in zip(c.month, c[key], c.p_all)))
    (RES / "wc_summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
