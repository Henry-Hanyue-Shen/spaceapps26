"""Monthly time-series statistics. Sea level: mm; all slopes: mm/year.

AR(1) inference uses n_eff=n(1-rho)/(1+rho), residual-based rho, and
SE inflation sqrt(n/n_eff). Negative rho is conservatively treated as zero.
This effective-sample-size approximation is not an exact GLS confidence band.
"""
import warnings
import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats as sp
from common import metadata


def monthly(series):
    """Normalize a dated series to one value per calendar month (input units)."""
    if not isinstance(series, pd.Series) or not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError("Expected a pandas Series with a DatetimeIndex; sea level in mm")
    if series.index.has_duplicates:
        raise ValueError("Duplicate timestamps are not allowed")
    return series.astype(float).replace([np.inf, -np.inf], np.nan).sort_index().resample("MS").mean()


def years(index):
    """Elapsed calendar years, with monthly observations separated by 1/12 yr."""
    ordinal = index.year.to_numpy() * 12 + index.month.to_numpy()
    return (ordinal - ordinal[0]) / 12.0


def deseasonalize(series):
    """Remove each calendar month's observed climatology; returns mm for mm input."""
    series = monthly(series)
    return series - series.groupby(series.index.month).transform("mean")


def sen_slope(series):
    """Theil-Sen slope and rank-based 95% CI, mm/yr; CI assumes independent errors."""
    s = monthly(series).dropna()
    if len(s) < 3:
        raise ValueError("Sen slope needs at least three observations")
    fit = sp.theilslopes(s.to_numpy(), years(s.index), alpha=0.95)
    return {**metadata(s), "method": "Sen (independent-error rank CI)",
            "trend_mm_yr": fit.slope, "ci95_mm_yr": [fit.low_slope, fit.high_slope]}


def _mk_result(series, function, label, seasonal=False):
    s = monthly(series)
    valid = s.dropna()
    if len(valid) < 12:
        raise ValueError("Kendall tests need at least 12 observations")
    # Preserve calendar positions for seasonal grouping. Ordinary MK can skip gaps.
    values = s.to_numpy() if seasonal else valid.to_numpy()
    if np.ptp(valid.to_numpy()) == 0:
        p, z, statistic = 1.0, 0.0, 0.0
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            fit = function(values)
        p, z, statistic = fit.p, fit.z, fit.s
    result = sen_slope(s)
    if seasonal:
        # Pair only identical calendar months; interval below inverts seasonal S.
        slopes, variance = [], 0.0
        for _, group in valid.groupby(valid.index.month):
            y, t = group.to_numpy(), years(group.index)
            i, j = np.triu_indices(len(y), 1)
            slopes.extend((y[j] - y[i]) / (t[j] - t[i]))
            _, counts = np.unique(y, return_counts=True)
            n = len(y)
            variance += (n*(n-1)*(2*n+5) - np.sum(counts*(counts-1)*(2*counts+5))) / 18
        slopes = np.sort(slopes)
        if not len(slopes):
            raise ValueError("Seasonal slope needs repeated calendar months")
        radius = sp.norm.ppf(.975) * np.sqrt(variance)
        lo = int(np.clip(np.round((len(slopes)-radius)/2)-1, 0, len(slopes)-1))
        hi = int(np.clip(np.round((len(slopes)+radius)/2), 0, len(slopes)-1))
        result.update(trend_mm_yr=np.median(slopes), ci95_mm_yr=[slopes[lo], slopes[hi]])
    result.update(method=label, p=p, z=z, statistic_s=statistic,
                  ci_method="Seasonal rank CI; independent years" if seasonal
                  else "Sen rank CI; independent errors (not Hamed-Rao adjusted)",
                  missing_months=int(s.isna().sum()))
    return result


def plain_mk(series):
    """Plain Mann-Kendall p-value and calendar-time Sen slope in mm/yr."""
    return _mk_result(series, mk.original_test, "Plain Mann-Kendall")


def mk_hamed_rao(series):
    """pymannkendall Hamed-Rao test; mm/yr Sen slope, separate independent-error CI.

    pymannkendall skips missing observations when estimating rank autocorrelation;
    gaps are reported, and its p-value is approximate for gappy records.
    """
    return _mk_result(series, mk.hamed_rao_modification_test, "Hamed-Rao Mann-Kendall")


def seasonal_kendall(series):
    """pymannkendall seasonal_test(period=12); seasonal Sen slope and CI in mm/yr."""
    return _mk_result(series, lambda x: mk.seasonal_test(x, period=12),
                      "Seasonal Kendall (period 12)", seasonal=True)


