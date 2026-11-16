"""Exploration: which global signals LEAD New York Harbor's non-tidal residual (NTR), and by how long?

Fixed before running (differs from model.py only in the split, because records now start in 1981):
  TRAIN 1981-01..2010-12, TEST 2011-01..latest. Seasons (Oct Y..Apr Y+1): train start years 1981-2009, test 2010-2025.
Every predictor: train monthly climatology and train linear trend removed, standardized by train SD.

Part 1  Monthly screening. Targets: (a) monthly mean NTR anomaly, (b) the same in cool months only, (c) monthly
        surge-day anomaly in cool months. For each predictor and each lead of 1..12 months: prewhitened
        cross-correlation on TRAIN (AR(1) filter of the predictor applied to both series). Benjamini-Hochberg FDR 10%
        over all predictor x lead tests per target. Lag 0 is reported for reference, not tested.
Part 2  Confirmation on TEST for every discovery: same-sign prewhitened correlation (one-sided 5%), OLS skill vs
        climatology, and the skill gained over persistence (NTR of the previous month).
Part 3  Season-ahead screening: Oct-Apr surge days ~ time + predictor averaged over Jul-Sep (known by 1 October).
        Quasi-Poisson; train rate ratio and p; FDR 10%; TEST deviance skill vs trend-only; leave-one-season-out skill.
Part 4  ENSO lead-time curve: rate ratio when ENSO is taken from each month Jan..Dec of the season's start year.
Part 5  Which cool-season month responds to August ENSO.
Part 6  Other East Coast gauges: August ENSO -> seasonal surge days, same definition.
"""
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config_ntr import PROCESSED, RESULTS, FIGURES, COOL_MONTHS, ensure_dirs

warnings.filterwarnings("ignore")
TRAIN, TEST = ("1981-01-01", "2010-12-31"), ("2011-01-01", "2026-12-31")
SEASON_TRAIN, SEASON_TEST = (1981, 2009), (2010, 2025)
LEADS = list(range(1, 13))
FDR_Q = 0.10


def in_period(index, period):
    return (index >= pd.Timestamp(period[0])) & (index <= pd.Timestamp(period[1]))


def anomaly(s, standardize=True):
    """Remove TRAIN monthly climatology and TRAIN linear trend; optionally standardize by TRAIN SD."""
    s = s.asfreq("MS")
    tr = s[in_period(s.index, TRAIN)]
    a = s - tr.groupby(tr.index.month).mean().reindex(s.index.month).to_numpy()
    t = (a.index.year + (a.index.month - 1) / 12).to_numpy()
    ok = in_period(a.index, TRAIN) & a.notna().to_numpy()
    if ok.sum() < 60:
        return None
    slope, icept = np.polyfit(t[ok], a.to_numpy()[ok], 1)
    a = a - (icept + slope * t)
    return a / a[in_period(a.index, TRAIN)].std() if standardize else a


def bh(pvals, q):
    """Benjamini-Hochberg: boolean array of discoveries."""
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    thresh = q * (np.arange(1, len(p) + 1)) / len(p)
    passed = p[order] <= thresh
    k = np.max(np.nonzero(passed)[0]) + 1 if passed.any() else 0
    out = np.zeros(len(p), bool)
    out[order[:k]] = True
    return out


def prewhitened_r(x, y, lag, period, a):
    xw, yw = x - a * x.shift(1), y - a * y.shift(1)
    pair = pd.concat([xw.shift(lag), yw], axis=1).dropna()
    pair = pair[in_period(pair.index, period)]
    n = len(pair)
    if n < 30:
        return np.nan, n
    return float(np.corrcoef(pair.iloc[:, 0], pair.iloc[:, 1])[0, 1]), n


def ols_skill(y, feats):
    df = pd.concat([y.rename("y"), feats], axis=1).dropna()
    tr, te = df[in_period(df.index, TRAIN)], df[in_period(df.index, TEST)]
    if len(tr) < 60 or len(te) < 24:
        return np.nan
    fit = sm.OLS(tr["y"], sm.add_constant(tr.drop(columns="y"))).fit()
    pred = fit.predict(sm.add_constant(te.drop(columns="y"), has_constant="add"))
    return float(1 - ((te["y"] - pred) ** 2).sum() / (te["y"] ** 2).sum())


