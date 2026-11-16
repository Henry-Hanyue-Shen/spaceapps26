"""Observed vs fitted/predicted values, written as tables for the team hand-off workbook.

season_predictions.csv  one row per cool season (Oct Y..Apr Y+1), The Battery:
    observed surge days; trend-only model; ENSO models (quasi-Poisson, log link: surge ~ time + ENSO) with
    (a) NOAA ONI in August, (b) NASA GISTEMP Nino3.4 in June. For each: the value fitted on the 1981-2009 seasons
    (in-sample for 'train', a genuine forecast for 'test' 2010-2025) and the leave-one-season-out prediction.
monthly_predictions.csv one row per month: observed monthly mean NTR anomaly (mm), persistence prediction, and the
    same-month model (NASA POWER wind + NASA POWER NAO + ONI, OLS fitted on 1981-2010; 'test' = 2011 onward).
model_coefficients.csv  every fitted coefficient with its 95% interval.
Same definitions and splits as explore_analyze.py.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from config_ntr import PROCESSED, RESULTS, ensure_dirs
from explore_analyze import TRAIN, TEST, SEASON_TRAIN, SEASON_TEST, anomaly, in_period, qp_fit, season_totals


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
    P = {c: anomaly(raw[c]) for c in ("oni", "nino34_giss", "wind_ne_power", "nao_power")}
    coefs = []

    # ---------------- seasons
    S = pd.DataFrame({"observed_surge_days": season_totals(tgt["surge_days"])})
    S.index.name = "season_start_year"
    S["season"] = [f"{y}-10..{y + 1}-04" for y in S.index]
    S["t"] = S.index - 2000
    S["oni_august_sd"] = [P["oni"].get(pd.Timestamp(y, 8, 1), np.nan) for y in S.index]
    S["nasa_nino34_june_sd"] = [P["nino34_giss"].get(pd.Timestamp(y, 6, 1), np.nan) for y in S.index]
    S["period"] = np.where(S.index <= SEASON_TRAIN[1], "train", "test")
    S.loc[S.index < SEASON_TRAIN[0], "period"] = "before 1981 (not used)"
    use = S.loc[SEASON_TRAIN[0]:SEASON_TEST[1]].rename(columns={"observed_surge_days": "y"})
    tr = use.loc[:SEASON_TRAIN[1]]
    for label, xcols in (("trend_only", []), ("oni_august", ["oni_august_sd"]), ("nasa_nino34_june", ["nasa_nino34_june_sd"])):
        d = use[["y", "t"] + xcols].dropna()
        f = qp_fit(d.loc[:SEASON_TRAIN[1]], ["t"] + xcols)
        S.loc[d.index, f"pred_{label}_trainfit"] = f.predict(sm.add_constant(d[["t"] + xcols], has_constant="add"))
        for s in d.index:
            rest = d.drop(s)
            S.loc[s, f"pred_{label}_leave_one_out"] = float(qp_fit(rest, ["t"] + xcols).predict(sm.add_constant(d.loc[[s], ["t"] + xcols], has_constant="add")).iloc[0])
        ci = f.conf_int()
        for name in f.params.index:
            coefs.append({"model": f"season surge days ~ {label} (quasi-Poisson, log link, train 1981-2009)", "term": name,
                          "coefficient": f.params[name], "ci95_low": ci.loc[name, 0], "ci95_high": ci.loc[name, 1],
                          "exp_coefficient": np.exp(f.params[name]), "p": f.pvalues[name], "n": int(f.nobs), "dispersion": f.scale})
    S.drop(columns="t").to_csv(RESULTS / "season_predictions.csv")

    # ---------------- months
    y = anomaly(tgt["ntr_mean_mm"], standardize=False)
    M = pd.DataFrame({"observed_ntr_anomaly_mm": y, "ntr_mean_mm_raw": tgt["ntr_mean_mm"], "surge_days": tgt["surge_days"],
                      "wind_ne_power_sd": P["wind_ne_power"], "nao_power_sd": P["nao_power"], "oni_sd": P["oni"]})
    M["pred_persistence_mm"] = np.nan
    d = pd.concat([y.rename("y"), y.shift(1).rename("prev")], axis=1).dropna()
    fp = sm.OLS(d[in_period(d.index, TRAIN)]["y"], sm.add_constant(d[in_period(d.index, TRAIN)][["prev"]])).fit()
    M.loc[d.index, "pred_persistence_mm"] = fp.predict(sm.add_constant(d[["prev"]], has_constant="add"))
    d = M[["observed_ntr_anomaly_mm", "wind_ne_power_sd", "nao_power_sd", "oni_sd"]].dropna()
    fc = sm.OLS(d[in_period(d.index, TRAIN)]["observed_ntr_anomaly_mm"], sm.add_constant(d[in_period(d.index, TRAIN)].iloc[:, 1:])).fit()
    M.loc[d.index, "pred_same_month_model_mm"] = fc.predict(sm.add_constant(d.iloc[:, 1:], has_constant="add"))
    M["period"] = np.where(in_period(M.index, TRAIN), "train", np.where(in_period(M.index, TEST), "test", "before 1981 (not used)"))
    for f, label in ((fp, "monthly NTR anomaly ~ previous month (OLS, train 1981-2010)"),
                     (fc, "monthly NTR anomaly ~ wind + NAO + ONI, same month (OLS, train 1981-2010)")):
        ci = f.conf_int()
        for name in f.params.index:
            coefs.append({"model": label, "term": name, "coefficient": f.params[name], "ci95_low": ci.loc[name, 0], "ci95_high": ci.loc[name, 1],
                          "exp_coefficient": np.nan, "p": f.pvalues[name], "n": int(f.nobs), "dispersion": np.nan})
    M.index = M.index.strftime("%Y-%m")
    M.to_csv(RESULTS / "monthly_predictions.csv", index_label="month")
    pd.DataFrame(coefs).to_csv(RESULTS / "model_coefficients.csv", index=False)

    te = S[S.period == "test"].dropna(subset=["observed_surge_days", "pred_oni_august_trainfit"])
    print(f"seasons: {S['observed_surge_days'].count()} observed; test seasons {len(te)}")
    for c in ("pred_trend_only_trainfit", "pred_oni_august_trainfit", "pred_nasa_nino34_june_trainfit"):
        print(f"  test mean abs error, {c}: {(te['observed_surge_days'] - te[c]).abs().mean():.2f} days")
    mt = M[(M.period == "test")].dropna(subset=["observed_ntr_anomaly_mm", "pred_same_month_model_mm"])
    print(f"months: test n {len(mt)}, RMSE same-month model {np.sqrt(((mt.observed_ntr_anomaly_mm - mt.pred_same_month_model_mm) ** 2).mean()):.1f} mm, "
          f"persistence {np.sqrt(((mt.observed_ntr_anomaly_mm - mt.pred_persistence_mm) ** 2).mean()):.1f} mm, "
          f"climatology {np.sqrt((mt.observed_ntr_anomaly_mm ** 2).mean()):.1f} mm")


if __name__ == "__main__":
    main()
