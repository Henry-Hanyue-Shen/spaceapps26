# Data standard: every processed file in `data_processed/` follows this

Raw NASA (and NOAA) files use their own conventions. `preprocess.py` converts them to one "usual" format, so
that every series can be plotted on the same axes, with the same units and the same zero line. Raw files are never
edited; every conversion is recorded in `data_processed/PROVENANCE.md`.

Sources for the raw conventions: NASA-SSH V1 User Guide, Table 2, and the NASA-SSH Indicators User Guide (both in
`../docs_nasa/`); NOAA CO-OPS API documentation.

## Conventions

| Item | Standard | Raw convention it replaces |
|---|---|---|
| Sea level unit | **mm** | NASA-SSH `ssha` in **m**; GMSL indicator in **cm**; CO-OPS metric in **m** |
| Sea level zero line | **mean over 1993-01..2012-12 = 0** for every series (each series re-zeroed by its own mean over that period) | NASA-SSH: anomaly relative to the DTU21 mean sea surface (1993–2012 altimetry); CO-OPS: datum MSL, epoch 1983–2001 |
| Time | ISO 8601 UTC. Weekly series: the map's date (`YYYY-MM-DD`). Monthly series: the month (`YYYY-MM`), value = mean of all weekly maps whose date falls in that month | NASA-SSH `time` = seconds since 1990-01-01 00:00:00 UTC |
| Longitude | **−180 to 180**, ascending | NASA-SSH 0.25 to 359.75 |
| Latitude | −90 to 90, ascending | (same) |
| Missing | `NaN` (CSV: empty) | `_FillValue`, `counts == 0`, CO-OPS gaps |
| Ocean mask | keep ocean basins only; drop land and the lakes and inland seas listed in `basin_names_table` (e.g. Caspian Sea) | grid includes lakes |
| Global mean | cos(latitude)-weighted ocean mean over 66°S–66°N (same as NASA's GMSL indicator) | — |
| Seasonal cycle | kept in the standard series; a `_deseason` copy has the 1993–2012 monthly climatology removed | — |
| ENSO / PDO indices | NASA indicators: original values **and** a z-score (mean 0, SD 1 over 1993–2012). NOAA ONI: kept in °C (NOAA's centred 30-year base), plus a z-score | NASA indicators: CSEOF mode amplitude (unit as in the file header) |
| GIA | **not** applied to any satellite series; recorded in metadata | — |
| Tide gauges | kept as relative sea level (they include land motion); re-zeroed to 1993–2012 | — |

## Files produced

- `series_weekly.csv`: tidy long format, columns `date, region, variable, value, unit, source`.
- `series_monthly.csv`: same columns at monthly resolution, plus `n_obs` (weekly maps averaged).
- `series_monthly_wide.csv`: one column per `region:variable`, for quick plotting.
- `grid_1deg_monthly.nc`: CF-1.8 netCDF with `time` (datetime64), `lat`, `lon` (−180..180), variable `sla` in mm
  (1993–2012 baseline), attribute `gia_correction = "none"`.
- `indices_monthly.csv`: `month, nasa_enso, nasa_enso_z, nasa_pdo, nasa_pdo_z, noaa_oni, noaa_oni_z`.
- `PROVENANCE.md`: for every output, its source files (dataset short name, granule count, first and last dates,
  download date) and every conversion applied.

## Checks run by `preprocess.py` (fail loudly)

1. After conversion, each satellite series has a 1993–2012 mean of 0 ± 0.01 mm.
2. Our global mean vs the NASA GMSL indicator (both converted): report bias, RMSE and trend difference. Correlation
   should be > 0.99; otherwise stop and print both heads.
3. No longitude outside [−180, 180); no duplicate dates; monotonic time.
4. Units are present in every column header or `unit` field.