def screen(y, preds, label):
    rows = []
    for name, x in preds.items():
        xt = x[in_period(x.index, TRAIN)].dropna()
        if len(xt) < 120:
            continue
        a = float(np.corrcoef(xt.to_numpy()[1:], xt.to_numpy()[:-1])[0, 1])
        for lag in [0] + LEADS:
            r, n = prewhitened_r(x, y, lag, TRAIN, a)
            p = float(2 * sp.norm.sf(abs(r) * np.sqrt(n))) if np.isfinite(r) else np.nan
            rows.append({"target": label, "predictor": name, "lead": lag, "r_train": r, "n_train": n, "p_train": p, "ar1": a})
    df = pd.DataFrame(rows)
    tested = (df.lead >= 1) & df.p_train.notna()
    df["discovery"] = False
    df.loc[tested, "discovery"] = bh(df.loc[tested, "p_train"], FDR_Q)
    persist = y.shift(1).rename("persistence")
    base = ols_skill(y, persist.to_frame())
    conf = []
    for i, row in df[df.discovery].iterrows():
        x = preds[row.predictor]
        r, n = prewhitened_r(x, y, int(row.lead), TEST, row.ar1)
        p1 = float(sp.norm.sf(np.sign(row.r_train) * r * np.sqrt(n))) if np.isfinite(r) else np.nan
        feat = x.shift(int(row.lead)).rename("x")
        alone = ols_skill(y, feat.to_frame())
        both = ols_skill(y, pd.concat([feat, persist], axis=1))
        base_same = ols_skill(y.where(feat.notna()), persist.to_frame())   # persistence on the same months
        conf.append({**row.to_dict(), "r_test": r, "n_test": n, "p_test_one_sided": p1, "skill_alone": alone,
                     "gain_over_persistence": both - base_same,
                     "confirmed": bool(np.isfinite(r) and np.sign(r) == np.sign(row.r_train) and p1 < 0.05)})
    return df, pd.DataFrame(conf), base


# ------------------------------------------------------------------ seasons
def poisson_dev(y, mu):
    y, mu = np.asarray(y, float), np.asarray(mu, float)
    return float(2 * np.sum(np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / mu), 0) - (y - mu)))


def qp_fit(df, cols):
    return sm.GLM(df["y"], sm.add_constant(df[cols], has_constant="add"), family=sm.families.Poisson()).fit(scale="X2")


def season_eval(df, xcols):
    """df: index start_year, columns y, t, predictors. Returns train RR/p of the first predictor, test skill, LOO skill."""
    df = df[["y", "t"] + xcols].dropna()
    tr, te = df.loc[SEASON_TRAIN[0]:SEASON_TRAIN[1]], df.loc[SEASON_TEST[0]:SEASON_TEST[1]]
    out = {"n_train": len(tr), "n_test": len(te), "n_all": len(df)}
    if len(tr) < 15 or len(te) < 6:
        return None
    try:
        f, b = qp_fit(tr, ["t"] + xcols), qp_fit(tr, ["t"])
        ci = f.conf_int().loc[xcols[0]]
        out.update(rr_train=float(np.exp(f.params[xcols[0]])), rr_ci=[float(np.exp(ci[0])), float(np.exp(ci[1]))], p_train=float(f.pvalues[xcols[0]]))
        d1 = poisson_dev(te["y"], f.predict(sm.add_constant(te[["t"] + xcols], has_constant="add")))
        d0 = poisson_dev(te["y"], b.predict(sm.add_constant(te[["t"]], has_constant="add")))
        out["test_skill"] = 1 - d1 / d0
        l1 = l0 = 0.0
        for s in df.index:
            rest, one = df.drop(s), df.loc[[s]]
            l1 += poisson_dev(one["y"], qp_fit(rest, ["t"] + xcols).predict(sm.add_constant(one[["t"] + xcols], has_constant="add")))
            l0 += poisson_dev(one["y"], qp_fit(rest, ["t"]).predict(sm.add_constant(one[["t"]], has_constant="add")))
        out["loo_skill"] = 1 - l1 / l0
        fa = qp_fit(df, ["t"] + xcols)
        cia = fa.conf_int().loc[xcols[0]]
        out.update(rr_all=float(np.exp(fa.params[xcols[0]])), rr_all_ci=[float(np.exp(cia[0])), float(np.exp(cia[1]))], p_all=float(fa.pvalues[xcols[0]]))
    except Exception as exc:  # separation or non-convergence
        out["error"] = str(exc)[:80]
        return None
    return out


