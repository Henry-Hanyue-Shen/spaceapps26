# Sea Level Detective results

Generated: 2026-11-14T19:20:49.529280+00:00

Mode: no-NASA (public NOAA only).

All intervals are 95%. Trends: mm/year. Sea level: mm. ONI: degrees C. N/A denotes a descriptive quantity with no inferential interval, not zero uncertainty.

E0, E2, E3 and NASA coastal comparisons were skipped. NASA authentication/downloads were not invoked.

## E1: synthetic detection

Noise: marginal SD 61.3021 mm; monthly phi 0.691168. Median across gauge residual estimates; monthly climatology and OLS trend removed. Seed 20261114. Runtime 19.148 seconds.

Each cell is rejection proportion [binomial Wilson CI], n=1000 independent series per setting. Trend 0 reports false positives; positive trends report power. Two-sided alpha=0.05.

| Years | Months | True trend (mm/yr) | Naive OLS | Plain MK | Hamed-Rao MK | Seasonal Kendall | AR(1)-OLS |
|---:|---:|---:|---|---|---|---|---|
| 10 | 120 | 0 | 0.405 [0.374994, 0.435733] | 0.384 [0.354354, 0.414534] | 0.184 [0.161209, 0.20921] | 0.354 [0.324971, 0.384146] | 0.07 [0.0557764, 0.0875146] |
| 10 | 120 | 1 | 0.411 [0.380902, 0.441779] | 0.384 [0.354354, 0.414534] | 0.2 [0.176377, 0.225919] | 0.366 [0.336709, 0.396316] | 0.082 [0.066552, 0.100647] |
| 10 | 120 | 2 | 0.452 [0.421396, 0.482972] | 0.423 [0.392732, 0.453858] | 0.234 [0.208808, 0.261228] | 0.398 [0.368108, 0.428673] | 0.099 [0.0819954, 0.119074] |
| 10 | 120 | 3 | 0.496 [0.465086, 0.526945] | 0.48 [0.449171, 0.510982] | 0.284 [0.256919, 0.312734] | 0.445 [0.414467, 0.475954] | 0.133 [0.113351, 0.155458] |
| 10 | 120 | 4 | 0.545 [0.514022, 0.575633] | 0.534 [0.503011, 0.564729] | 0.341 [0.312277, 0.37094] | 0.503 [0.472059, 0.533918] | 0.188 [0.164995, 0.213393] |
| 15 | 180 | 0 | 0.384 [0.354354, 0.414534] | 0.371 [0.341606, 0.401381] | 0.185 [0.162155, 0.210256] | 0.346 [0.317157, 0.376022] | 0.07 [0.0557764, 0.0875146] |
| 15 | 180 | 1 | 0.434 [0.403592, 0.464913] | 0.416 [0.385829, 0.446814] | 0.2 [0.176377, 0.225919] | 0.392 [0.36221, 0.422616] | 0.079 [0.0638472, 0.0973749] |
| 15 | 180 | 2 | 0.542 [0.511018, 0.572661] | 0.527 [0.496011, 0.557782] | 0.306 [0.278225, 0.335259] | 0.511 [0.480035, 0.541881] | 0.125 [0.105926, 0.146944] |
| 15 | 180 | 3 | 0.672 [0.642292, 0.700392] | 0.654 [0.623978, 0.682843] | 0.435 [0.40458, 0.465918] | 0.635 [0.604697, 0.66427] | 0.226 [0.201155, 0.252942] |
| 15 | 180 | 4 | 0.787 [0.76055, 0.811253] | 0.779 [0.752243, 0.803622] | 0.587 [0.556207, 0.617127] | 0.759 [0.731533, 0.784485] | 0.371 [0.341606, 0.401381] |
| 20 | 240 | 0 | 0.389 [0.359263, 0.419586] | 0.39 [0.360245, 0.420596] | 0.16 [0.138585, 0.184017] | 0.359 [0.32986, 0.38922] | 0.05 [0.0381303, 0.0653138] |
| 20 | 240 | 1 | 0.461 [0.430313, 0.491986] | 0.45 [0.419415, 0.480967] | 0.239 [0.213598, 0.2664] | 0.435 [0.40458, 0.465918] | 0.089 [0.0728882, 0.108257] |
| 20 | 240 | 2 | 0.679 [0.649427, 0.707204] | 0.655 [0.624994, 0.683819] | 0.429 [0.398654, 0.45989] | 0.639 [0.608752, 0.668184] | 0.229 [0.204023, 0.256051] |
| 20 | 240 | 3 | 0.86 [0.837113, 0.880131] | 0.845 [0.821253, 0.866106] | 0.662 [0.632112, 0.690649] | 0.839 [0.81493, 0.860475] | 0.46 [0.429321, 0.490985] |
| 20 | 240 | 4 | 0.967 [0.954019, 0.976407] | 0.963 [0.949418, 0.973039] | 0.845 [0.821253, 0.866106] | 0.956 [0.941448, 0.967062] | 0.706 [0.677017, 0.733406] |
| 25 | 300 | 0 | 0.389 [0.359263, 0.419586] | 0.378 [0.348468, 0.408466] | 0.165 [0.143285, 0.189279] | 0.366 [0.336709, 0.396316] | 0.053 [0.0407465, 0.0686746] |
| 25 | 300 | 1 | 0.535 [0.504011, 0.565721] | 0.527 [0.496011, 0.557782] | 0.312 [0.28405, 0.341389] | 0.521 [0.490016, 0.551823] | 0.162 [0.140464, 0.186123] |
| 25 | 300 | 2 | 0.833 [0.808618, 0.854833] | 0.829 [0.804416, 0.851066] | 0.612 [0.581424, 0.641719] | 0.82 [0.794978, 0.842573] | 0.409 [0.378932, 0.439764] |
| 25 | 300 | 3 | 0.969 [0.956335, 0.978076] | 0.966 [0.952865, 0.975569] | 0.877 [0.855189, 0.895926] | 0.962 [0.948273, 0.972191] | 0.744 [0.716053, 0.77008] |
| 25 | 300 | 4 | 0.998 [0.992737, 0.999451] | 0.997 [0.991217, 0.998979] | 0.974 [0.962176, 0.982196] | 0.996 [0.98976, 0.998443] | 0.938 [0.921312, 0.951336] |
| 30 | 360 | 0 | 0.407 [0.376963, 0.437749] | 0.409 [0.378932, 0.439764] | 0.175 [0.152706, 0.199782] | 0.403 [0.373026, 0.433716] | 0.059 [0.0460143, 0.0753609] |
| 30 | 360 | 1 | 0.659 [0.62906, 0.687723] | 0.647 [0.616869, 0.676006] | 0.418 [0.387801, 0.448827] | 0.643 [0.612809, 0.672096] | 0.254 [0.227997, 0.281886] |
| 30 | 360 | 2 | 0.943 [0.926863, 0.955747] | 0.937 [0.920205, 0.95045] | 0.813 [0.787652, 0.835952] | 0.934 [0.916891, 0.947788] | 0.655 [0.624994, 0.683819] |
| 30 | 360 | 3 | 0.997 [0.991217, 0.998979] | 0.998 [0.992737, 0.999451] | 0.972 [0.95983, 0.980558] | 0.997 [0.991217, 0.998979] | 0.95 [0.934686, 0.96187] |
| 30 | 360 | 4 | 1 [0.996173, 1] | 1 [0.996173, 1] | 1 [0.996173, 1] | 1 [0.996173, 1] | 0.998 [0.992737, 0.999451] |
| 35 | 420 | 0 | 0.386 [0.356317, 0.416555] | 0.387 [0.357299, 0.417566] | 0.185 [0.162155, 0.210256] | 0.384 [0.354354, 0.414534] | 0.054 [0.0416213, 0.0697922] |
| 35 | 420 | 1 | 0.727 [0.698559, 0.753704] | 0.721 [0.692396, 0.747912] | 0.501 [0.470066, 0.531927] | 0.711 [0.68214, 0.738246] | 0.294 [0.266594, 0.322983] |
| 35 | 420 | 2 | 0.979 [0.96811, 0.986224] | 0.977 [0.965724, 0.984626] | 0.9 [0.879848, 0.917091] | 0.974 [0.962176, 0.982196] | 0.805 [0.779296, 0.82837] |
| 35 | 420 | 3 | 1 [0.996173, 1] | 1 [0.996173, 1] | 0.997 [0.991217, 0.998979] | 1 [0.996173, 1] | 0.988 [0.979143, 0.993122] |
| 35 | 420 | 4 | 1 [0.996173, 1] | 1 [0.996173, 1] | 1 [0.996173, 1] | 1 [0.996173, 1] | 1 [0.996173, 1] |

Weatherhead comparison applies only to plain stationary AR(1) simulations. Weatherhead et al. (1998) formula for monthly data: SD and lag-1 autocorrelation of the monthly noise, trend per year, n* in years. Crossings use linear interpolation inside the tested bracket; no crossing CI.

| Trend (mm/yr) | Weatherhead n* (years) | Empirical AR(1)-OLS 90% crossing |
|---:|---:|---|
| 1 | 60.7409 | above 35 years or not observed |
| 2 | 38.2644 | above 35 years or not observed |
| 3 | 29.2012 | 28.7864 years; linear interpolation; descriptive, no crossing CI |
| 4 | 24.105 | 24.181 years; linear interpolation; descriptive, no crossing CI |