def residual_rho(residual, index):
    """Lag-one correlation (unitless), using only adjacent calendar-month pairs."""
    ordinal = index.year.to_numpy() * 12 + index.month.to_numpy()
    adjacent = np.diff(ordinal) == 1
    a, b = np.asarray(residual)[:-1][adjacent], np.asarray(residual)[1:][adjacent]
    if len(a) < 3 or np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return 0.0
    return float(np.clip(np.corrcoef(a, b)[0, 1], -0.99, 0.99))


def regression(y, design, index, adjusted=True):
    """OLS coefficients and approximate AR(1) covariance in design-dependent units."""
    y, design = np.asarray(y, float), np.asarray(design, float)
    n, k = design.shape
    if n <= k + 2 or np.linalg.matrix_rank(design) < k:
        raise ValueError("Too few observations or rank-deficient regression design")
    beta = np.linalg.lstsq(design, y, rcond=None)[0]
    residual = y - design @ beta
    rho = residual_rho(residual, index)
    effective = float(np.clip(n * (1-max(0, rho))/(1+max(0, rho)), k+1, n)) if adjusted else float(n)
    covariance = np.linalg.inv(design.T @ design) * (residual @ residual)/(n-k) * n/effective
    se = np.sqrt(np.maximum(0, np.diag(covariance)))
    critical = sp.t.ppf(.975, effective-k)
    denom = np.sum((y-y.mean())**2)
    return {"beta": beta, "residual": residual, "se": se, "covariance": covariance,
            "ci": np.column_stack((beta-critical*se, beta+critical*se)),
            "rho": rho, "n_eff": effective, "df": effective-k,
            "r2": 1-float(residual @ residual)/denom if denom > 0 else np.nan}


def _trend(series, adjusted):
    s = monthly(series).dropna()
    t = years(s.index)
    fit = regression(s, np.column_stack((np.ones(len(s)), t-t.mean())), s.index, adjusted)
    slope, se = fit["beta"][1], fit["se"][1]
    p = 2*sp.t.sf(abs(slope/se), fit["df"]) if se > 0 else float(slope == 0)
    return {**metadata(s), "method": "AR(1)-OLS effective sample size" if adjusted else "Naive OLS",
            "trend_mm_yr": slope, "ci95_mm_yr": fit["ci"][1].tolist(),
            "se_mm_yr": se, "p": p, "rho": fit["rho"], "n_eff": fit["n_eff"], "r2": fit["r2"]}


def ols_ar1(series):
    """OLS trend, AR(1) effective-sample-size SE and 95% CI, all in mm/yr."""
    return _trend(series, True)


def naive_ols(series):
    """OLS trend with independent-error SE and 95% CI in mm/yr."""
    return _trend(series, False)


def fit_with_index(series, index, lag):
    """Joint trend + annual/semiannual harmonics + fixed-lag index regression.

    Sea level is mm; trend and CI are mm/yr; index coefficient is mm/index-unit
    (mm/degree C for ONI). Positive integer lag means index leads sea level.
    Only beta_index * lagged_index is removed, leaving trend and seasonality.
    Both R-squared values use the exact same observations.
    """
    if not isinstance(lag, (int, np.integer)) or lag < 0:
        raise ValueError("lag must be a nonnegative integer number of months")
    s, idx = monthly(series), monthly(index)
    idx.index = idx.index + pd.DateOffset(months=int(lag))
    frame = pd.concat([s.rename("level"), idx.rename("index")], axis=1).dropna()
    t = years(frame.index)
    phase = 2*np.pi*(frame.index.month.to_numpy()-1)/12
    base = np.column_stack((np.ones(len(t)), t-t.mean(), np.sin(phase), np.cos(phase),
                            np.sin(2*phase), np.cos(2*phase)))
    design = np.column_stack((base, frame["index"]))
    fit = regression(frame.level, design, frame.index)
    reduced = regression(frame.level, base, frame.index)
    removed = frame.level - fit["beta"][-1]*frame["index"]
    return {**metadata(frame.level), "method": "Joint trend + two harmonics + index; AR(1) CI",
            "lag_months": int(lag), "trend_mm_yr": fit["beta"][1],
            "ci95_mm_yr": fit["ci"][1].tolist(), "index_coefficient": fit["beta"][-1],
            "index_ci95": fit["ci"][-1].tolist(), "r2_with_index": fit["r2"],
            "r2_without_index": reduced["r2"], "rho": fit["rho"], "n_eff": fit["n_eff"],
            "index_removed": removed.rename(s.name)}
