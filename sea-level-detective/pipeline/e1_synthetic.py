"""Seeded monthly AR(1) Monte Carlo; batched exact rank calculations for speed."""
import time
import numpy as np
import pandas as pd
from scipy import stats as sp
from scipy.signal import lfilter
from config import (SEED, MC_REPLICATES, MC_LENGTHS, MC_TRENDS, GAUGES,
                    PROCESSED, FIGURES, ensure_dirs)
from common import read_monthly, metadata, save_json
from stats import deseasonalize, regression, years, residual_rho

METHODS = ("naive_ols", "plain_mk", "hamed_rao_mk", "seasonal_kendall", "ar1_ols")


def ar1_noise(rng, count, months, sigma, phi):
    """Stationary Gaussian AR(1), marginal SD sigma mm (not innovation SD)."""
    if sigma <= 0 or abs(phi) >= 1:
        raise ValueError("Require sigma > 0 and |phi| < 1")
    innovations = rng.normal(0, sigma*np.sqrt(1-phi**2), (count, months))
    innovations[:, 0] = rng.normal(0, sigma, count)
    return lfilter([1], [1, -phi], innovations, axis=1)


def noise_parameters():
    """Estimate each gauge's detrended, deseasonalized residual SD and lag-one rho."""
    estimates = []
    for station, info in GAUGES.items():
        if not (PROCESSED / f"gauge_{station}.csv").exists():
            continue
        s = deseasonalize(read_monthly(f"gauge_{station}.csv").level_mm).dropna()
        if len(s) < 120:
            continue
        t = years(s.index)
        fit = regression(s, np.column_stack((np.ones(len(s)), t-t.mean())), s.index)
        estimates.append({"station": station, "name": info["name"], **metadata(s),
                          "sigma_mm": np.std(fit["residual"], ddof=2),
                          "phi": residual_rho(fit["residual"], s.index)})
    if estimates:
        return {"sigma_mm": float(np.median([v["sigma_mm"] for v in estimates])),
                "phi": float(np.median([v["phi"] for v in estimates])),
                "method": "Median across gauge residual estimates; monthly climatology and OLS trend removed",
                "gauge_estimates": estimates, "fallback": False}
    return {"sigma_mm": 30.0, "phi": .6, "method": "Specified fallback; gauge residual estimates unavailable",
            "gauge_estimates": [], "fallback": True}


def wilson(successes, total):
    """Binomial Wilson 95% confidence interval for a rejection probability."""
    z, p = sp.norm.ppf(.975), successes/total
    center = (p+z*z/(2*total))/(1+z*z/total)
    radius = z*np.sqrt(p*(1-p)/total+z*z/(4*total*total))/(1+z*z/total)
    return [float(center-radius), float(center+radius)]


def batch_pvalues(noise, trends=MC_TRENDS):
    """Exact continuous-data MK/seasonal/HR tests, plus OLS, for complete months.

    Batches avoid Python loops over every pair. HR uses the pymannkendall
    all-lag, significant-rank-ACF correction (including absolute weighted sum).
    Trend equivariance lets all trend settings share a Sen detrend and ACF.
    This helper is only for simulated, tie-free, complete Gaussian series;
    observed-data tests use pymannkendall in stats.py.
    """
    count, n = noise.shape
    if n % 12 or n < 24 or not np.isfinite(noise).all():
        raise ValueError("Simulation requires complete years of finite monthly data")
    output = {float(trend): {method: np.empty(count) for method in METHODS} for trend in trends}
    i, j = np.triu_indices(n, 1)
    delta = (j-i)/12
    same_month = (j-i) % 12 == 0
    t = np.arange(n)/12
    t -= t.mean()
    ssx = t @ t
    mk_var = n*(n-1)*(2*n+5)/18
    ny = n//12
    seasonal_var = 12*ny*(ny-1)*(2*ny+5)/18
    k = np.arange(1, n)
    weight = (n-k)*(n-k-1)*(n-k-2)
    for start in range(0, count, 32):
        stop = min(start+32, count)
        y = noise[start:stop]
        slopes = (y[:, j]-y[:, i])/delta
        sen = np.median(slopes, axis=1)
        ranks = sp.rankdata(y-sen[:, None]*t, axis=1)
        ranks -= ranks.mean(axis=1, keepdims=True)
        fft = np.fft.rfft(ranks, n=2*n, axis=1)
        acf = np.fft.irfft(fft*np.conj(fft), n=2*n, axis=1)[:, :n]
        acf /= acf[:, :1]
        significant = np.where(np.abs(acf[:, 1:]) > sp.norm.ppf(.975)/np.sqrt(n), acf[:, 1:], 0)
        correction = 1+2*np.abs(significant @ weight)/(n*(n-1)*(n-2))
        ols_slope = y @ t/ssx
        residual = y-y.mean(axis=1, keepdims=True)-ols_slope[:, None]*t
        a = residual[:, :-1]-residual[:, :-1].mean(axis=1, keepdims=True)
        b = residual[:, 1:]-residual[:, 1:].mean(axis=1, keepdims=True)
        rho = (a*b).sum(axis=1)/np.sqrt((a*a).sum(axis=1)*(b*b).sum(axis=1))
        rho = np.clip(rho, 0, .99)
        effective = np.clip(n*(1-rho)/(1+rho), 3, n)
        se = np.sqrt((residual*residual).sum(axis=1)/(n-2)/ssx)
        seasonal_slopes = slopes[:, same_month]
        for trend in trends:
            result = output[float(trend)]
            score = (slopes > -trend).sum(axis=1)-(slopes < -trend).sum(axis=1)
            z = (score-np.sign(score))/np.sqrt(mk_var)
            seasonal_score = ((seasonal_slopes > -trend).sum(axis=1)
                              -(seasonal_slopes < -trend).sum(axis=1))
            zs = (seasonal_score-np.sign(seasonal_score))/np.sqrt(seasonal_var)
            result["plain_mk"][start:stop] = 2*sp.norm.sf(np.abs(z))
            result["hamed_rao_mk"][start:stop] = 2*sp.norm.sf(np.abs(z)/np.sqrt(correction))
            result["seasonal_kendall"][start:stop] = 2*sp.norm.sf(np.abs(zs))
            result["naive_ols"][start:stop] = 2*sp.t.sf(np.abs(ols_slope+trend)/se, n-2)
            result["ar1_ols"][start:stop] = 2*sp.t.sf(np.abs(ols_slope+trend)/(se*np.sqrt(n/effective)), effective-2)
    return output


