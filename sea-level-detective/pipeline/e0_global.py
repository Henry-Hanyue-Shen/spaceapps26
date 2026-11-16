"""Global gridded/indicator consistency and quadratic rates/accelerations."""
import numpy as np
import pandas as pd
from scipy import stats as sp
from common import read_monthly, metadata, save_json
from stats import years, regression, ols_ar1
from config import SEED


def quadratic(series):
    """Quadratic plus annual/semiannual nuisance terms; mm/yr and mm/yr^2."""
    s = series.dropna()
    t = years(s.index)
    center = t.mean()
    t -= center
    phase = 2*np.pi*(s.index.month.to_numpy()-1)/12
    design = np.column_stack((np.ones(len(t)), t, .5*t*t, np.sin(phase), np.cos(phase),
                              np.sin(2*phase), np.cos(2*phase)))
    fit = regression(s, design, s.index)
    rates = []
    for label, value in (("start", t[0]), ("midpoint", 0), ("end", t[-1])):
        vector = np.array([0, 1, value, 0, 0, 0, 0])
        estimate = vector @ fit["beta"]
        radius = sp.t.ppf(.975, fit["df"])*np.sqrt(vector @ fit["covariance"] @ vector)
        rates.append({"epoch": label, "years_since_first_month": value+center,
                      "rate_mm_yr": estimate, "ci95_mm_yr": [estimate-radius, estimate+radius]})
    return {**metadata(s), "method": "Joint quadratic + two harmonics; AR(1) effective-sample-size CI",
            "rates": rates, "acceleration_mm_yr2": fit["beta"][2],
            "acceleration_ci95_mm_yr2": fit["ci"][2].tolist(), "rho": fit["rho"], "n_eff": fit["n_eff"]}


def main():
    print("E0: matched global series and quadratic fits", flush=True)
    ours = read_monthly("box_monthly.csv")["global"]
    reference = read_monthly("indicators.csv").gmsl_mm
    pair = pd.concat([ours.rename("ours"), reference.rename("reference")], axis=1).dropna()
    difference = pair.ours-pair.reference
    if len(pair) < 24:
        raise ValueError("Not enough matched global months")
    # Twelve-month moving blocks preserve short-range dependence in bias/RMSE CIs.
    rng, n = np.random.default_rng(SEED), len(pair)
    starts = rng.integers(0, n, size=(2000, int(np.ceil(n/12))))
    indices = ((starts[:, :, None]+np.arange(12)) % n).reshape(2000, -1)[:, :n]
    sampled = difference.to_numpy()[indices]
    bias_ci = np.quantile(sampled.mean(axis=1), [.025, .975])
    rmse_ci = np.quantile(np.sqrt((sampled**2).mean(axis=1)), [.025, .975])
    comparisons = {**metadata(difference), "method": "Same-month, same-unit differences, gridded minus indicator",
                   "bias_mm": difference.mean(), "bias_ci95_mm": bias_ci.tolist(),
                   "rmse_mm": np.sqrt(np.mean(difference**2)), "rmse_ci95_mm": rmse_ci.tolist(),
                   "ci_method": "Circular moving-block bootstrap, 12 months, 2000 replicates",
                   "trend_difference": ols_ar1(difference)}
    fits = {}
    for name, series in (("gridded_global", ours), ("nasa_gmsl", reference)):
        fits[name] = {"1993_2017": quadratic(series.loc["1993-01":"2017-12"]),
                      "1993_latest": quadratic(series.loc["1993-01":])}
    return save_json("e0.json", {"experiment": "E0", "gia_correction_applied": False,
                                "global_latitude_band": [-66, 66], "comparison": comparisons,
                                "quadratic_fits": fits, "context": "Nerem et al. (2018) is context only; no tuning to literature."})


if __name__ == "__main__":
    main()
