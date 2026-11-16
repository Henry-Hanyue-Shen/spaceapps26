# Sea Level Detective — pipeline spec (for Codex)

Goal: a small, readable Python pipeline (Python 3.13, venv at `../.venv`, run with `..\.venv\Scripts\python.exe`)
that produces the numbers for experiments E0–E4 of `../experiment_plan/experiment_plan_sealevel_detective.tex`.
It must run in two modes: **with** a NASA Earthdata token (env var `EARTHDATA_TOKEN`) and **without** it
(`--no-nasa`), in which case it runs everything that needs no NASA login.

Installed packages: numpy, pandas, scipy, xarray, netCDF4, h5netcdf, earthaccess, pymannkendall, statsmodels,
matplotlib, requests. Do not install anything else.

## Layout (all inside `pipeline/`)
- `config.py` — paths (`data_raw/`, `data_processed/`, `results/`, `figures/`), box definitions, constants.
- `fetch_nasa.py` — `earthaccess.login(strategy="environment")`; download
  `NASA_SSH_GMSL_INDICATOR`, `NASA_SSH_ENSO_INDICATOR`, `NASA_SSH_PDO_INDICATOR` (ASCII .txt) and every granule
  of `NASA_SSH_REF_SIMPLE_GRID_V1` (netCDF-4, about 1 MB each, about 1,700 files) into `data_raw/nasa/`, skipping files
  already present. Threads ≤ 8. Exit with a clear message if no token is set.
- `build_series.py` — read each grid file once (variable `ssha` in **metres**; coords `latitude`, `longitude`;
  inspect one file first and adapt names/flags), compute cos(lat)-weighted box means → `data_processed/box_weekly.csv`,
  then monthly means → `box_monthly.csv`; also a 1° monthly grid `grid_1deg_monthly.nc` (coarsened). Parse the three
  indicator .txt files (inspect the header; GMSL is in **cm**) → `indicators.csv` (monthly).
- `fetch_noaa.py` (no login) — NOAA CO-OPS monthly mean water level, metric, datum MSL, for the Battery 8518750,
  La Jolla 9410230 and San Francisco 9414290, full record (API `https://api.tidesandcurrents.noaa.gov/api/prod/datagetter`,
  product `monthly_mean`, max 10-year windows per request — loop). NOAA ONI from
  `https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt`. Save to `data_raw/noaa/` and tidy CSVs in `data_processed/`.
- `stats.py` — functions, each with a docstring and units:
  - `deseasonalize(series)` (monthly climatology removed);
  - `sen_slope(series)` with a 95% CI (per year);
  - `mk_hamed_rao(series)` (pymannkendall `hamed_rao_modification_test`);
  - `seasonal_kendall(series)` (pymannkendall `seasonal_test`, period 12);
  - `ols_ar1(series)`: OLS trend with an AR(1)-adjusted SE (effective sample size);
  - `fit_with_index(series, index, lag)`: **joint** fit of trend + annual and semiannual harmonics + index at a fixed lag.
    Return the trend, its AR(1)-adjusted CI, the index coefficient, R² with and without the index, and the
    index-removed series (subtract **only** the fitted index component).
  All trends in mm/yr.
- `e1_synthetic.py` — Monte Carlo, ≥ 1,000 series per setting. Monthly AR(1) noise with **marginal** SD σ and φ
  (use σ, φ estimated from the deseasonalized gauge residuals; fall back to σ = 30 mm, φ = 0.6). Lengths 10, 15, 20,
  25, 30, 35 years; trends 0, 1, 2, 3, 4 mm/yr. Tests: naive OLS, plain MK, Hamed–Rao MK, seasonal Kendall, AR(1)-OLS.
  Report the false-positive rate at trend 0, with a binomial 95% CI, and power curves. Compare the AR(1)-OLS 90%-power
  crossing with Weatherhead et al. 1998, n* = [(3.3 σ/|ω|) √((1+φ)/(1−φ))]^(2/3), **only** for the plain AR(1) case.
  Save `results/e1.json` and `figures/e1_*.png`. Seeded; must finish in < 10 min on a laptop.
- `e0_global.py` — needs NASA. Our area-weighted global series vs `NASA_SSH_GMSL_INDICATOR` (match units and times;
  report bias, RMSE, trend difference). Quadratic fit 1993-01..2017-12 and 1993..latest (rate and acceleration with CIs).
  No GIA correction: state it in the JSON. Nerem 2018 is context only.
- `e2_seesaw.py` — needs NASA. Per-1°-cell regression of the deseasonalized SSHA on the ENSO index (lag fixed in config,
  default 0; also report lags 0–6 as a sensitivity table) → map PNG. W/E Pacific box series with El Niño periods shaded.
  Run with both the NASA ENSO indicator and NOAA ONI.
- `e3_windows.py` — needs NASA. For each box: Sen slope of every 10-year window (descriptive, overlapping) raw vs
  index-removed; full-record trend. No pass/fail gate.
- `e4_coasts.py` — gauge part runs **without** NASA: per gauge, trend (all methods), ONI regression amplitude
  (mm per °C) and the 1997/98 and 2015/16 peak anomalies; Battery cool-season (Oct–Apr) mean anomaly in El Niño
  winters (ONI ≥ 0.5 for DJF) vs others, with a Welch t-test and a permutation test. With NASA: also the box vs gauge
  correlation and trend difference.
- `run_all.py` — `--no-nasa` runs fetch_noaa, e1, e4 (gauge part); otherwise everything. Writes `results/summary.md`
  with every number, its window, n, method and CI.
- `tests/test_stats.py` — recover a known trend from synthetic data; FPR sanity check. Runnable with plain
  `python -m unittest`.

## Boxes (fixed before results; put in config.py)
Global 66°S–66°N; W. Pacific 5°S–5°N, 120°E–160°E; E. Pacific 5°S–5°N, 150°W–90°W; California shelf
32°N–38°N, 124°W–117°W; NY Bight 39.5°N–41°N, 74.5°W–71.5°W. Handle the longitude convention (0–360 vs ±180).

## Rules
- Never hard-code results; never tune to match literature.
- No credentials in code or files; read the token only from the environment.
- Keep each script short and commented; print progress.
- `.gitignore`: data_raw/, data_processed/*.nc.
