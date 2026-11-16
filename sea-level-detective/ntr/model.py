"""How long do global signals take to change NY Harbor's non-tidal residual (NTR), and do they help predict it?

Targets (monthly, The Battery):
  A. monthly mean NTR anomaly (mm): seasonal climatology and linear trend fitted on TRAIN only, then removed everywhere
  B. surge days per cool-season month (daily max NTR > 0.30 m), Poisson model with a linear time term

Predictors (deseasonalized and standardized on TRAIN; source recorded in the output):
  enso  NASA_SSH_ENSO_INDICATOR (fallback: NOAA ONI)
  nao   MERRA-2 station-style NAO (fallback: NOAA CPC NAO)
  wind  MERRA-2 NY Bight wind from the NE (no fallback)
  gs    NASA-SSH Gulf Stream SSH difference, south minus north boxes (no fallback)

Method:
  1. Lag selection on TRAIN only, after prewhitening both series with the predictor's AR(1) filter.
     Cross-correlation at lags 0..6 months (predictor leads). Significance: two-sided 5% with a Bonferroni
     correction over the 7 lags (|z| > 2.69).
  2. Held-out test (TEST): OLS fitted on TRAIN, evaluated on TEST.
     Skill = 1 - SSE(model) / SSE(climatology) on the same months.
     Models: persistence; each predictor at its best lag; all concurrent (best lag 0..6); all leading (lag 1..6 only,
     i.e. a genuine forecast); leading + persistence.
  3. Surge days (cool season): Poisson GLM on TRAIN; test deviance skill vs the time-trend-only model;
     rate ratio per 1 SD of each predictor with a 95% CI.
"""
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config_ntr import (PROCESSED, PIPELINE_PROCESSED, RESULTS, FIGURES, TRAIN, TEST, MAX_LAG, COOL_MONTHS,
                        SURGE_THRESHOLD_M, ensure_dirs)

Z_CRIT = 2.69   # two-sided 5% with Bonferroni over 7 lags


def monthly_csv(path, col=None):
    if not path.exists():
        return None
    df = pd.read_csv(path, parse_dates=[0], index_col=0)
    s = df[col] if col else df.iloc[:, 0]
    s.index = s.index.to_period("M").to_timestamp()
    return s.groupby(level=0).mean().asfreq("MS")


def load_predictors():
    """Return (DataFrame of raw monthly predictors, dict of sources)."""
    cols, src = {}, {}
    ind = monthly_csv(PIPELINE_PROCESSED / "indicators.csv", "enso") if (PIPELINE_PROCESSED / "indicators.csv").exists() else None
    if ind is not None and ind.count() > 100:
        cols["enso"], src["enso"] = ind, "NASA_SSH_ENSO_INDICATOR"
    else:
        cols["enso"], src["enso"] = monthly_csv(PROCESSED / "oni.csv", "oni"), "NOAA ONI (fallback)"
    m2 = PROCESSED / "merra2_predictors.csv"
    pub = PROCESSED / "public_predictors.csv"
    if m2.exists():
        cols["nao"], src["nao"] = monthly_csv(m2, "nao_merra2"), "MERRA-2 SLP, station-style NAO"
        cols["wind"], src["wind"] = monthly_csv(m2, "wind_ne_ms"), "MERRA-2 NY Bight wind from NE"
    elif pub.exists():
        cols["nao"], src["nao"] = monthly_csv(pub, "nao_ncep"), "NCEP/NCAR reanalysis SLP, station-style NAO (public)"
        cols["wind"], src["wind"] = monthly_csv(pub, "wind_ne_ms"), "NCEP/NCAR reanalysis NY Bight wind from NE (public)"
    else:
        cols["nao"], src["nao"] = monthly_csv(PROCESSED / "cpc_nao.csv", "nao"), "NOAA CPC NAO (fallback)"
    box = PIPELINE_PROCESSED / "box_monthly.csv"
    if box.exists():
        b = pd.read_csv(box, parse_dates=[0], index_col=0)
        if {"gs_south", "gs_north"} <= set(b.columns):
            gs = b["gs_south"] - b["gs_north"]
            gs.index = gs.index.to_period("M").to_timestamp()
            cols["gs"], src["gs"] = gs.asfreq("MS"), "NASA-SSH Gulf Stream SSH difference (south - north)"
    return pd.DataFrame(cols), src


def train_mask(index):
    return (index >= pd.Timestamp(TRAIN[0])) & (index <= pd.Timestamp(TRAIN[1]) + pd.offsets.MonthEnd(0))


