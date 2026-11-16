# Sea Level Detective pipeline

Implementation of `SPEC.md`. Run from this folder using the provided Python 3.13 venv:

```powershell
..\.venv\Scripts\python.exe -m unittest -v
..\.venv\Scripts\python.exe run_all.py --no-nasa
```

The second command downloads NOAA data, runs E1 and the gauge portion of E4,
and writes `results/summary.md`, `results/e1.json`, `results/e4.json`, tidy CSVs,
and E1 figures. It stops with exit code 2 if a NOAA request fails. It never
imports or runs the NASA downloader. Raw historical NOAA request windows are
cached; the current partial decade and ONI are refreshed.

For a future full NASA run, set `EARTHDATA_TOKEN` in the process environment
and omit `--no-nasa`. No token is included in source, manifests, or output.
NASA authentication and data access have to be validated with real local data;
offline fixtures do not establish compatibility with an unseen product version.

The implementation uses the specified installed packages only. Every output
path is rooted in this directory. The Matplotlib cache is local too. There is
no automatic package installation or system configuration change.

## Numerical conventions

- Sea level is converted to millimetres during ingestion: NASA grid metres
  times 1000, GMSL centimetres times 10, NOAA monthly MSL metres times 1000.
  NASA ENSO/PDO retain their native indicator units; ONI is degrees C.
- Trend time is calendar months divided by 12, including gaps. Positive index
  lag means the index leads sea level. Regression fits the trend, annual and
  semiannual harmonics and lagged index together. Removing the index subtracts
  only its fitted component. R-squared comparisons use the same observations.
- AR(1) confidence intervals inflate ordinary OLS standard errors by
  `sqrt(n/n_eff)`, with `n_eff = n*(1-rho)/(1+rho)`, residual-based lag-one rho,
  and effective residual degrees of freedom. Negative rho is treated as zero;
  effective n is bounded between the parameter count plus one and observed n.
  This is an approximation, not GLS. Only adjacent months estimate rho.
- Sen intervals are independent-error rank intervals. Hamed-Rao adjusts its
  test statistic, not the separately reported Sen interval. The library skips
  missing observations for its rank autocorrelation calculation, so its
  significance on gappy records is approximate. Seasonal Kendall preserves
  calendar positions and uses within-month pairs for the slope and rank CI.
- E1 simulates a stationary monthly Gaussian AR(1) process with the specified
  marginal SD, using the median gauge residual SD and phi, or the specified
  fallback. Each of the 30 length/trend settings has 1000 series. It batches
  exact rank calculations and shares noise across trend settings. Unit tests
  compare this implementation against pymannkendall and check calibration.
  The under-ten-minute runtime is measured and reported, not assumed.
- Weatherhead's stated formula convention uses annual observations. Both its
  literal value and the monthly-sampling conversion (divide by `12^(1/3)`)
  are reported. Only the plain stationary AR(1) simulation is compared.
  A crossing outside the tested 10–35-year range is reported as censored.
- Gauge trends use deseasonalized series except seasonal Kendall, which uses
  raw monthly data. Peak anomalies remove the full-record monthly climatology
  and linear trend. Peak windows are the complete 1997–1998 and 2015–2016
  calendar years. These maxima are descriptive and have no inferential CI.
- Battery winters contain all seven months October–April and are identified
  by January's year. DJF ONI is assigned to January. Winters with DJF ONI >=0.5 C
  are compared with all other ONI-covered complete winters. Welch inference
  treats winters as independent; permutation inference assumes exchangeable
  winter labels. Both assumptions are stated in the results.
- NASA grid ingestion reads each file once, handles longitude wrapping and
  CF missing/quality values, and records the first file's schema. One-degree
  cells use cosine latitude weights; monthly values average the weekly grids.
  Indicator parsers record headers and reject ambiguous value columns.
- E0 uses matched months and units. Its quadratic fit includes annual and
  semiannual nuisance terms and reports start, midpoint and end rates plus
  acceleration. No GIA correction is applied. Literature is context only.
- E2 uses per-cell deseasonalized SSHA/index regressions with pointwise AR(1)
  intervals. It does not imply spatial multiple-testing significance. E3 uses
  every monthly-start ten-year window and identical raw/removed month pairs;
  overlapping estimates are descriptive, and no pass/fail gate is imposed.

## Data/API references

- [NOAA CO-OPS retrieval API](https://api.tidesandcurrents.noaa.gov/api/prod/)
  and [monthly response fields](https://api.tidesandcurrents.noaa.gov/api/prod/responseHelp.html).
  Requests intentionally use <=10-year windows as specified, even though the
  current API documents a larger limit for monthly means. Querying from 1800
  avoids truncating any of these three stations' records.
- [NOAA ONI ASCII](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt).
- [NASA reference grid](https://podaac.jpl.nasa.gov/dataset/NASA_SSH_REF_SIMPLE_GRID_V1),
  [GMSL indicator](https://podaac.jpl.nasa.gov/dataset/NASA_SSH_GMSL_INDICATOR),
  and [ENSO indicator](https://podaac.jpl.nasa.gov/dataset/NASA_SSH_ENSO_INDICATOR).
- [pyMannKendall](https://github.com/mmhs013/pyMannKendall), used directly for
  observed records and as the reference for the batched simulation tests.

`results/summary.md` includes compact tables and a complete JSON appendix to
preserve all scalar results, windows, sample sizes, methods and interval
definitions. Per-cell arrays are retained in the E2 NetCDF files.
