"""Gauge trends, ONI amplitudes, event peaks, and Battery winter comparison."""
import argparse
import numpy as np
import pandas as pd
from scipy import stats as sp
from config import GAUGES, ENSO_LAG, PEAK_WINDOWS, PERMUTATIONS, SEED, PROCESSED
from common import read_monthly, metadata, save_json
from stats import (deseasonalize, sen_slope, plain_mk, mk_hamed_rao, seasonal_kendall,
                   naive_ols, ols_ar1, fit_with_index, regression, residual_rho, years)


def anomalies(series):
    """Monthly climatology and full-record linear trend removed, in mm."""
    s = deseasonalize(series).dropna()
    t = years(s.index)
    fit = regression(s, np.column_stack((np.ones(len(s)), t-t.mean())), s.index)
    return pd.Series(fit["residual"], index=s.index, name="anomaly_mm")


def mean_ci(values):
    """Mean and Student-t 95% CI (mm), independent winter sampling units."""
    values = np.asarray(values)
    if len(values) < 2:
        raise ValueError("At least two winters per group are required")
    radius = sp.t.ppf(.975, len(values)-1)*sp.sem(values)
    return {"n": len(values), "mean_mm": values.mean(),
            "ci95_mm": [values.mean()-radius, values.mean()+radius]}


def winter_comparison(series, oni):
    """Oct-Apr mean by January year; El Nino iff that year's DJF ONI >=0.5 C."""
    anomaly, winters = anomalies(series), []
    for year in range(anomaly.index.min().year+1, anomaly.index.max().year+1):
        dates = pd.date_range(f"{year-1}-10-01", periods=7, freq="MS")
        values = anomaly.reindex(dates)
        djf = oni.get(pd.Timestamp(year, 1, 1), np.nan)
        if values.notna().all() and np.isfinite(djf):
            winters.append({"year": year, "mean_mm": values.mean(), "djf_oni_c": djf,
                            "el_nino": bool(djf >= .5)})
    frame = pd.DataFrame(winters)
    if frame.empty:
        raise ValueError("No complete Oct-Apr winters with DJF ONI")
    a, b = frame.loc[frame.el_nino, "mean_mm"].to_numpy(), frame.loc[~frame.el_nino, "mean_mm"].to_numpy()
    first, second = mean_ci(a), mean_ci(b)
    test = sp.ttest_ind(a, b, equal_var=False)
    va, vb = np.var(a, ddof=1)/len(a), np.var(b, ddof=1)/len(b)
    df = (va+vb)**2/(va**2/(len(a)-1)+vb**2/(len(b)-1))
    difference = a.mean()-b.mean()
    radius = sp.t.ppf(.975, df)*np.sqrt(va+vb)
    pooled, rng, count = np.r_[a, b], np.random.default_rng(SEED), 0
    for _ in range(PERMUTATIONS):
        shuffled = rng.permutation(pooled)
        count += abs(shuffled[:len(a)].mean()-shuffled[len(a):].mean()) >= abs(difference)
    frame.to_csv(PROCESSED / "battery_winters.csv", index=False)
    return {"window": [f"{int(frame.year.min())-1}-10-01", f"{int(frame.year.max())}-04-01"],
            "n": len(frame), "method": "Complete 7-month Oct-Apr detrended/deseasonalized anomalies; DJF ONI >=0.5 C",
            "el_nino": first, "other": second, "difference_mm": difference,
            "ci95_mm": [difference-radius, difference+radius], "ci_method": "Welch independent-winter CI",
            "welch_t": test.statistic, "welch_df": df, "welch_p": test.pvalue,
            "permutation_p": (count+1)/(PERMUTATIONS+1), "permutations": PERMUTATIONS,
            "permutation_method": "Two-sided winter-label permutation, plus-one correction; exchangeable winters",
            "seed": SEED, "winters": winters}


def coastal_comparison(gauge, box):
    """Same-month gauge/box comparison; all trend differences in mm/year."""
    pair = pd.concat([deseasonalize(gauge).rename("gauge"), deseasonalize(box).rename("box")], axis=1).dropna()
    if len(pair) < 24:
        raise ValueError("Fewer than 24 matched coastal months")
    r = float(pair.gauge.corr(pair.box))
    product = max(0, residual_rho(pair.gauge, pair.index)*residual_rho(pair.box, pair.index))
    n_eff = float(np.clip(len(pair)*(1-product)/(1+product), 4, len(pair)))
    fisher = np.arctanh(np.clip(r, -.99999999, .99999999))
    ci = np.tanh(fisher+np.array([-1, 1])*sp.norm.ppf(.975)/np.sqrt(n_eff-3))
    return {**metadata(pair.gauge), "method": "Pearson correlation of matched deseasonalized series",
            "correlation": r, "correlation_ci95": ci.tolist(), "n_eff": n_eff,
            "ci_method": "Fisher-z interval with AR(1) product effective sample size",
            "gauge_trend": ols_ar1(pair.gauge), "box_trend": ols_ar1(pair.box),
            "gauge_minus_box_trend": ols_ar1(pair.gauge-pair.box)}


def main(no_nasa=False):
    oni = read_monthly("oni.csv").oni_c
    boxes = None if no_nasa else read_monthly("box_monthly.csv")
    output = {"experiment": "E4", "nasa_enabled": not no_nasa, "gauges": {},
              "notes": ["Gauge records are relative sea level on datum MSL; no vertical-land-motion or GIA correction.",
                        "Nonseasonal trend methods use deseasonalized monthly values; seasonal Kendall uses raw monthly values.",
                        "Peaks are observed monthly maxima after full-record climatology and linear detrending; no inferential CI for a selected maximum.",
                        "Hamed-Rao p-values compress missing months; gap counts are reported. Sen intervals are independent-error rank intervals."]}
    for station, info in GAUGES.items():
        print(f"E4: {info['name']}", flush=True)
        gauge = read_monthly(f"gauge_{station}.csv").level_mm
        adjusted = deseasonalize(gauge)
        trends = [function(adjusted) for function in (sen_slope, naive_ols, plain_mk, mk_hamed_rao, ols_ar1)]
        trends.append(seasonal_kendall(gauge))
        fitted = fit_with_index(gauge, oni, ENSO_LAG)
        fitted.pop("index_removed").to_csv(PROCESSED / f"gauge_{station}_oni_removed.csv", index_label="date")
        fitted["index_coefficient_units"] = "mm per degree C ONI"
        anomaly = anomalies(gauge)
        peaks = []
        for label, (start, end) in PEAK_WINDOWS.items():
            part = anomaly.loc[start:end].dropna()
            peaks.append({"event": label, "requested_window": [start, end], **metadata(part),
                          "method": "Maximum detrended/deseasonalized monthly anomaly",
                          "peak_mm": float(part.max()) if len(part) else None,
                          "peak_month": str(part.idxmax().date()) if len(part) else None, "ci95": None,
                          "ci_note": "Descriptive selected maximum; no confidence interval"})
        record = {"name": info["name"], **metadata(gauge), "missing_months": int(gauge.isna().sum()),
                  "trends": trends, "oni_fit": fitted, "peaks": peaks}
        if boxes is not None:
            record["nasa_box_comparison"] = {"box": info["box"], **coastal_comparison(gauge, boxes[info["box"]])}
        output["gauges"][station] = record
        if station == "8518750":
            output["battery_winters"] = winter_comparison(gauge, oni)
    return save_json("e4.json", output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-nasa", action="store_true")
    main(parser.parse_args().no_nasa)