def test_mask(index):
    return (index >= pd.Timestamp(TEST[0])) & (index <= pd.Timestamp(TEST[1]) + pd.offsets.MonthEnd(0))


def deseason_standardize(s):
    tr = s[train_mask(s.index)]
    clim = tr.groupby(tr.index.month).mean()
    anom = s - clim.reindex(s.index.month).to_numpy()
    return anom / anom[train_mask(anom.index)].std()


def target_anomaly(y):
    """Remove TRAIN monthly climatology and TRAIN linear trend (extrapolated) from monthly mean NTR (mm)."""
    tr = y[train_mask(y.index)]
    clim = tr.groupby(tr.index.month).mean()
    anom = y - clim.reindex(y.index.month).to_numpy()
    t = (anom.index.year + (anom.index.month - 1) / 12).to_numpy()
    ok = train_mask(anom.index) & anom.notna().to_numpy()
    slope, icept = np.polyfit(t[ok], anom.to_numpy()[ok], 1)
    return anom - (icept + slope * t), slope


def ar1(x):
    x = x.dropna()
    return float(np.corrcoef(x.to_numpy()[1:], x.to_numpy()[:-1])[0, 1])


def lag_correlations(x, y):
    """Prewhitened cross-correlations on TRAIN; x leads y by k months."""
    a = ar1(x[train_mask(x.index)])
    xw, yw = x - a * x.shift(1), y - a * y.shift(1)
    out = []
    for k in range(MAX_LAG + 1):
        pair = pd.concat([xw.shift(k), yw], axis=1).dropna()
        pair = pair[train_mask(pair.index)]
        n = len(pair)
        r = float(np.corrcoef(pair.iloc[:, 0], pair.iloc[:, 1])[0, 1]) if n > 10 else np.nan
        out.append({"lag": k, "r": r, "n": n, "z": r * np.sqrt(n) if n else np.nan,
                    "significant": bool(abs(r) * np.sqrt(n) > Z_CRIT) if n else False})
    return {"prewhiten_ar1": a, "lags": out}


def best_lag(lags, leading=False):
    cand = [l for l in lags if (l["lag"] >= 1 or not leading) and np.isfinite(l["r"])]
    return max(cand, key=lambda l: abs(l["r"]))["lag"]


def evaluate(y, features):
    """OLS on TRAIN, skill on TEST vs climatology (prediction 0 for the anomaly), on common months."""
    df = pd.concat([y.rename("y"), features], axis=1).dropna()
    tr, te = df[train_mask(df.index)], df[test_mask(df.index)]
    if len(tr) < 36 or len(te) < 12:
        return None
    X = sm.add_constant(tr.drop(columns="y"))
    fit = sm.OLS(tr["y"], X).fit()
    pred = fit.predict(sm.add_constant(te.drop(columns="y"), has_constant="add"))
    sse, sse0 = float(((te["y"] - pred) ** 2).sum()), float((te["y"] ** 2).sum())
    return {"skill_vs_climatology": 1 - sse / sse0, "rmse_mm": float(np.sqrt(sse / len(te))),
            "rmse_climatology_mm": float(np.sqrt(sse0 / len(te))), "n_train": len(tr), "n_test": len(te),
            "train_r2": float(fit.rsquared), "coef": {k: float(v) for k, v in fit.params.items()},
            "pred": pred, "obs": te["y"]}


def surge_model(counts, feats):
    df = pd.concat([counts.rename("y"), feats], axis=1).dropna()
    df = df[df.index.month.isin(COOL_MONTHS)]
    df["t"] = df.index.year + (df.index.month - 1) / 12 - 2000
    tr, te = df[train_mask(df.index)], df[test_mask(df.index)]
    if len(tr) < 40 or len(te) < 20:
        return None
    base_cols, full_cols = ["t"], ["t"] + list(feats.columns)
    res = {}
    fits = {}
    for name, cols in (("trend_only", base_cols), ("with_predictors", full_cols)):
        # quasi-Poisson: Pearson-scaled covariance, because surge-day counts are overdispersed
        f = sm.GLM(tr["y"], sm.add_constant(tr[cols]), family=sm.families.Poisson()).fit(scale="X2")
        mu = f.predict(sm.add_constant(te[cols], has_constant="add"))
        y = te["y"].to_numpy()
        dev = 2 * np.sum(np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / mu), 0) - (y - mu))
        fits[name], res[name] = f, {"test_deviance": float(dev)}
    null = res["trend_only"]["test_deviance"]
    res["deviance_skill_vs_trend_only"] = 1 - res["with_predictors"]["test_deviance"] / null
    f = fits["with_predictors"]
    ci = f.conf_int()
    res["rate_ratio_per_sd"] = {c: {"rr": float(np.exp(f.params[c])), "ci95": [float(np.exp(ci.loc[c, 0])), float(np.exp(ci.loc[c, 1]))],
                                    "p": float(f.pvalues[c])} for c in feats.columns}
    res["n_train_months"], res["n_test_months"] = len(tr), len(te)
    res["mean_surge_days_per_cool_month_train"] = float(tr["y"].mean())
    return res