def crossing(lengths, powers):
    """First 90% crossing; interpolate only within a sampled bracket."""
    for i, power in enumerate(powers):
        if power >= .9:
            if i == 0:
                return {"years": None, "status": f"at or below {lengths[0]} years", "bracket_years": [None, lengths[0]]}
            value = lengths[i-1]+(.9-powers[i-1])/(power-powers[i-1])*(lengths[i]-lengths[i-1])
            return {"years": value, "status": "linear interpolation; descriptive, no crossing CI",
                    "bracket_years": [lengths[i-1], lengths[i]]}
    return {"years": None, "status": f"above {lengths[-1]} years or not observed", "bracket_years": [lengths[-1], None]}


def main():
    ensure_dirs()
    if MC_REPLICATES < 1000:
        raise ValueError("SPEC.md requires at least 1000 series per setting")
    import matplotlib.pyplot as plt
    started, rng, params = time.perf_counter(), np.random.default_rng(SEED), noise_parameters()
    rows = []
    for length in MC_LENGTHS:
        print(f"E1: {MC_REPLICATES} AR(1) series x {length} years x {len(MC_TRENDS)} trends", flush=True)
        noise = ar1_noise(rng, MC_REPLICATES, length*12, params["sigma_mm"], params["phi"])
        for trend, results in batch_pvalues(noise).items():
            for method, p in results.items():
                if not np.isfinite(p).all():
                    raise ValueError(f"Non-finite Monte Carlo p-values: {length}, {trend}, {method}")
                hits = int((p < .05).sum())
                rows.append({"window_years": length, "n_months": length*12, "n": MC_REPLICATES,
                             "true_trend_mm_yr": trend, "method": method, "rejections": hits,
                             "metric": "false_positive_rate" if trend == 0 else "power",
                             "estimate": hits/MC_REPLICATES, "ci95": wilson(hits, MC_REPLICATES),
                             "ci_method": "Binomial Wilson"})
    weatherhead = []
    for trend in MC_TRENDS[1:]:
        powers = [next(r["estimate"] for r in rows if r["window_years"] == length
                       and r["true_trend_mm_yr"] == trend and r["method"] == "ar1_ols") for length in MC_LENGTHS]
        specified = ((3.3*params["sigma_mm"]/abs(trend))*np.sqrt((1+params["phi"])/(1-params["phi"])))**(2/3)
        weatherhead.append({"trend_mm_yr": trend, "method": "Plain stationary AR(1) only",
                            "empirical_crossing": crossing(MC_LENGTHS, powers),
                            # Weatherhead et al. (1998) eq. for monthly data: sigma and phi of the monthly noise,
                            # trend per year, n* in years. No cadence conversion is needed.
                            "weatherhead_years": specified,
                            "n_per_setting": MC_REPLICATES, "ci": None})
    for trend in MC_TRENDS:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        for method in METHODS:
            selected = [r for r in rows if r["method"] == method and r["true_trend_mm_yr"] == trend]
            estimates = np.array([r["estimate"] for r in selected])
            intervals = np.array([r["ci95"] for r in selected]).T
            ax.errorbar(MC_LENGTHS, estimates, yerr=[estimates-intervals[0], intervals[1]-estimates],
                        label=method, marker="o", capsize=2)
        ax.axhline(.05 if trend == 0 else .9, color="grey", linestyle="--")
        ax.set(xlabel="Record length (years)", ylabel="False-positive rate" if trend == 0 else "Power",
               ylim=(0, 1.02), title=f"Monthly AR(1), true trend {trend} mm/year")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(FIGURES / f"e1_trend_{trend}.png", dpi=160)
        plt.close(fig)
    elapsed = time.perf_counter()-started
    result = {"experiment": "E1", "seed": SEED, "noise": params, "settings": rows,
              "weatherhead": weatherhead, "elapsed_seconds": elapsed, "under_ten_minutes": elapsed < 600,
              "notes": ["Two-sided alpha=0.05. No seasonal forcing, missing data, or index contamination.",
                        "Same noise realizations reused across trend settings; binomial CIs are per setting.",
                        "Weatherhead et al. (1998) formula uses the SD and lag-1 autocorrelation of the monthly noise, the trend per year, and gives n* in years (no cadence conversion).",
                        "Formula comparison is restricted to this plain stationary AR(1) case; no fit to literature."]}
    print(f"E1 completed in {elapsed:.1f} seconds", flush=True)
    return save_json("e1.json", result)


if __name__ == "__main__":
    main()