def season_totals(counts):
    rows = {}
    for y in range(1980, 2026):
        s = counts.loc[f"{y}-10":f"{y + 1}-04"]
        rows[y] = s.sum() if s.count() >= 6 else np.nan
    return pd.Series(rows)


def main():
    ensure_dirs()
    raw = pd.read_csv(PROCESSED / "explore_monthly.csv", parse_dates=["date"], index_col="date").asfreq("MS")
    sources = json.loads((PROCESSED / "explore_sources.json").read_text())
    tgt = pd.read_csv(PROCESSED / "ntr_monthly.csv", parse_dates=["date"], index_col="date").asfreq("MS")

    # NASA NAO from POWER SLP (station-style), then drop the two raw pressures
    z = {}
    for k in ("iceland", "azores"):
        s = raw[f"slp_{k}_power"]
        tr = s[in_period(s.index, TRAIN)]
        g = tr.groupby(tr.index.month).agg(["mean", "std"])
        z[k] = (s - g["mean"].reindex(s.index.month).to_numpy()) / g["std"].reindex(s.index.month).to_numpy()
    raw["nao_power"] = z["azores"] - z["iceland"]
    sources["nao_power"] = {"source": "NASA POWER (MERRA-2) SLP: z(Azores) - z(Iceland)", "nasa": True}
    raw = raw.drop(columns=["slp_iceland_power", "slp_azores_power"])
    preds = {c: a for c in raw.columns if (a := anomaly(raw[c])) is not None}

    y_mean = anomaly(tgt["ntr_mean_mm"], standardize=False)
    cool = y_mean.index.month.isin(COOL_MONTHS)
    surge = tgt["surge_days"]
    tr_s = surge[in_period(surge.index, TRAIN)]
    y_surge = (surge - tr_s.groupby(tr_s.index.month).mean().reindex(surge.index.month).to_numpy()).where(cool)
    targets = {"mean NTR, all months": y_mean, "mean NTR, cool months": y_mean.where(cool), "surge days, cool months": y_surge}

    out = {"train": TRAIN, "test": TEST, "fdr_q": FDR_Q, "n_predictors": len(preds), "sources": sources, "monthly": {}}
    all_screen = []
    for label, y in targets.items():
        df, conf, base = screen(y, preds, label)
        all_screen.append(df)
        out["monthly"][label] = {
            "tests": int((df.lead >= 1).sum()), "discoveries": int(df.discovery.sum()), "persistence_skill": base,
            "lag0": df[df.lead == 0].set_index("predictor")["r_train"].round(3).to_dict(),
            "confirmed": conf[conf.confirmed].to_dict("records") if len(conf) else [],
            "discovered_not_confirmed": conf[~conf.confirmed][["predictor", "lead", "r_train", "r_test"]].to_dict("records") if len(conf) else []}
    screen_df = pd.concat(all_screen)
    screen_df.to_csv(RESULTS / "explore_screen.csv", index=False)

    # ---------------- Part 3: season-ahead
    seasons = pd.DataFrame({"y": season_totals(surge)})
    seasons["t"] = seasons.index - 2000
    jas = {}
    for name, x in preds.items():
        v = {yv: x.loc[f"{yv}-07":f"{yv}-09"].mean() if x.loc[f"{yv}-07":f"{yv}-09"].count() >= 2 else np.nan for yv in seasons.index}
        jas[name] = pd.Series(v)
    jas["previous_season_surge"] = ((seasons["y"] - seasons["y"].loc[SEASON_TRAIN[0]:SEASON_TRAIN[1]].mean()) / seasons["y"].loc[SEASON_TRAIN[0]:SEASON_TRAIN[1]].std()).shift(1)
    jas["battery_ntr_summer"] = pd.Series({yv: (y_mean.loc[f"{yv}-07":f"{yv}-09"].mean()) for yv in seasons.index})
    jas["battery_ntr_summer"] = jas["battery_ntr_summer"] / jas["battery_ntr_summer"].loc[SEASON_TRAIN[0]:SEASON_TRAIN[1]].std()
    srows = []
    for name, x in jas.items():
        r = season_eval(seasons.assign(x=x), ["x"])
        if r:
            srows.append({"predictor": name, **r})
    sdf = pd.DataFrame(srows)
    sdf["discovery"] = bh(sdf["p_train"], FDR_Q)
    sdf["confirmed"] = sdf.discovery & (sdf.test_skill > 0) & (sdf.loo_skill > 0)
    sdf = sdf.sort_values("loo_skill", ascending=False)
    sdf.to_csv(RESULTS / "explore_season.csv", index=False)
    out["season"] = {"n_candidates": len(sdf), "table": sdf.to_dict("records")}
    # does any second predictor add to ENSO?
    combos = []
    for name in sdf.predictor:
        if name in ("oni", "nino34_giss"):
            continue
        d = seasons.assign(enso=jas["oni"], x=jas[name])
        both, alone = season_eval(d, ["x", "enso"]), season_eval(d.dropna(subset=["x"]), ["enso"])
        if both and alone:
            combos.append({"added": name, "loo_enso_only": alone["loo_skill"], "loo_with": both["loo_skill"],
                           "test_enso_only": alone["test_skill"], "test_with": both["test_skill"],
                           "rr_added_all": both["rr_all"], "p_added_all": both["p_all"]})
    cdf = pd.DataFrame(combos)
    cdf["loo_gain"] = cdf.loo_with - cdf.loo_enso_only
    cdf["test_gain"] = cdf.test_with - cdf.test_enso_only
    out["season"]["added_to_enso"] = cdf.sort_values("loo_gain", ascending=False).to_dict("records")

    # ---------------- Part 4: ENSO lead-time curve (which month already knows)
    curve = []
    for idx_name in ("oni", "nino34_giss"):
        for m in range(1, 13):
            x = pd.Series({yv: preds[idx_name].get(pd.Timestamp(yv, m, 1), np.nan) for yv in seasons.index})
            r = season_eval(seasons.assign(x=x), ["x"])
            if r:
                curve.append({"index": idx_name, "month": m, "months_before_october": 10 - m, **r})
    out["enso_lead_curve"] = curve

    # Outlook for the 2026-27 season from each lead month (expected count, 95% CI of the mean, extrapolation flag)
    outlook = []
    for idx_name in ("oni", "nino34_giss"):
        for m in range(5, 10):
            x = pd.Series({yv: preds[idx_name].get(pd.Timestamp(yv, m, 1), np.nan) for yv in seasons.index})
            d = seasons.assign(x=x).dropna()
            x26 = preds[idx_name].get(pd.Timestamp(2026, m, 1), np.nan)
            if not np.isfinite(x26) or len(d) < 20:
                continue
            f, b = qp_fit(d, ["t", "x"]), qp_fit(d, ["t"])
            new = pd.DataFrame({"const": [1.0], "t": [26], "x": [x26]})
            pf = f.get_prediction(new).summary_frame(alpha=0.05)
            outlook.append({"index": idx_name, "month": m, "value_sd": float(x26), "observed_max_sd": float(d.x.max()),
                            "extrapolation": bool(x26 > d.x.max()), "expected": float(pf["mean"].iloc[0]),
                            "ci": [float(pf["mean_ci_lower"].iloc[0]), float(pf["mean_ci_upper"].iloc[0])],
                            "trend_only": float(b.get_prediction(new[["const", "t"]]).summary_frame()["mean"].iloc[0])})
    out["outlook_2026"] = outlook

    # ---------------- Part 5: which calendar month responds
    aug = pd.Series({yv: preds["oni"].get(pd.Timestamp(yv, 8, 1), np.nan) for yv in range(1980, 2026)})
    resp = []
    for c in (10, 11, 12, 1, 2, 3, 4):
        d = pd.DataFrame({"y": {yv: surge.get(pd.Timestamp(yv if c >= 10 else yv + 1, c, 1), np.nan) for yv in range(1981, 2026)}})
        d["t"], d["x"] = d.index - 2000, aug.reindex(d.index)
        d = d.dropna()
        try:
            f = qp_fit(d, ["t", "x"])
            ci = f.conf_int().loc["x"]
            resp.append({"month": c, "rr": float(np.exp(f.params["x"])), "ci": [float(np.exp(ci[0])), float(np.exp(ci[1]))],
                         "p": float(f.pvalues["x"]), "mean_days": float(d.y.mean()), "n": len(d)})
        except Exception:
            pass
    out["response_by_month"] = resp

    # ---------------- Part 6: other gauges
    other_path = PROCESSED / "explore_surge_days.csv"
    other = (pd.read_csv(other_path, parse_dates=["date"], index_col="date").asfreq("MS") if other_path.exists()
             else pd.DataFrame(index=surge.index))   # other gauges are still downloading on the first run
    other["the_battery"] = surge
    gauges = []
    for st in other.columns:
        d = pd.DataFrame({"y": season_totals(other[st])})
        d["t"], d["x"] = d.index - 2000, aug.reindex(d.index)
        r = season_eval(d, ["x"])
        if r:
            gauges.append({"gauge": st, "mean_days": float(d.y.mean()), **r})
    out["other_gauges"] = gauges

    # ---------------- figures
    p1 = screen_df[screen_df.target == "mean NTR, all months"].pivot(index="predictor", columns="lead", values="r_train")
    d1 = screen_df[screen_df.target == "mean NTR, all months"].pivot(index="predictor", columns="lead", values="discovery")
    fig, ax = plt.subplots(figsize=(9, 0.32 * len(p1) + 1.5))
    im = ax.imshow(p1.to_numpy(), cmap="RdBu_r", vmin=-0.5, vmax=0.5, aspect="auto")
    ax.set_xticks(range(p1.shape[1])); ax.set_xticklabels(p1.columns); ax.set_yticks(range(len(p1))); ax.set_yticklabels(p1.index, fontsize=7)
    for i in range(d1.shape[0]):
        for j in range(d1.shape[1]):
            if d1.to_numpy()[i, j] is True or d1.to_numpy()[i, j] == True:
                ax.plot(j, i, "k.", ms=5)
    ax.set_xlabel("lead (months; 0 = same month, not tested)"); ax.set_title("Prewhitened correlation with Battery monthly mean NTR (train 1981-2010); dots = FDR 10%", fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.7); fig.tight_layout(); fig.savefig(FIGURES / "explore_lag_heatmap.png", dpi=150); plt.close(fig)

    c = pd.DataFrame(curve)
    if len(c):
        fig, ax = plt.subplots(figsize=(7, 3.2))
        for idx_name, col in (("oni", "#2a78d6"), ("nino34_giss", "#eb6834")):
            cc = c[c["index"] == idx_name]
            ax.errorbar(cc.month, cc.rr_all, yerr=[cc.rr_all - cc.rr_all_ci.str[0], cc.rr_all_ci.str[1] - cc.rr_all], marker="o", color=col, capsize=2,
                        label="NOAA ONI" if idx_name == "oni" else "NASA GISTEMP Nino3.4")
        ax.axhline(1, color="#898781", lw=0.8); ax.axvline(9.5, color="#898781", ls=":"); ax.set_xticks(range(1, 13))
        ax.set_xticklabels("J F M A M J J A S O N D".split()); ax.set_ylabel("rate ratio per SD"); ax.legend(fontsize=8, frameon=False)
        ax.set_title("How early does ENSO know the coming Oct-Apr surge season? (month of the start year)", fontsize=9)
        fig.tight_layout(); fig.savefig(FIGURES / "explore_enso_lead_curve.png", dpi=150); plt.close(fig)

    (RESULTS / "explore.json").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float) and not np.isfinite(o) else float(o)))

    # ---------------- summary
    L = [f"# NTR exploration: The Battery. Train {TRAIN[0][:7]}..{TRAIN[1][:7]}, test {TEST[0][:7]}.., {len(preds)} predictors, FDR {FDR_Q:.0%}", ""]
    for label, m in out["monthly"].items():
        L += [f"## Monthly: {label}", f"{m['tests']} predictor x lead tests; {m['discoveries']} discoveries on train; persistence skill {m['persistence_skill']:.3f}"]
        top0 = sorted(m["lag0"].items(), key=lambda kv: -abs(kv[1] if kv[1] == kv[1] else 0))[:6]
        L.append("Same-month (lag 0, reference): " + ", ".join(f"{k} {v:+.2f}" for k, v in top0))
        for cfm in m["confirmed"]:
            L.append(f"- CONFIRMED {cfm['predictor']} leads by {int(cfm['lead'])} mo: r_train {cfm['r_train']:+.2f}, r_test {cfm['r_test']:+.2f} "
                     f"(p {cfm['p_test_one_sided']:.3f}), skill alone {cfm['skill_alone']:.3f}, gain over persistence {cfm['gain_over_persistence']:+.3f}")
        if m["discovered_not_confirmed"]:
            L.append("- discovered on train but NOT confirmed on test: " + ", ".join(f"{d['predictor']}@{int(d['lead'])}" for d in m["discovered_not_confirmed"]))
        L.append("")
    L += ["## Season-ahead: Jul-Sep predictor -> Oct-Apr surge days (quasi-Poisson + trend)",
          "| predictor | RR/SD train | p train | FDR | test skill | LOO skill | RR/SD all | p all |", "|---|---:|---:|:-:|---:|---:|---:|---:|"]
    for r in out["season"]["table"]:
        L.append(f"| {r['predictor']} | {r['rr_train']:.2f} | {r['p_train']:.3f} | {'yes' if r['discovery'] else ''} | {r['test_skill']:+.3f} | "
                 f"{r['loo_skill']:+.3f} | {r['rr_all']:.2f} | {r['p_all']:.4f} |")
    L += ["", "Added to ENSO (LOO gain, test gain): " + "; ".join(f"{r['added']} {r['loo_gain']:+.3f}/{r['test_gain']:+.3f}" for r in out["season"]["added_to_enso"][:8]), "",
          "## ENSO lead-time curve (all seasons): month -> RR/SD [CI], p, LOO skill"]
    for r in curve:
        L.append(f"- {r['index']} month {r['month']:>2} ({r['months_before_october']:+d} mo before Oct): RR {r['rr_all']:.2f} "
                 f"[{r['rr_all_ci'][0]:.2f}, {r['rr_all_ci'][1]:.2f}], p {r['p_all']:.4f}, LOO {r['loo_skill']:+.3f}")
    L += ["", "## Outlook 2026-27 by lead month (expected Oct-Apr surge days [95% CI of the mean]; * = beyond the observed range)"]
    for r in outlook:
        L.append(f"- {r['index']} month {r['month']}: {r['value_sd']:+.2f} SD (max seen {r['observed_max_sd']:+.2f}){'*' if r['extrapolation'] else ''} "
                 f"-> {r['expected']:.1f} [{r['ci'][0]:.1f}, {r['ci'][1]:.1f}] vs trend-only {r['trend_only']:.1f}")
    L += ["", "## Response by calendar month (August ONI -> surge days in that month)"]
    for r in resp:
        L.append(f"- month {r['month']:>2}: RR {r['rr']:.2f} [{r['ci'][0]:.2f}, {r['ci'][1]:.2f}], p {r['p']:.3f}, mean {r['mean_days']:.1f} days")
    L += ["", "## Other gauges (August ONI -> Oct-Apr surge days)"]
    for r in gauges:
        L.append(f"- {r['gauge']}: RR {r['rr_all']:.2f} [{r['rr_all_ci'][0]:.2f}, {r['rr_all_ci'][1]:.2f}], p {r['p_all']:.4f}, LOO {r['loo_skill']:+.3f}, "
                 f"test {r['test_skill']:+.3f}, mean {r['mean_days']:.1f} days, n {r['n_all']}")
    (RESULTS / "explore_summary.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