def season_outlook(counts, enso, outlook_year=2026):
    """Genuine forecast: August ENSO state -> surge days in the following cool season (Oct Y .. Apr Y+1).

    Quasi-Poisson with a linear time term; train seasons starting 1980-2011, test 2012-2025.
    Returns rate ratio per 1 SD of ENSO, test deviance skill vs trend-only, and the outlook for `outlook_year`.
    """
    rows = []
    for y in range(counts.index.year.min(), counts.index.year.max() + 1):
        season = counts.loc[f"{y}-10":f"{y + 1}-04"]
        aug = enso.get(pd.Timestamp(f"{y}-08-01"), np.nan)
        rows.append({"start_year": y, "surge_days": season.sum() if season.count() >= 6 else np.nan,
                     "months": int(season.count()), "enso_aug": aug, "t": y - 2000})
    df = pd.DataFrame(rows).set_index("start_year")
    fit_df = df.dropna()
    tr, te = fit_df.loc[:2011], fit_df.loc[2012:2025]
    if len(tr) < 15 or len(te) < 5:
        return None
    full = sm.GLM(tr["surge_days"], sm.add_constant(tr[["t", "enso_aug"]]), family=sm.families.Poisson()).fit(scale="X2")
    base = sm.GLM(tr["surge_days"], sm.add_constant(tr[["t"]]), family=sm.families.Poisson()).fit(scale="X2")

    def deviance(f, cols):
        mu = f.predict(sm.add_constant(te[cols], has_constant="add")).to_numpy()
        yv = te["surge_days"].to_numpy()
        return float(2 * np.sum(np.where(yv > 0, yv * np.log(np.where(yv > 0, yv, 1) / mu), 0) - (yv - mu)))
    out = {"n_train_seasons": len(tr), "n_test_seasons": len(te),
           "rate_ratio_per_sd": float(np.exp(full.params["enso_aug"])),
           "rate_ratio_ci95": [float(np.exp(full.conf_int().loc["enso_aug", 0])), float(np.exp(full.conf_int().loc["enso_aug", 1]))],
           "p": float(full.pvalues["enso_aug"]), "dispersion": float(full.scale),
           "test_deviance_skill_vs_trend_only": 1 - deviance(full, ["t", "enso_aug"]) / deviance(base, ["t"]),
           "mean_surge_days_per_season_train": float(tr["surge_days"].mean()),
           "mean_surge_days_per_season_test": float(te["surge_days"].mean())}
    # Robustness: all complete seasons 1980-2025, and leave-one-season-out rate ratios
    allf = fit_df.loc[:2025]
    fa = sm.GLM(allf["surge_days"], sm.add_constant(allf[["t", "enso_aug"]]), family=sm.families.Poisson()).fit(scale="X2")
    loo = []
    for s in allf.index:
        x = allf.drop(s)
        f1 = sm.GLM(x["surge_days"], sm.add_constant(x[["t", "enso_aug"]]), family=sm.families.Poisson()).fit(scale="X2")
        loo.append((float(np.exp(f1.params["enso_aug"])), float(f1.pvalues["enso_aug"])))
    out["all_seasons"] = {"n": len(allf), "rate_ratio_per_sd": float(np.exp(fa.params["enso_aug"])),
                          "ci95": [float(np.exp(fa.conf_int().loc["enso_aug", 0])), float(np.exp(fa.conf_int().loc["enso_aug", 1]))],
                          "p": float(fa.pvalues["enso_aug"]),
                          "leave_one_out_rr_range": [min(r for r, _ in loo), max(r for r, _ in loo)],
                          "leave_one_out_max_p": max(p for _, p in loo)}
    strong = allf[allf["enso_aug"] >= 1.2]
    out["strong_el_nino_seasons"] = {int(k): float(v) for k, v in strong["surge_days"].items()}
    out["observed_enso_aug_max_sd"] = float(allf["enso_aug"].max())
    e = enso.get(pd.Timestamp(f"{outlook_year}-08-01"), np.nan)
    if np.isfinite(e):
        x = pd.DataFrame({"const": [1.0], "t": [outlook_year - 2000], "enso_aug": [e]})
        pf = full.get_prediction(x).summary_frame(alpha=0.05)
        pb = base.get_prediction(x[["const", "t"]]).summary_frame(alpha=0.05)
        out["outlook"] = {"season": f"{outlook_year}-10..{outlook_year + 1}-04", "enso_aug_sd": float(e),
                          "expected_surge_days": float(pf["mean"].iloc[0]),
                          "expected_ci95": [float(pf["mean_ci_lower"].iloc[0]), float(pf["mean_ci_upper"].iloc[0])],
                          "trend_only_expected": float(pb["mean"].iloc[0]),
                          "extrapolation": bool(e > out["observed_enso_aug_max_sd"]),
                          "note": "Expected count with a 95% interval for the mean, not a prediction interval for one season."}
    df.to_csv(RESULTS / "ntr_seasons.csv")
    return out