## E4: coasts

### The Battery (8518750)

Record: 1856-01-01 to 2026-10-01; n=1865 observed months; 185 missing calendar months. Relative sea level, datum MSL.

| Method | Trend [95% CI] (mm/yr) | p | Window | n |
|---|---|---:|---|---:|
| Sen (independent-error rank CI) | 2.96226 [2.90454, 3.01901] | N/A | 1856-01-01 to 2026-10-01 | 1865 |
| Naive OLS | 2.9556 [2.89782, 3.01337] | 0 | 1856-01-01 to 2026-10-01 | 1865 |
| Plain Mann-Kendall | 2.96226 [2.90454, 3.01901] | 0 | 1856-01-01 to 2026-10-01 | 1865 |
| Hamed-Rao Mann-Kendall | 2.96226 [2.90454, 3.01901] | 0 | 1856-01-01 to 2026-10-01 | 1865 |
| AR(1)-OLS effective sample size | 2.9556 [2.86985, 3.04135] | 0 | 1856-01-01 to 2026-10-01 | 1865 |
| Seasonal Kendall (period 12) | 2.97143 [2.91045, 3.01987] | 0 | 1856-01-01 to 2026-10-01 | 1865 |

ONI joint trend/harmonics/index fit: lag=0 months; window=1950-01-01 to 2026-09-01; n=921. Amplitude=8.90056 [1.2599, 16.5412] mm/degree C; trend=3.41349 [3.13985, 3.68713] mm/year. R² with index=0.707957; without=0.704102.

- 1997/98: peak=244.332 mm in 1998-02-01; window=1997-01 to 1998-12; n=24; Maximum detrended/deseasonalized monthly anomaly; Descriptive selected maximum; no confidence interval.
- 2015/16: peak=51.6409 mm in 2016-09-01; window=2015-01 to 2016-12; n=24; Maximum detrended/deseasonalized monthly anomaly; Descriptive selected maximum; no confidence interval.

### La Jolla (9410230)

Record: 1924-11-01 to 2026-09-01; n=1188 observed months; 35 missing calendar months. Relative sea level, datum MSL.

| Method | Trend [95% CI] (mm/yr) | p | Window | n |
|---|---|---:|---|---:|
| Sen (independent-error rank CI) | 1.98896 [1.90677, 2.07015] | N/A | 1924-11-01 to 2026-09-01 | 1188 |
| Naive OLS | 2.02976 [1.94255, 2.11697] | 1.4737e-263 | 1924-11-01 to 2026-09-01 | 1188 |
| Plain Mann-Kendall | 1.98896 [1.90677, 2.07015] | 0 | 1924-11-01 to 2026-09-01 | 1188 |
| Hamed-Rao Mann-Kendall | 1.98896 [1.90677, 2.07015] | 0 | 1924-11-01 to 2026-09-01 | 1188 |
| AR(1)-OLS effective sample size | 2.02976 [1.81131, 2.24821] | 7.98805e-44 | 1924-11-01 to 2026-09-01 | 1188 |
| Seasonal Kendall (period 12) | 2 [1.91429, 2.07143] | 0 | 1924-11-01 to 2026-09-01 | 1188 |

ONI joint trend/harmonics/index fit: lag=0 months; window=1950-01-01 to 2026-09-01; n=899. Amplitude=37.8346 [31.8884, 43.7808] mm/degree C; trend=2.07136 [1.85416, 2.28856] mm/year. R² with index=0.809448; without=0.680073.

- 1997/98: peak=206.643 mm in 1997-11-01; window=1997-01 to 1998-12; n=24; Maximum detrended/deseasonalized monthly anomaly; Descriptive selected maximum; no confidence interval.
- 2015/16: peak=164.544 mm in 2015-10-01; window=2015-01 to 2016-12; n=24; Maximum detrended/deseasonalized monthly anomaly; Descriptive selected maximum; no confidence interval.

### San Francisco (9414290)

Record: 1854-07-01 to 2026-10-01; n=2059 observed months; 9 missing calendar months. Relative sea level, datum MSL.

| Method | Trend [95% CI] (mm/yr) | p | Window | n |
|---|---|---:|---|---:|
| Sen (independent-error rank CI) | 1.53223 [1.47892, 1.58541] | N/A | 1854-07-01 to 2026-10-01 | 2059 |
| Naive OLS | 1.53095 [1.47707, 1.58483] | 0 | 1854-07-01 to 2026-10-01 | 2059 |
| Plain Mann-Kendall | 1.53223 [1.47892, 1.58541] | 0 | 1854-07-01 to 2026-10-01 | 2059 |
| Hamed-Rao Mann-Kendall | 1.53223 [1.47892, 1.58541] | 2.64233e-14 | 1854-07-01 to 2026-10-01 | 2059 |
| AR(1)-OLS effective sample size | 1.53095 [1.40452, 1.65738] | 6.20297e-77 | 1854-07-01 to 2026-10-01 | 2059 |
| Seasonal Kendall (period 12) | 1.53488 [1.48684, 1.58667] | 0 | 1854-07-01 to 2026-10-01 | 2059 |

ONI joint trend/harmonics/index fit: lag=0 months; window=1950-01-01 to 2026-09-01; n=912. Amplitude=39.7435 [31.9749, 47.5122] mm/degree C; trend=1.97452 [1.69503, 2.25401] mm/year. R² with index=0.608843; without=0.464156.

- 1997/98: peak=297.913 mm in 1998-02-01; window=1997-01 to 1998-12; n=24; Maximum detrended/deseasonalized monthly anomaly; Descriptive selected maximum; no confidence interval.
- 2015/16: peak=150.231 mm in 2015-10-01; window=2015-01 to 2016-12; n=24; Maximum detrended/deseasonalized monthly anomaly; Descriptive selected maximum; no confidence interval.

### Battery cool-season comparison

Complete 7-month Oct-Apr detrended/deseasonalized anomalies; DJF ONI >=0.5 C. Window: 1949-10-01 to 2026-04-01; n=77 complete winters.

El Nino winters: 12.3973 [-14.2028, 38.9974] mm, n=25. Other winters: -2.64675 [-13.4059, 8.11245] mm, n=52.

Difference: 15.044 [-13.3687, 43.4567] mm (Welch independent-winter CI); Welch t=1.07779, df=32.5592, p=0.289046. Permutation p=0.1941, 9999 permutations, seed=20261114.

## Method notes

- Two-sided alpha=0.05. No seasonal forcing, missing data, or index contamination.
- Same noise realizations reused across trend settings; binomial CIs are per setting.
- Weatherhead et al. (1998) formula uses the SD and lag-1 autocorrelation of the monthly noise, the trend per year, and gives n* in years (no cadence conversion).
- Formula comparison is restricted to this plain stationary AR(1) case; no fit to literature.
- Gauge records are relative sea level on datum MSL; no vertical-land-motion or GIA correction.
- Nonseasonal trend methods use deseasonalized monthly values; seasonal Kendall uses raw monthly values.
- Peaks are observed monthly maxima after full-record climatology and linear detrending; no inferential CI for a selected maximum.
- Hamed-Rao p-values compress missing months; gap counts are reported. Sen intervals are independent-error rank intervals.

## Complete numeric record

This appendix includes every scalar result and diagnostic. Per-cell E2 fields are in the named NetCDF files; their arrays include coefficient, CI, n and effective n at each cell. Diagnostic counts, R², rho, observed peaks, timings and configuration constants have no inferential CI unless one is explicitly supplied.