def main():
    ensure_dirs()
    tgt = pd.read_csv(PROCESSED / "ntr_monthly.csv", parse_dates=["date"], index_col="date").asfreq("MS")
    y, trend = target_anomaly(tgt["ntr_mean_mm"])
    raw, sources = load_predictors()
    preds = raw.apply(deseason_standardize)
    out = {"sources": sources, "train": TRAIN, "test": TEST, "surge_threshold_m": SURGE_THRESHOLD_M,
           "target_train_trend_mm_per_yr": float(trend), "lag_analysis": {}, "models": {}}

    # 1. lag analysis (all months and cool season only)
    for name in preds.columns:
        la = lag_correlations(preds[name], y)
        cool_y = y.where(y.index.month.isin(COOL_MONTHS))
        la_cool = lag_correlations(preds[name], cool_y)
        out["lag_analysis"][name] = {"all_months": la, "cool_season": la_cool,
                                     "best_lag_any": best_lag(la["lags"]), "best_lag_leading": best_lag(la["lags"], True)}

    # 2. held-out prediction of monthly mean NTR anomaly
    def lagged(names, leading):
        cols = {}
        for n in names:
            k = out["lag_analysis"][n]["best_lag_leading" if leading else "best_lag_any"]
            cols[f"{n}_lag{k}"] = preds[n].shift(k)
        return pd.DataFrame(cols)
    persist = y.shift(1).rename("persistence")
    models = {"persistence": persist.to_frame()}
    for n in preds.columns:
        models[f"{n} (best lag)"] = lagged([n], False)
    models["all concurrent (best lag 0-6)"] = lagged(list(preds.columns), False)
    models["all leading (lag 1-6, forecast)"] = lagged(list(preds.columns), True)
    models["all leading + persistence"] = pd.concat([lagged(list(preds.columns), True), persist], axis=1)
    best = None
    for name, feats in models.items():
        r = evaluate(y, feats)
        if r is None:
            continue
        if name.startswith("all leading") and (best is None or r["skill_vs_climatology"] > best[1]["skill_vs_climatology"]):
            best = (name, r)
        out["models"][name] = {k: v for k, v in r.items() if k not in ("pred", "obs")}

    # 3. surge days, cool season, concurrent best lags
    out["surge_days_cool_season"] = surge_model(tgt["surge_days"], lagged(list(preds.columns), False))
    out["season_outlook"] = season_outlook(tgt["surge_days"], preds["enso"])

    # figures
    fig, axes = plt.subplots(1, len(preds.columns), figsize=(3.2 * len(preds.columns), 3), sharey=True)
    for ax, n in zip(np.atleast_1d(axes), preds.columns):
        lags = out["lag_analysis"][n]["all_months"]["lags"]
        ax.bar([l["lag"] for l in lags], [l["r"] for l in lags], color="#2a78d6")
        thr = Z_CRIT / np.sqrt(max(lags[0]["n"], 1))
        ax.axhline(thr, ls=":", c="#52514e"); ax.axhline(-thr, ls=":", c="#52514e"); ax.axhline(0, c="#c3c2b7", lw=.8)
        ax.set_title(f"{n}\n{sources[n][:38]}", fontsize=8); ax.set_xlabel("lag (months, index leads)")
    np.atleast_1d(axes)[0].set_ylabel("prewhitened correlation (train)")
    fig.tight_layout(); fig.savefig(FIGURES / "ntr_lag_correlations.png", dpi=150); plt.close(fig)
    if best:
        name, r = best
        fig, ax = plt.subplots(figsize=(9, 3))
        ax.plot(r["obs"].index, r["obs"], color="#2a78d6", lw=1.2, label="observed NTR anomaly")
        ax.plot(r["pred"].index, r["pred"], color="#eb6834", lw=1.4, label=f"forecast: {name}")
        ax.axhline(0, c="#c3c2b7", lw=.8); ax.set_ylabel("mm"); ax.legend(fontsize=8, frameon=False)
        ax.set_title(f"Held-out test {TEST[0]}..: skill vs climatology {r['skill_vs_climatology']:.2f}", fontsize=9)
        fig.tight_layout(); fig.savefig(FIGURES / "ntr_forecast_test.png", dpi=150); plt.close(fig)

    (RESULTS / "ntr.json").write_text(json.dumps(out, indent=1, default=float))
    lines = [f"# NTR study: The Battery ({TRAIN[0]}..{TRAIN[1]} train, {TEST[0]}.. test)", "",
             f"Sources: {sources}", f"Target trend removed (train fit): {trend:.2f} mm/yr", "", "## Lag analysis (prewhitened, train)"]
    for n, la in out["lag_analysis"].items():
        sig = [l["lag"] for l in la["all_months"]["lags"] if l["significant"]]
        sigc = [l["lag"] for l in la["cool_season"]["lags"] if l["significant"]]
        rs = ", ".join(f"{l['lag']}:{l['r']:+.2f}" for l in la["all_months"]["lags"])
        lines.append(f"- {n}: r by lag {rs}; significant lags (all) {sig or 'none'}, (cool season) {sigc or 'none'}; "
                     f"best any {la['best_lag_any']}, best leading {la['best_lag_leading']}")
    lines += ["", "## Held-out skill (monthly mean NTR anomaly)", "| model | skill vs climatology | RMSE mm | clim RMSE mm | n test |", "|---|---:|---:|---:|---:|"]
    for n, m in out["models"].items():
        lines.append(f"| {n} | {m['skill_vs_climatology']:.3f} | {m['rmse_mm']:.1f} | {m['rmse_climatology_mm']:.1f} | {m['n_test']} |")
    s = out["surge_days_cool_season"]
    if s:
        lines += ["", f"## Cool-season surge days (> {SURGE_THRESHOLD_M} m)",
                  f"Deviance skill vs trend-only on test: {s['deviance_skill_vs_trend_only']:.3f} "
                  f"(train mean {s['mean_surge_days_per_cool_month_train']:.2f} days/month)"]
        for c, v in s["rate_ratio_per_sd"].items():
            lines.append(f"- {c}: rate ratio per SD {v['rr']:.2f} [{v['ci95'][0]:.2f}, {v['ci95'][1]:.2f}], p = {v['p']:.3g}")
    o = out["season_outlook"]
    if o:
        lines += ["", "## Season forecast: August ENSO -> Oct-Apr surge days (quasi-Poisson, trend term)",
                  f"Train {o['n_train_seasons']} seasons (1980-2011), test {o['n_test_seasons']} (2012-2025); dispersion {o['dispersion']:.2f}",
                  f"Rate ratio per SD of August ENSO: {o['rate_ratio_per_sd']:.2f} [{o['rate_ratio_ci95'][0]:.2f}, {o['rate_ratio_ci95'][1]:.2f}], p = {o['p']:.3g}",
                  f"Test deviance skill vs trend-only: {o['test_deviance_skill_vs_trend_only']:.3f}",
                  f"Mean surge days per season: train {o['mean_surge_days_per_season_train']:.1f}, test {o['mean_surge_days_per_season_test']:.1f}",
                  f"All {o['all_seasons']['n']} seasons: RR {o['all_seasons']['rate_ratio_per_sd']:.2f} "
                  f"[{o['all_seasons']['ci95'][0]:.2f}, {o['all_seasons']['ci95'][1]:.2f}], p = {o['all_seasons']['p']:.2g}; "
                  f"leave-one-out RR {o['all_seasons']['leave_one_out_rr_range'][0]:.2f}-{o['all_seasons']['leave_one_out_rr_range'][1]:.2f}, "
                  f"max p {o['all_seasons']['leave_one_out_max_p']:.2g}",
                  f"Strong El Nino seasons (Aug ENSO >= 1.2 SD): {o['strong_el_nino_seasons']}"]
        if "outlook" in o:
            q = o["outlook"]
            lines.append(f"Outlook {q['season']}: August ENSO = {q['enso_aug_sd']:+.2f} SD -> expected {q['expected_surge_days']:.1f} "
                         f"surge days [{q['expected_ci95'][0]:.1f}, {q['expected_ci95'][1]:.1f}] vs trend-only {q['trend_only_expected']:.1f}")
    (RESULTS / "ntr_summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