```json
{
  "noaa": {
    "datum": "MSL",
    "units": "mm",
    "gauges": {
      "8518750": {
        "name": "The Battery",
        "window": [
          "1856-01-01",
          "2026-10-01"
        ],
        "n": 1865,
        "source": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter",
        "missing_months": 185
      },
      "9410230": {
        "name": "La Jolla",
        "window": [
          "1924-11-01",
          "2026-09-01"
        ],
        "n": 1188,
        "source": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter",
        "missing_months": 35
      },
      "9414290": {
        "name": "San Francisco",
        "window": [
          "1854-07-01",
          "2026-10-01"
        ],
        "n": 2059,
        "source": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter",
        "missing_months": 9
      }
    },
    "oni": {
      "window": [
        "1950-01-01",
        "2026-09-01"
      ],
      "n": 921,
      "source": "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt",
      "units": "degree C",
      "time_assignment": "central month; DJF is January of the stated year"
    }
  },
  "preprocess": {
    "rows": 10682,
    "series": [
      "gauge_the_battery",
      "gauge_la_jolla",
      "gauge_san_francisco"
    ],
    "gmsl_check": "skipped: NASA data not present"
  },
  "e1": {
    "experiment": "E1",
    "seed": 20261114,
    "noise": {
      "sigma_mm": 61.3021355359611,
      "phi": 0.6911677411517617,
      "method": "Median across gauge residual estimates; monthly climatology and OLS trend removed",
      "gauge_estimates": [
        {
          "station": "8518750",
          "name": "The Battery",
          "window": [
            "1856-01-01",
            "2026-10-01"
          ],
          "n": 1865,
          "sigma_mm": 61.3021355359611,
          "phi": 0.37488578020187435
        },
        {
          "station": "9410230",
          "name": "La Jolla",
          "window": [
            "1924-11-01",
            "2026-09-01"
          ],
          "n": 1188,
          "sigma_mm": 45.290352694066925,
          "phi": 0.7225064165786146
        },
        {
          "station": "9414290",
          "name": "San Francisco",
          "window": [
            "1854-07-01",
            "2026-10-01"
          ],
          "n": 2059,
          "sigma_mm": 61.79601763327969,
          "phi": 0.6911677411517617
        }
      ],
      "fallback": false
    },
    "settings": [
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "naive_ols",
        "rejections": 405,
        "metric": "false_positive_rate",
        "estimate": 0.405,
        "ci95": [
          0.37499439177359234,
          0.43573269233866313
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "plain_mk",
        "rejections": 384,
        "metric": "false_positive_rate",
        "estimate": 0.384,
        "ci95": [
          0.35435414144032196,
          0.4145336665283268
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "hamed_rao_mk",
        "rejections": 184,
        "metric": "false_positive_rate",
        "estimate": 0.184,
        "ci95": [
          0.16120869057645773,
          0.20920982078641312
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "seasonal_kendall",
        "rejections": 354,
        "metric": "false_positive_rate",
        "estimate": 0.354,
        "ci95": [
          0.32497103040683056,
          0.38414638307095145
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "ar1_ols",
        "rejections": 70,
        "metric": "false_positive_rate",
        "estimate": 0.07,
        "ci95": [
          0.05577636414629404,
          0.08751464815128336
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "naive_ols",
        "rejections": 411,
        "metric": "power",
        "estimate": 0.411,
        "ci95": [
          0.3809022198018245,
          0.4417789432086042
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "plain_mk",
        "rejections": 384,
        "metric": "power",
        "estimate": 0.384,
        "ci95": [
          0.35435414144032196,
          0.4145336665283268
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "hamed_rao_mk",
        "rejections": 200,
        "metric": "power",
        "estimate": 0.2,
        "ci95": [
          0.17637709044319852,
          0.22591896464813463
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "seasonal_kendall",
        "rejections": 366,
        "metric": "power",
        "estimate": 0.366,
        "ci95": [
          0.3367094419466035,
          0.3963161293275252
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "ar1_ols",
        "rejections": 82,
        "metric": "power",
        "estimate": 0.082,
        "ci95": [
          0.06655195342021952,
          0.10064721667370458
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "naive_ols",
        "rejections": 452,
        "metric": "power",
        "estimate": 0.452,
        "ci95": [
          0.42139559401833404,
          0.4829717747962793
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "plain_mk",
        "rejections": 423,
        "metric": "power",
        "estimate": 0.423,
        "ci95": [
          0.3927318137578076,
          0.4538575070489678
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "hamed_rao_mk",
        "rejections": 234,
        "metric": "power",
        "estimate": 0.234,
        "ci95": [
          0.20880800256185078,
          0.2612278329524646
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "seasonal_kendall",
        "rejections": 398,
        "metric": "power",
        "estimate": 0.398,
        "ci95": [
          0.36810785286312253,
          0.4286728058679308
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "ar1_ols",
        "rejections": 99,
        "metric": "power",
        "estimate": 0.099,
        "ci95": [
          0.08199544136866538,
          0.11907361893674984
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "naive_ols",
        "rejections": 496,
        "metric": "power",
        "estimate": 0.496,
        "ci95": [
          0.46508589340292905,
          0.5269447206649553
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "plain_mk",
        "rejections": 480,
        "metric": "power",
        "estimate": 0.48,
        "ci95": [
          0.44917079499694124,
          0.510982275342481
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "hamed_rao_mk",
        "rejections": 284,
        "metric": "power",
        "estimate": 0.284,
        "ci95": [
          0.2569190250903582,
          0.3127341345754016
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "seasonal_kendall",
        "rejections": 445,
        "metric": "power",
        "estimate": 0.445,
        "ci95": [
          0.41446705005753576,
          0.4759538933758753
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "ar1_ols",
        "rejections": 133,
        "metric": "power",
        "estimate": 0.133,
        "ci95": [
          0.11335116065727396,
          0.15545768007112354
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "naive_ols",
        "rejections": 545,
        "metric": "power",
        "estimate": 0.545,
        "ci95": [
          0.5140224377348876,
          0.5756331540014126
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "plain_mk",
        "rejections": 534,
        "metric": "power",
        "estimate": 0.534,
        "ci95": [
          0.5030108102327143,
          0.5647289701902679
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "hamed_rao_mk",
        "rejections": 341,
        "metric": "power",
        "estimate": 0.341,
        "ci95": [
          0.31227731829126676,
          0.37093959090713985
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "seasonal_kendall",
        "rejections": 503,
        "metric": "power",
        "estimate": 0.503,
        "ci95": [
          0.4720586747142764,
          0.5339183647348104
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 10,
        "n_months": 120,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "ar1_ols",
        "rejections": 188,
        "metric": "power",
        "estimate": 0.188,
        "ci95": [
          0.16499470988376858,
          0.21339318741121788
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "naive_ols",
        "rejections": 384,
        "metric": "false_positive_rate",
        "estimate": 0.384,
        "ci95": [
          0.35435414144032196,
          0.4145336665283268
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "plain_mk",
        "rejections": 371,
        "metric": "false_positive_rate",
        "estimate": 0.371,
        "ci95": [
          0.341606326344111,
          0.40138097734516226
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "hamed_rao_mk",
        "rejections": 185,
        "metric": "false_positive_rate",
        "estimate": 0.185,
        "ci95": [
          0.16215480378454947,
          0.2102560540613503
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "seasonal_kendall",
        "rejections": 346,
        "metric": "false_positive_rate",
        "estimate": 0.346,
        "ci95": [
          0.3171566601020642,
          0.3760219815114867
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "ar1_ols",
        "rejections": 70,
        "metric": "false_positive_rate",
        "estimate": 0.07,
        "ci95": [
          0.05577636414629404,
          0.08751464815128336
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "naive_ols",
        "rejections": 434,
        "metric": "power",
        "estimate": 0.434,
        "ci95": [
          0.40359177593584417,
          0.4649133561842491
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "plain_mk",
        "rejections": 416,
        "metric": "power",
        "estimate": 0.416,
        "ci95": [
          0.38582896762102037,
          0.44681392780455287
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "hamed_rao_mk",
        "rejections": 200,
        "metric": "power",
        "estimate": 0.2,
        "ci95": [
          0.17637709044319852,
          0.22591896464813463
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "seasonal_kendall",
        "rejections": 392,
        "metric": "power",
        "estimate": 0.392,
        "ci95": [
          0.3622102251883648,
          0.42261635464451514
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "ar1_ols",
        "rejections": 79,
        "metric": "power",
        "estimate": 0.079,
        "ci95": [
          0.06384721576082919,
          0.09737491488400823
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "naive_ols",
        "rejections": 542,
        "metric": "power",
        "estimate": 0.542,
        "ci95": [
          0.5110177730722398,
          0.5726607792149736
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "plain_mk",
        "rejections": 527,
        "metric": "power",
        "estimate": 0.527,
        "ci95": [
          0.4960112345098614,
          0.5577821205319188
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "hamed_rao_mk",
        "rejections": 306,
        "metric": "power",
        "estimate": 0.306,
        "ci95": [
          0.2782254333203639,
          0.3352593489720314
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "seasonal_kendall",
        "rejections": 511,
        "metric": "power",
        "estimate": 0.511,
        "ci95": [
          0.4800349634365892,
          0.5418808478767286
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "ar1_ols",
        "rejections": 125,
        "metric": "power",
        "estimate": 0.125,
        "ci95": [
          0.10592623063520473,
          0.14694383822896162
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "naive_ols",
        "rejections": 672,
        "metric": "power",
        "estimate": 0.672,
        "ci95": [
          0.6422916335335495,
          0.7003919615474198
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "plain_mk",
        "rejections": 654,
        "metric": "power",
        "estimate": 0.654,
        "ci95": [
          0.6239780184885133,
          0.6828433398979359
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "hamed_rao_mk",
        "rejections": 435,
        "metric": "power",
        "estimate": 0.435,
        "ci95": [
          0.4045798065188989,
          0.4659176720842233
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "seasonal_kendall",
        "rejections": 635,
        "metric": "power",
        "estimate": 0.635,
        "ci95": [
          0.6046972526360328,
          0.6642695225728674
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "ar1_ols",
        "rejections": 226,
        "metric": "power",
        "estimate": 0.226,
        "ci95": [
          0.2011546846733466,
          0.25294237897673766
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "naive_ols",
        "rejections": 787,
        "metric": "power",
        "estimate": 0.787,
        "ci95": [
          0.7605503974702781,
          0.8112530431590133
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "plain_mk",
        "rejections": 779,
        "metric": "power",
        "estimate": 0.779,
        "ci95": [
          0.7522428263299143,
          0.803621842435146
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "hamed_rao_mk",
        "rejections": 587,
        "metric": "power",
        "estimate": 0.587,
        "ci95": [
          0.5562066759628382,
          0.6171274680606752
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "seasonal_kendall",
        "rejections": 759,
        "metric": "power",
        "estimate": 0.759,
        "ci95": [
          0.7315330470912914,
          0.784484692013191
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 15,
        "n_months": 180,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "ar1_ols",
        "rejections": 371,
        "metric": "power",
        "estimate": 0.371,
        "ci95": [
          0.341606326344111,
          0.40138097734516226
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "naive_ols",
        "rejections": 389,
        "metric": "false_positive_rate",
        "estimate": 0.389,
        "ci95": [
          0.35926319596566997,
          0.4195863444181233
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "plain_mk",
        "rejections": 390,
        "metric": "false_positive_rate",
        "estimate": 0.39,
        "ci95": [
          0.3602454063696288,
          0.4205964804971933
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "hamed_rao_mk",
        "rejections": 160,
        "metric": "false_positive_rate",
        "estimate": 0.16,
        "ci95": [
          0.13858526208349012,
          0.1840169336866874
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "seasonal_kendall",
        "rejections": 359,
        "metric": "false_positive_rate",
        "estimate": 0.359,
        "ci95": [
          0.32985959695418837,
          0.38921954893873817
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "ar1_ols",
        "rejections": 50,
        "metric": "false_positive_rate",
        "estimate": 0.05,
        "ci95": [
          0.03813026239274882,
          0.06531382024425081
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "naive_ols",
        "rejections": 461,
        "metric": "power",
        "estimate": 0.461,
        "ci95": [
          0.4303127166140634,
          0.49198577054780995
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "plain_mk",
        "rejections": 450,
        "metric": "power",
        "estimate": 0.45,
        "ci95": [
          0.4194153840742968,
          0.4809672917742588
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "hamed_rao_mk",
        "rejections": 239,
        "metric": "power",
        "estimate": 0.239,
        "ci95": [
          0.2135979397357572,
          0.2663996281937026
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "seasonal_kendall",
        "rejections": 435,
        "metric": "power",
        "estimate": 0.435,
        "ci95": [
          0.4045798065188989,
          0.4659176720842233
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "ar1_ols",
        "rejections": 89,
        "metric": "power",
        "estimate": 0.089,
        "ci95": [
          0.07288824391300744,
          0.10825735156211885
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "naive_ols",
        "rejections": 679,
        "metric": "power",
        "estimate": 0.679,
        "ci95": [
          0.6494265062245327,
          0.7072035142376386
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "plain_mk",
        "rejections": 655,
        "metric": "power",
        "estimate": 0.655,
        "ci95": [
          0.6249942093571865,
          0.6838194955122914
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "hamed_rao_mk",
        "rejections": 429,
        "metric": "power",
        "estimate": 0.429,
        "ci95": [
          0.3986535230179055,
          0.45988987668704334
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "seasonal_kendall",
        "rejections": 639,
        "metric": "power",
        "estimate": 0.639,
        "ci95": [
          0.608752162967835,
          0.6681839981731807
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "ar1_ols",
        "rejections": 229,
        "metric": "power",
        "estimate": 0.229,
        "ci95": [
          0.20402312975052514,
          0.25605097334864574
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "naive_ols",
        "rejections": 860,
        "metric": "power",
        "estimate": 0.86,
        "ci95": [
          0.8371133085163773,
          0.8801314253740229
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "plain_mk",
        "rejections": 845,
        "metric": "power",
        "estimate": 0.845,
        "ci95": [
          0.821253161260159,
          0.866106375384808
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "hamed_rao_mk",
        "rejections": 662,
        "metric": "power",
        "estimate": 0.662,
        "ci95": [
          0.6321115753976023,
          0.6906485548530779
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "seasonal_kendall",
        "rejections": 839,
        "metric": "power",
        "estimate": 0.839,
        "ci95": [
          0.8149299903062807,
          0.860475467440513
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "ar1_ols",
        "rejections": 460,
        "metric": "power",
        "estimate": 0.46,
        "ci95": [
          0.42932142688110647,
          0.49098471379773795
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "naive_ols",
        "rejections": 967,
        "metric": "power",
        "estimate": 0.967,
        "ci95": [
          0.9540187355329184,
          0.9764070720415732
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "plain_mk",
        "rejections": 963,
        "metric": "power",
        "estimate": 0.963,
        "ci95": [
          0.9494176025179306,
          0.9730388191244452
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "hamed_rao_mk",
        "rejections": 845,
        "metric": "power",
        "estimate": 0.845,
        "ci95": [
          0.821253161260159,
          0.866106375384808
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "seasonal_kendall",
        "rejections": 956,
        "metric": "power",
        "estimate": 0.956,
        "ci95": [
          0.9414482108495923,
          0.9670617854115815
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 20,
        "n_months": 240,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "ar1_ols",
        "rejections": 706,
        "metric": "power",
        "estimate": 0.706,
        "ci95": [
          0.677017384524264,
          0.7334059909796873
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "naive_ols",
        "rejections": 389,
        "metric": "false_positive_rate",
        "estimate": 0.389,
        "ci95": [
          0.35926319596566997,
          0.4195863444181233
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "plain_mk",
        "rejections": 378,
        "metric": "false_positive_rate",
        "estimate": 0.378,
        "ci95": [
          0.34846769603702693,
          0.4084660330334485
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "hamed_rao_mk",
        "rejections": 165,
        "metric": "false_positive_rate",
        "estimate": 0.165,
        "ci95": [
          0.14328467985555532,
          0.18927924832976667
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "seasonal_kendall",
        "rejections": 366,
        "metric": "false_positive_rate",
        "estimate": 0.366,
        "ci95": [
          0.3367094419466035,
          0.3963161293275252
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "ar1_ols",
        "rejections": 53,
        "metric": "false_positive_rate",
        "estimate": 0.053,
        "ci95": [
          0.04074650524859452,
          0.06867461683749176
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "naive_ols",
        "rejections": 535,
        "metric": "power",
        "estimate": 0.535,
        "ci95": [
          0.5040112456567101,
          0.5657208812493011
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "plain_mk",
        "rejections": 527,
        "metric": "power",
        "estimate": 0.527,
        "ci95": [
          0.4960112345098614,
          0.5577821205319188
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "hamed_rao_mk",
        "rejections": 312,
        "metric": "power",
        "estimate": 0.312,
        "ci95": [
          0.2840496860924683,
          0.3413891750981004
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "seasonal_kendall",
        "rejections": 521,
        "metric": "power",
        "estimate": 0.521,
        "ci95": [
          0.49001642660541767,
          0.5518228495381892
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "ar1_ols",
        "rejections": 162,
        "metric": "power",
        "estimate": 0.162,
        "ci95": [
          0.1404641118483431,
          0.18612277688789222
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "naive_ols",
        "rejections": 833,
        "metric": "power",
        "estimate": 0.833,
        "ci95": [
          0.8086179403533302,
          0.85483343849529
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "plain_mk",
        "rejections": 829,
        "metric": "power",
        "estimate": 0.829,
        "ci95": [
          0.8044158480970535,
          0.8510661448194513
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "hamed_rao_mk",
        "rejections": 612,
        "metric": "power",
        "estimate": 0.612,
        "ci95": [
          0.5814239245764211,
          0.6417188815228144
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "seasonal_kendall",
        "rejections": 820,
        "metric": "power",
        "estimate": 0.82,
        "ci95": [
          0.7949777670979878,
          0.8425731074712568
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "ar1_ols",
        "rejections": 409,
        "metric": "power",
        "estimate": 0.409,
        "ci95": [
          0.37893242495569907,
          0.4397640450886719
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "naive_ols",
        "rejections": 969,
        "metric": "power",
        "estimate": 0.969,
        "ci95": [
          0.9563345039877078,
          0.9780759965528414
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "plain_mk",
        "rejections": 966,
        "metric": "power",
        "estimate": 0.966,
        "ci95": [
          0.9528648097546889,
          0.9755686513367737
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "hamed_rao_mk",
        "rejections": 877,
        "metric": "power",
        "estimate": 0.877,
        "ci95": [
          0.8551887673529645,
          0.8959258567489271
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "seasonal_kendall",
        "rejections": 962,
        "metric": "power",
        "estimate": 0.962,
        "ci95": [
          0.9482730796686497,
          0.9721909954906974
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "ar1_ols",
        "rejections": 744,
        "metric": "power",
        "estimate": 0.744,
        "ci95": [
          0.7160527265828488,
          0.7700798152762004
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "naive_ols",
        "rejections": 998,
        "metric": "power",
        "estimate": 0.998,
        "ci95": [
          0.9927371921365079,
          0.9994513564118793
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "plain_mk",
        "rejections": 997,
        "metric": "power",
        "estimate": 0.997,
        "ci95": [
          0.9912169859464969,
          0.9989792161188614
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "hamed_rao_mk",
        "rejections": 974,
        "metric": "power",
        "estimate": 0.974,
        "ci95": [
          0.9621761711573101,
          0.9821960617983837
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "seasonal_kendall",
        "rejections": 996,
        "metric": "power",
        "estimate": 0.996,
        "ci95": [
          0.9897604437227377,
          0.9984434118595916
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 25,
        "n_months": 300,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "ar1_ols",
        "rejections": 938,
        "metric": "power",
        "estimate": 0.938,
        "ci95": [
          0.9213119396866343,
          0.9513358198800193
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "naive_ols",
        "rejections": 407,
        "metric": "false_positive_rate",
        "estimate": 0.407,
        "ci95": [
          0.3769631485524506,
          0.4377486285258626
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "plain_mk",
        "rejections": 409,
        "metric": "false_positive_rate",
        "estimate": 0.409,
        "ci95": [
          0.37893242495569907,
          0.4397640450886719
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "hamed_rao_mk",
        "rejections": 175,
        "metric": "false_positive_rate",
        "estimate": 0.175,
        "ci95": [
          0.1527057476303958,
          0.19978164538521503
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "seasonal_kendall",
        "rejections": 403,
        "metric": "false_positive_rate",
        "estimate": 0.403,
        "ci95": [
          0.37302615583096504,
          0.4337162353152327
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "ar1_ols",
        "rejections": 59,
        "metric": "false_positive_rate",
        "estimate": 0.059,
        "ci95": [
          0.04601429821280047,
          0.07536090277145915
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "naive_ols",
        "rejections": 659,
        "metric": "power",
        "estimate": 0.659,
        "ci95": [
          0.6290604090928602,
          0.6877226817087334
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "plain_mk",
        "rejections": 647,
        "metric": "power",
        "estimate": 0.647,
        "ci95": [
          0.6168686714441486,
          0.6760062615610983
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "hamed_rao_mk",
        "rejections": 418,
        "metric": "power",
        "estimate": 0.418,
        "ci95": [
          0.3878005681433438,
          0.4488270202482872
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "seasonal_kendall",
        "rejections": 643,
        "metric": "power",
        "estimate": 0.643,
        "ci95": [
          0.6128092971223535,
          0.6720962499507777
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "ar1_ols",
        "rejections": 254,
        "metric": "power",
        "estimate": 0.254,
        "ci95": [
          0.2279970750986118,
          0.2818856900762812
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "naive_ols",
        "rejections": 943,
        "metric": "power",
        "estimate": 0.943,
        "ci95": [
          0.9268629323405141,
          0.9557465596412841
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "plain_mk",
        "rejections": 937,
        "metric": "power",
        "estimate": 0.937,
        "ci95": [
          0.920205076295354,
          0.9504503367882711
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "hamed_rao_mk",
        "rejections": 813,
        "metric": "power",
        "estimate": 0.813,
        "ci95": [
          0.7876522642371055,
          0.8359521849509368
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "seasonal_kendall",
        "rejections": 934,
        "metric": "power",
        "estimate": 0.934,
        "ci95": [
          0.9168907240940241,
          0.9477876495405142
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "ar1_ols",
        "rejections": 655,
        "metric": "power",
        "estimate": 0.655,
        "ci95": [
          0.6249942093571865,
          0.6838194955122914
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "naive_ols",
        "rejections": 997,
        "metric": "power",
        "estimate": 0.997,
        "ci95": [
          0.9912169859464969,
          0.9989792161188614
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "plain_mk",
        "rejections": 998,
        "metric": "power",
        "estimate": 0.998,
        "ci95": [
          0.9927371921365079,
          0.9994513564118793
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "hamed_rao_mk",
        "rejections": 972,
        "metric": "power",
        "estimate": 0.972,
        "ci95": [
          0.9598298168024069,
          0.9805577231872291
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "seasonal_kendall",
        "rejections": 997,
        "metric": "power",
        "estimate": 0.997,
        "ci95": [
          0.9912169859464969,
          0.9989792161188614
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "ar1_ols",
        "rejections": 950,
        "metric": "power",
        "estimate": 0.95,
        "ci95": [
          0.9346861797557492,
          0.9618697376072513
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "naive_ols",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "plain_mk",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "hamed_rao_mk",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "seasonal_kendall",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 30,
        "n_months": 360,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "ar1_ols",
        "rejections": 998,
        "metric": "power",
        "estimate": 0.998,
        "ci95": [
          0.9927371921365079,
          0.9994513564118793
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "naive_ols",
        "rejections": 386,
        "metric": "false_positive_rate",
        "estimate": 0.386,
        "ci95": [
          0.35631736299485905,
          0.41655513793984755
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "plain_mk",
        "rejections": 387,
        "metric": "false_positive_rate",
        "estimate": 0.387,
        "ci95": [
          0.35729917409070144,
          0.417565673327034
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "hamed_rao_mk",
        "rejections": 185,
        "metric": "false_positive_rate",
        "estimate": 0.185,
        "ci95": [
          0.16215480378454947,
          0.2102560540613503
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "seasonal_kendall",
        "rejections": 384,
        "metric": "false_positive_rate",
        "estimate": 0.384,
        "ci95": [
          0.35435414144032196,
          0.4145336665283268
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 0.0,
        "method": "ar1_ols",
        "rejections": 54,
        "metric": "false_positive_rate",
        "estimate": 0.054,
        "ci95": [
          0.04162131372306273,
          0.06979215484605245
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "naive_ols",
        "rejections": 727,
        "metric": "power",
        "estimate": 0.727,
        "ci95": [
          0.6985586005647291,
          0.7537040510828288
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "plain_mk",
        "rejections": 721,
        "metric": "power",
        "estimate": 0.721,
        "ci95": [
          0.6923963660323501,
          0.7479122067170344
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "hamed_rao_mk",
        "rejections": 501,
        "metric": "power",
        "estimate": 0.501,
        "ci95": [
          0.47006583523375295,
          0.5319265112492759
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "seasonal_kendall",
        "rejections": 711,
        "metric": "power",
        "estimate": 0.711,
        "ci95": [
          0.6821395598954265,
          0.7382455480236692
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 1.0,
        "method": "ar1_ols",
        "rejections": 294,
        "metric": "power",
        "estimate": 0.294,
        "ci95": [
          0.2665940090203127,
          0.3229826154757359
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "naive_ols",
        "rejections": 979,
        "metric": "power",
        "estimate": 0.979,
        "ci95": [
          0.9681097049387625,
          0.9862242604320758
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "plain_mk",
        "rejections": 977,
        "metric": "power",
        "estimate": 0.977,
        "ci95": [
          0.9657235493377733,
          0.9846257230670071
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "hamed_rao_mk",
        "rejections": 900,
        "metric": "power",
        "estimate": 0.9,
        "ci95": [
          0.8798480368046516,
          0.9170905564069044
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "seasonal_kendall",
        "rejections": 974,
        "metric": "power",
        "estimate": 0.974,
        "ci95": [
          0.9621761711573101,
          0.9821960617983837
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 2.0,
        "method": "ar1_ols",
        "rejections": 805,
        "metric": "power",
        "estimate": 0.805,
        "ci95": [
          0.77929577121571,
          0.8283699061081016
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "naive_ols",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "plain_mk",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "hamed_rao_mk",
        "rejections": 997,
        "metric": "power",
        "estimate": 0.997,
        "ci95": [
          0.9912169859464969,
          0.9989792161188614
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "seasonal_kendall",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 3.0,
        "method": "ar1_ols",
        "rejections": 988,
        "metric": "power",
        "estimate": 0.988,
        "ci95": [
          0.9791427315245017,
          0.9931223521935965
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "naive_ols",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "plain_mk",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "hamed_rao_mk",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "seasonal_kendall",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      },
      {
        "window_years": 35,
        "n_months": 420,
        "n": 1000,
        "true_trend_mm_yr": 4.0,
        "method": "ar1_ols",
        "rejections": 1000,
        "metric": "power",
        "estimate": 1.0,
        "ci95": [
          0.996173241514445,
          1.0
        ],
        "ci_method": "Binomial Wilson"
      }
    ],
    "weatherhead": [
      {
        "trend_mm_yr": 1,
        "method": "Plain stationary AR(1) only",
        "empirical_crossing": {
          "years": null,
          "status": "above 35 years or not observed",
          "bracket_years": [
            35,
            null
          ]
        },
        "weatherhead_years": 60.74087426135442,
        "n_per_setting": 1000,
        "ci": null
      },
      {
        "trend_mm_yr": 2,
        "method": "Plain stationary AR(1) only",
        "empirical_crossing": {
          "years": null,
          "status": "above 35 years or not observed",
          "bracket_years": [
            35,
            null
          ]
        },
        "weatherhead_years": 38.26435303544907,
        "n_per_setting": 1000,
        "ci": null
      },
      {
        "trend_mm_yr": 3,
        "method": "Plain stationary AR(1) only",
        "empirical_crossing": {
          "years": 28.786407766990294,
          "status": "linear interpolation; descriptive, no crossing CI",
          "bracket_years": [
            25,
            30
          ]
        },
        "weatherhead_years": 29.201166601178247,
        "n_per_setting": 1000,
        "ci": null
      },
      {
        "trend_mm_yr": 4,
        "method": "Plain stationary AR(1) only",
        "empirical_crossing": {
          "years": 24.181034482758623,
          "status": "linear interpolation; descriptive, no crossing CI",
          "bracket_years": [
            20,
            25
          ]
        },
        "weatherhead_years": 24.105031924985536,
        "n_per_setting": 1000,
        "ci": null
      }
    ],
    "elapsed_seconds": 19.148012800025754,
    "under_ten_minutes": true,
    "notes": [
      "Two-sided alpha=0.05. No seasonal forcing, missing data, or index contamination.",
      "Same noise realizations reused across trend settings; binomial CIs are per setting.",
      "Weatherhead et al. (1998) formula uses the SD and lag-1 autocorrelation of the monthly noise, the trend per year, and gives n* in years (no cadence conversion).",
      "Formula comparison is restricted to this plain stationary AR(1) case; no fit to literature."
    ]
  },
  "e4": {
    "experiment": "E4",
    "nasa_enabled": false,
    "gauges": {
      "8518750": {
        "name": "The Battery",
        "window": [
          "1856-01-01",
          "2026-10-01"
        ],
        "n": 1865,
        "missing_months": 185,
        "trends": [
          {
            "window": [
              "1856-01-01",
              "2026-10-01"
            ],
            "n": 1865,
            "method": "Sen (independent-error rank CI)",
            "trend_mm_yr": 2.962261938287181,
            "ci95_mm_yr": [
              2.9045357033404837,
              3.0190082577390878
            ]
          },
          {
            "window": [
              "1856-01-01",
              "2026-10-01"
            ],
            "n": 1865,
            "method": "Naive OLS",
            "trend_mm_yr": 2.9555983152518426,
            "ci95_mm_yr": [
              2.8978225436116403,
              3.013374086892045
            ],
            "se_mm_yr": 0.029458824964953452,
            "p": 0.0,
            "rho": 0.37488578020187435,
            "n_eff": 1865.0,
            "r2": 0.8438268972273425
          },
          {
            "window": [
              "1856-01-01",
              "2026-10-01"
            ],
            "n": 1865,
            "method": "Plain Mann-Kendall",
            "trend_mm_yr": 2.962261938287181,
            "ci95_mm_yr": [
              2.9045357033404837,
              3.0190082577390878
            ],
            "p": 0.0,
            "z": 49.626576825843806,
            "statistic_s": 1332864.0,
            "ci_method": "Sen rank CI; independent errors (not Hamed-Rao adjusted)",
            "missing_months": 185
          },
          {
            "window": [
              "1856-01-01",
              "2026-10-01"
            ],
            "n": 1865,
            "method": "Hamed-Rao Mann-Kendall",
            "trend_mm_yr": 2.962261938287181,
            "ci95_mm_yr": [
              2.9045357033404837,
              3.0190082577390878
            ],
            "p": 0.0,
            "z": 24.1674976647576,
            "statistic_s": 1332864.0,
            "ci_method": "Sen rank CI; independent errors (not Hamed-Rao adjusted)",
            "missing_months": 185
          },
          {
            "window": [
              "1856-01-01",
              "2026-10-01"
            ],
            "n": 1865,
            "method": "AR(1)-OLS effective sample size",
            "trend_mm_yr": 2.9555983152518426,
            "ci95_mm_yr": [
              2.869847365737263,
              3.041349264766422
            ],
            "se_mm_yr": 0.04368869185324101,
            "p": 0.0,
            "rho": 0.37488578020187435,
            "n_eff": 847.9526348380186,
            "r2": 0.8438268972273425
          },
          {
            "window": [
              "1856-01-01",
              "2026-10-01"
            ],
            "n": 1865,
            "method": "Seasonal Kendall (period 12)",
            "trend_mm_yr": 2.9714285714285715,
            "ci95_mm_yr": [
              2.91044776119403,
              3.019867549668874
            ],
            "p": 0.0,
            "z": 49.53430150437235,
            "statistic_s": 111343.0,
            "ci_method": "Seasonal rank CI; independent years",
            "missing_months": 185
          }
        ],
        "oni_fit": {
          "window": [
            "1950-01-01",
            "2026-09-01"
          ],
          "n": 921,
          "method": "Joint trend + two harmonics + index; AR(1) CI",
          "lag_months": 0,
          "trend_mm_yr": 3.413487756162319,
          "ci95_mm_yr": [
            3.1398456921740814,
            3.6871298201505565
          ],
          "index_coefficient": 8.90055987032846,
          "index_ci95": [
            1.259902378815542,
            16.541217361841376
          ],
          "r2_with_index": 0.7079569608152398,
          "r2_without_index": 0.7041022710871911,
          "rho": 0.39395433003349123,
          "n_eff": 400.42062355496546,
          "index_coefficient_units": "mm per degree C ONI"
        },
        "peaks": [
          {
            "event": "1997/98",
            "requested_window": [
              "1997-01",
              "1998-12"
            ],
            "window": [
              "1997-01-01",
              "1998-12-01"
            ],
            "n": 24,
            "method": "Maximum detrended/deseasonalized monthly anomaly",
            "peak_mm": 244.33178711654446,
            "peak_month": "1998-02-01",
            "ci95": null,
            "ci_note": "Descriptive selected maximum; no confidence interval"
          },
          {
            "event": "2015/16",
            "requested_window": [
              "2015-01",
              "2016-12"
            ],
            "window": [
              "2015-01-01",
              "2016-12-01"
            ],
            "n": 24,
            "method": "Maximum detrended/deseasonalized monthly anomaly",
            "peak_mm": 51.64091346200195,
            "peak_month": "2016-09-01",
            "ci95": null,
            "ci_note": "Descriptive selected maximum; no confidence interval"
          }
        ]
      },
      "9410230": {
        "name": "La Jolla",
        "window": [
          "1924-11-01",
          "2026-09-01"
        ],
        "n": 1188,
        "missing_months": 35,
        "trends": [
          {
            "window": [
              "1924-11-01",
              "2026-09-01"
            ],
            "n": 1188,
            "method": "Sen (independent-error rank CI)",
            "trend_mm_yr": 1.9889617122941505,
            "ci95_mm_yr": [
              1.906768267300529,
              2.0701548821548825
            ]
          },
          {
            "window": [
              "1924-11-01",
              "2026-09-01"
            ],
            "n": 1188,
            "method": "Naive OLS",
            "trend_mm_yr": 2.0297572463342055,
            "ci95_mm_yr": [
              1.9425494497692044,
              2.1169650428992064
            ],
            "se_mm_yr": 0.044449183484689056,
            "p": 1.4736951760398451e-263,
            "rho": 0.7225064165786146,
            "n_eff": 1188.0,
            "r2": 0.6374487872133735
          },
          {
            "window": [
              "1924-11-01",
              "2026-09-01"
            ],
            "n": 1188,
            "method": "Plain Mann-Kendall",
            "trend_mm_yr": 1.9889617122941505,
            "ci95_mm_yr": [
              1.906768267300529,
              2.0701548821548825
            ],
            "p": 0.0,
            "z": 31.640110716242024,
            "statistic_s": 432131.0,
            "ci_method": "Sen rank CI; independent errors (not Hamed-Rao adjusted)",
            "missing_months": 35
          },
          {
            "window": [
              "1924-11-01",
              "2026-09-01"
            ],
            "n": 1188,
            "method": "Hamed-Rao Mann-Kendall",
            "trend_mm_yr": 1.9889617122941505,
            "ci95_mm_yr": [
              1.906768267300529,
              2.0701548821548825
            ],
            "p": 0.0,
            "z": 12.99666768169729,
            "statistic_s": 432131.0,
            "ci_method": "Sen rank CI; independent errors (not Hamed-Rao adjusted)",
            "missing_months": 35
          },
          {
            "window": [
              "1924-11-01",
              "2026-09-01"
            ],
            "n": 1188,
            "method": "AR(1)-OLS effective sample size",
            "trend_mm_yr": 2.0297572463342055,
            "ci95_mm_yr": [
              1.8113082813430281,
              2.248206211325383
            ],
            "se_mm_yr": 0.11074337098344626,
            "p": 7.988054560758264e-44,
            "rho": 0.7225064165786146,
            "n_eff": 191.38528247657194,
            "r2": 0.6374487872133735
          },
          {
            "window": [
              "1924-11-01",
              "2026-09-01"
            ],
            "n": 1188,
            "method": "Seasonal Kendall (period 12)",
            "trend_mm_yr": 2.0,
            "ci95_mm_yr": [
              1.9142857142857144,
              2.0714285714285716
            ],
            "p": 0.0,
            "z": 31.52675983586975,
            "statistic_s": 36122.0,
            "ci_method": "Seasonal rank CI; independent years",
            "missing_months": 35
          }
        ],
        "oni_fit": {
          "window": [
            "1950-01-01",
            "2026-09-01"
          ],
          "n": 899,
          "method": "Joint trend + two harmonics + index; AR(1) CI",
          "lag_months": 0,
          "trend_mm_yr": 2.0713581795141645,
          "ci95_mm_yr": [
            1.854155775468271,
            2.288560583560058
          ],
          "index_coefficient": 37.83457532891686,
          "index_ci95": [
            31.88838044415786,
            43.780770213675865
          ],
          "r2_with_index": 0.8094483570338118,
          "r2_without_index": 0.6800729876544857,
          "rho": 0.5878479938057751,
          "n_eff": 233.3502041845516,
          "index_coefficient_units": "mm per degree C ONI"
        },
        "peaks": [
          {
            "event": "1997/98",
            "requested_window": [
              "1997-01",
              "1998-12"
            ],
            "window": [
              "1997-01-01",
              "1998-12-01"
            ],
            "n": 24,
            "method": "Maximum detrended/deseasonalized monthly anomaly",
            "peak_mm": 206.6429842071571,
            "peak_month": "1997-11-01",
            "ci95": null,
            "ci_note": "Descriptive selected maximum; no confidence interval"
          },
          {
            "event": "2015/16",
            "requested_window": [
              "2015-01",
              "2016-12"
            ],
            "window": [
              "2015-01-01",
              "2016-12-01"
            ],
            "n": 24,
            "method": "Maximum detrended/deseasonalized monthly anomaly",
            "peak_mm": 164.54366162035444,
            "peak_month": "2015-10-01",
            "ci95": null,
            "ci_note": "Descriptive selected maximum; no confidence interval"
          }
        ]
      },
      "9414290": {
        "name": "San Francisco",
        "window": [
          "1854-07-01",
          "2026-10-01"
        ],
        "n": 2059,
        "missing_months": 9,
        "trends": [
          {
            "window": [
              "1854-07-01",
              "2026-10-01"
            ],
            "n": 2059,
            "method": "Sen (independent-error rank CI)",
            "trend_mm_yr": 1.5322259709745198,
            "ci95_mm_yr": [
              1.4789155211938163,
              1.585406291624039
            ]
          },
          {
            "window": [
              "1854-07-01",
              "2026-10-01"
            ],
            "n": 2059,
            "method": "Naive OLS",
            "trend_mm_yr": 1.5309494897142193,
            "ci95_mm_yr": [
              1.4770663484298847,
              1.5848326309985539
            ],
            "se_mm_yr": 0.027475727365343487,
            "p": 0.0,
            "rho": 0.6911677411517617,
            "n_eff": 2059.0,
            "r2": 0.6014899165169714
          },
          {
            "window": [
              "1854-07-01",
              "2026-10-01"
            ],
            "n": 2059,
            "method": "Plain Mann-Kendall",
            "trend_mm_yr": 1.5322259709745198,
            "ci95_mm_yr": [
              1.4789155211938163,
              1.585406291624039
            ],
            "p": 0.0,
            "z": 40.55050776218563,
            "statistic_s": 1263332.0,
            "ci_method": "Sen rank CI; independent errors (not Hamed-Rao adjusted)",
            "missing_months": 9
          },
          {
            "window": [
              "1854-07-01",
              "2026-10-01"
            ],
            "n": 2059,
            "method": "Hamed-Rao Mann-Kendall",
            "trend_mm_yr": 1.5322259709745198,
            "ci95_mm_yr": [
              1.4789155211938163,
              1.585406291624039
            ],
            "p": 2.6423307986078726e-14,
            "z": 7.614595122934961,
            "statistic_s": 1263332.0,
            "ci_method": "Sen rank CI; independent errors (not Hamed-Rao adjusted)",
            "missing_months": 9
          },
          {
            "window": [
              "1854-07-01",
              "2026-10-01"
            ],
            "n": 2059,
            "method": "AR(1)-OLS effective sample size",
            "trend_mm_yr": 1.5309494897142193,
            "ci95_mm_yr": [
              1.4045233198991813,
              1.6573756595292573
            ],
            "se_mm_yr": 0.06429559390822905,
            "p": 6.202971974522899e-77,
            "rho": 0.6911677411517617,
            "n_eff": 376.00387323817785,
            "r2": 0.6014899165169714
          },
          {
            "window": [
              "1854-07-01",
              "2026-10-01"
            ],
            "n": 2059,
            "method": "Seasonal Kendall (period 12)",
            "trend_mm_yr": 1.5348837209302326,
            "ci95_mm_yr": [
              1.486842105263158,
              1.5866666666666667
            ],
            "p": 0.0,
            "z": 40.80465690051605,
            "statistic_s": 106345.0,
            "ci_method": "Seasonal rank CI; independent years",
            "missing_months": 9
          }
        ],
        "oni_fit": {
          "window": [
            "1950-01-01",
            "2026-09-01"
          ],
          "n": 912,
          "method": "Joint trend + two harmonics + index; AR(1) CI",
          "lag_months": 0,
          "trend_mm_yr": 1.9745229292940865,
          "ci95_mm_yr": [
            1.695032219721917,
            2.254013638866256
          ],
          "index_coefficient": 39.7435171736804,
          "index_ci95": [
            31.97487911066074,
            47.51215523670007
          ],
          "r2_with_index": 0.6088432995845858,
          "r2_without_index": 0.4641556142589891,
          "rho": 0.5348552320826008,
          "n_eff": 276.3856938905352,
          "index_coefficient_units": "mm per degree C ONI"
        },
        "peaks": [
          {
            "event": "1997/98",
            "requested_window": [
              "1997-01",
              "1998-12"
            ],
            "window": [
              "1997-01-01",
              "1998-12-01"
            ],
            "n": 24,
            "method": "Maximum detrended/deseasonalized monthly anomaly",
            "peak_mm": 297.9129268245144,
            "peak_month": "1998-02-01",
            "ci95": null,
            "ci_note": "Descriptive selected maximum; no confidence interval"
          },
          {
            "event": "2015/16",
            "requested_window": [
              "2015-01",
              "2016-12"
            ],
            "window": [
              "2015-01-01",
              "2016-12-01"
            ],
            "n": 24,
            "method": "Maximum detrended/deseasonalized monthly anomaly",
            "peak_mm": 150.23122704228098,
            "peak_month": "2015-10-01",
            "ci95": null,
            "ci_note": "Descriptive selected maximum; no confidence interval"
          }
        ]
      }
    },
    "notes": [
      "Gauge records are relative sea level on datum MSL; no vertical-land-motion or GIA correction.",
      "Nonseasonal trend methods use deseasonalized monthly values; seasonal Kendall uses raw monthly values.",
      "Peaks are observed monthly maxima after full-record climatology and linear detrending; no inferential CI for a selected maximum.",
      "Hamed-Rao p-values compress missing months; gap counts are reported. Sen intervals are independent-error rank intervals."
    ],
    "battery_winters": {
      "window": [
        "1949-10-01",
        "2026-04-01"
      ],
      "n": 77,
      "method": "Complete 7-month Oct-Apr detrended/deseasonalized anomalies; DJF ONI >=0.5 C",
      "el_nino": {
        "n": 25,
        "mean_mm": 12.397257250987453,
        "ci95_mm": [
          -14.202848558288581,
          38.99736306026349
        ]
      },
      "other": {
        "n": 52,
        "mean_mm": -2.6467466289039523,
        "ci95_mm": [
          -13.40594238099246,
          8.112449123184557
        ]
      },
      "difference_mm": 15.044003879891406,
      "ci95_mm": [
        -13.368656728502568,
        43.456664488285384
      ],
      "ci_method": "Welch independent-winter CI",
      "welch_t": 1.0777943929859028,
      "welch_df": 32.55917783665509,
      "welch_p": 0.28904630677772686,
      "permutation_p": 0.1941,
      "permutations": 9999,
      "permutation_method": "Two-sided winter-label permutation, plus-one correction; exchangeable winters",
      "seed": 20261114,
      "winters": [
        {
          "year": 1950,
          "mean_mm": -49.40321161597402,
          "djf_oni_c": -1.32,
          "el_nino": false
        },
        {
          "year": 1951,
          "mean_mm": 38.498332925917,
          "djf_oni_c": -0.66,
          "el_nino": false
        },
        {
          "year": 1952,
          "mean_mm": 19.542734610665157,
          "djf_oni_c": 0.52,
          "el_nino": true
        },
        {
          "year": 1953,
          "mean_mm": 30.015707723984743,
          "djf_oni_c": 0.25,
          "el_nino": false
        },
        {
          "year": 1954,
          "mean_mm": -11.082747734124238,
          "djf_oni_c": 0.41,
          "el_nino": false
        },
        {
          "year": 1955,
          "mean_mm": -10.609774620804655,
          "djf_oni_c": -0.5,
          "el_nino": false
        },
        {
          "year": 1956,
          "mean_mm": 26.00605563537207,
          "djf_oni_c": -1.17,
          "el_nino": false
        },
        {
          "year": 1957,
          "mean_mm": -0.9495426798797675,
          "djf_oni_c": -0.27,
          "el_nino": false
        },
        {
          "year": 1958,
          "mean_mm": 54.38057329058267,
          "djf_oni_c": 1.69,
          "el_nino": true
        },
        {
          "year": 1959,
          "mean_mm": -27.289310738954885,
          "djf_oni_c": 0.6,
          "el_nino": true
        },
        {
          "year": 1960,
          "mean_mm": 31.183662374364697,
          "djf_oni_c": 0.02,
          "el_nino": false
        },
        {
          "year": 1961,
          "mean_mm": 25.228064059112853,
          "djf_oni_c": 0.0,
          "el_nino": false
        },
        {
          "year": 1962,
          "mean_mm": 6.986751458146725,
          "djf_oni_c": -0.16,
          "el_nino": false
        },
        {
          "year": 1963,
          "mean_mm": -10.254561142819398,
          "djf_oni_c": -0.33,
          "el_nino": false
        },
        {
          "year": 1964,
          "mean_mm": -39.924445172356954,
          "djf_oni_c": 0.95,
          "el_nino": true
        },
        {
          "year": 1965,
          "mean_mm": 16.69138508381977,
          "djf_oni_c": -0.51,
          "el_nino": false
        },
        {
          "year": 1966,
          "mean_mm": -18.692784660003497,
          "djf_oni_c": 1.24,
          "el_nino": true
        },
        {
          "year": 1967,
          "mean_mm": 36.4944741676018,
          "djf_oni_c": -0.46,
          "el_nino": false
        },
        {
          "year": 1968,
          "mean_mm": -25.175409861935755,
          "djf_oni_c": -0.62,
          "el_nino": false
        },
        {
          "year": 1969,
          "mean_mm": -30.559579605759033,
          "djf_oni_c": 0.98,
          "el_nino": true
        },
        {
          "year": 1970,
          "mean_mm": 29.91339350756056,
          "djf_oni_c": 0.46,
          "el_nino": false
        },
        {
          "year": 1971,
          "mean_mm": 23.243509478023007,
          "djf_oni_c": -1.29,
          "el_nino": false
        },
        {
          "year": 1972,
          "mean_mm": 23.145054019914017,
          "djf_oni_c": -0.57,
          "el_nino": false
        },
        {
          "year": 1973,
          "mean_mm": 84.76088427609076,
          "djf_oni_c": 1.55,
          "el_nino": true
        },
        {
          "year": 1974,
          "mean_mm": -18.051856896303953,
          "djf_oni_c": -1.87,
          "el_nino": false
        },
        {
          "year": 1975,
          "mean_mm": -32.0074552115558,
          "djf_oni_c": -0.56,
          "el_nino": false
        },
        {
          "year": 1976,
          "mean_mm": 0.1798036160495075,
          "djf_oni_c": -1.49,
          "el_nino": false
        },
        {
          "year": 1977,
          "mean_mm": -140.20436612777377,
          "djf_oni_c": 0.71,
          "el_nino": true
        },
        {
          "year": 1978,
          "mean_mm": 62.840035556974385,
          "djf_oni_c": 0.71,
          "el_nino": true
        },
        {
          "year": 1979,
          "mean_mm": 3.455865813151121,
          "djf_oni_c": 0.19,
          "el_nino": false
        },
        {
          "year": 1980,
          "mean_mm": -41.49973250210072,
          "djf_oni_c": 0.62,
          "el_nino": true
        },
        {
          "year": 1981,
          "mean_mm": -106.883902245924,
          "djf_oni_c": -0.27,
          "el_nino": false
        },
        {
          "year": 1982,
          "mean_mm": -65.98235770403298,
          "djf_oni_c": -0.05,
          "el_nino": false
        },
        {
          "year": 1983,
          "mean_mm": 48.06204398071517,
          "djf_oni_c": 2.14,
          "el_nino": true
        },
        {
          "year": 1984,
          "mean_mm": 55.963588522606194,
          "djf_oni_c": -0.63,
          "el_nino": false
        },
        {
          "year": 1985,
          "mean_mm": -40.56343836407422,
          "djf_oni_c": -1.01,
          "el_nino": false
        },
        {
          "year": 1986,
          "mean_mm": 1.76667760638822,
          "djf_oni_c": -0.4,
          "el_nino": false
        },
        {
          "year": 1987,
          "mean_mm": 24.525365005422096,
          "djf_oni_c": 1.18,
          "el_nino": true
        },
        {
          "year": 1988,
          "mean_mm": -26.001661881258322,
          "djf_oni_c": 0.63,
          "el_nino": true
        },
        {
          "year": 1989,
          "mean_mm": -69.67154591079587,
          "djf_oni_c": -1.64,
          "el_nino": false
        },
        {
          "year": 1990,
          "mean_mm": -84.91285851176201,
          "djf_oni_c": 0.18,
          "el_nino": false
        },
        {
          "year": 1991,
          "mean_mm": -14.868456827013846,
          "djf_oni_c": 0.35,
          "el_nino": false
        },
        {
          "year": 1992,
          "mean_mm": -0.5383408565514084,
          "djf_oni_c": 1.54,
          "el_nino": true
        },
        {
          "year": 1993,
          "mean_mm": 23.648917971053898,
          "djf_oni_c": 0.13,
          "el_nino": false
        },
        {
          "year": 1994,
          "mean_mm": -39.592394629912235,
          "djf_oni_c": 0.07,
          "el_nino": false
        },
        {
          "year": 1995,
          "mean_mm": -51.40513580230694,
          "djf_oni_c": 0.88,
          "el_nino": true
        },
        {
          "year": 1996,
          "mean_mm": 17.78212302529837,
          "djf_oni_c": -0.88,
          "el_nino": false
        },
        {
          "year": 1997,
          "mean_mm": 77.54081042433225,
          "djf_oni_c": -0.41,
          "el_nino": false
        },
        {
          "year": 1998,
          "mean_mm": 83.01378353765183,
          "djf_oni_c": 2.22,
          "el_nino": true
        },
        {
          "year": 1999,
          "mean_mm": -13.08467192045716,
          "djf_oni_c": -1.51,
          "el_nino": false
        },
        {
          "year": 2000,
          "mean_mm": -45.18312737856615,
          "djf_oni_c": -1.47,
          "el_nino": false
        },
        {
          "year": 2001,
          "mean_mm": 20.718417163324876,
          "djf_oni_c": -0.76,
          "el_nino": false
        },
        {
          "year": 2002,
          "mean_mm": -63.95146686621269,
          "djf_oni_c": -0.15,
          "el_nino": false
        },
        {
          "year": 2003,
          "mean_mm": -32.62135089575025,
          "djf_oni_c": 0.9,
          "el_nino": true
        },
        {
          "year": 2004,
          "mean_mm": -47.86266349671637,
          "djf_oni_c": 0.34,
          "el_nino": false
        },
        {
          "year": 2005,
          "mean_mm": 54.61030961660321,
          "djf_oni_c": 0.62,
          "el_nino": true
        },
        {
          "year": 2006,
          "mean_mm": -8.059574412934344,
          "djf_oni_c": -0.86,
          "el_nino": false
        },
        {
          "year": 2007,
          "mean_mm": -54.158029871043325,
          "djf_oni_c": 0.62,
          "el_nino": true
        },
        {
          "year": 2008,
          "mean_mm": 1.8863718137048247,
          "djf_oni_c": -1.76,
          "el_nino": false
        },
        {
          "year": 2009,
          "mean_mm": -29.212083644404153,
          "djf_oni_c": -0.89,
          "el_nino": false
        },
        {
          "year": 2010,
          "mean_mm": 105.68946089748685,
          "djf_oni_c": 1.47,
          "el_nino": true
        },
        {
          "year": 2011,
          "mean_mm": 35.44814829652072,
          "djf_oni_c": -1.29,
          "el_nino": false
        },
        {
          "year": 2012,
          "mean_mm": 18.349692838411748,
          "djf_oni_c": -0.71,
          "el_nino": false
        },
        {
          "year": 2013,
          "mean_mm": 34.53695166601704,
          "djf_oni_c": -0.24,
          "el_nino": false
        },
        {
          "year": 2014,
          "mean_mm": -28.132932363520517,
          "djf_oni_c": -0.24,
          "el_nino": false
        },
        {
          "year": 2015,
          "mean_mm": -34.08853067877235,
          "djf_oni_c": 0.73,
          "el_nino": true
        },
        {
          "year": 2016,
          "mean_mm": 23.241585291690082,
          "djf_oni_c": 2.5,
          "el_nino": true
        },
        {
          "year": 2017,
          "mean_mm": -26.71401302356175,
          "djf_oni_c": -0.08,
          "el_nino": false
        },
        {
          "year": 2018,
          "mean_mm": -3.526754195956459,
          "djf_oni_c": -0.71,
          "el_nino": false
        },
        {
          "year": 2019,
          "mean_mm": 10.803361774505987,
          "djf_oni_c": 0.99,
          "el_nino": true
        },
        {
          "year": 2020,
          "mean_mm": 77.56204917353986,
          "djf_oni_c": 0.71,
          "el_nino": true
        },
        {
          "year": 2021,
          "mean_mm": 32.17787942971659,
          "djf_oni_c": -0.99,
          "el_nino": false
        },
        {
          "year": 2022,
          "mean_mm": 26.22228111446475,
          "djf_oni_c": -0.76,
          "el_nino": false
        },
        {
          "year": 2023,
          "mean_mm": 77.26668279921292,
          "djf_oni_c": -0.55,
          "el_nino": false
        },
        {
          "year": 2024,
          "mean_mm": 157.88251305538967,
          "djf_oni_c": 1.84,
          "el_nino": true
        },
        {
          "year": 2025,
          "mean_mm": -13.073085259862207,
          "djf_oni_c": -0.46,
          "el_nino": false
        },
        {
          "year": 2026,
          "mean_mm": 6.828459282028803,
          "djf_oni_c": -0.39,
          "el_nino": false
        }
      ]
    }
  }
}
```
