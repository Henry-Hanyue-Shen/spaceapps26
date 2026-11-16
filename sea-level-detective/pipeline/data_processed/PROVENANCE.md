# Provenance of data_processed/

Written 2026-11-14 19:27 UTC by `preprocess.py` (standard: DATA_STANDARD.md).

Every sea-level series is in mm with its 1993-01..2012-12 mean set to 0. Monthly dates are YYYY-MM.
No GIA correction is applied. Tide gauges are relative sea level (they include land motion).

## Series
- `gauge_the_battery` sea_level: NOAA CO-OPS 8518750 monthly_mean, datum MSL (relative sea level); 1856-01..2026-10, 1865 months; m to mm (fetch_noaa); re-zeroed by subtracting its 1993-2012 mean (43.5 mm, 240 baseline values).
- `gauge_la_jolla` sea_level: NOAA CO-OPS 9410230 monthly_mean, datum MSL (relative sea level); 1924-11..2026-09, 1188 months; m to mm (fetch_noaa); re-zeroed by subtracting its 1993-2012 mean (2.6 mm, 239 baseline values).
- `gauge_san_francisco` sea_level: NOAA CO-OPS 9414290 monthly_mean, datum MSL (relative sea level); 1854-07..2026-10, 2059 months; m to mm (fetch_noaa); re-zeroed by subtracting its 1993-2012 mean (2.1 mm, 238 baseline values).
- `noaa_oni`: NOAA CPC ONI (deg C, NOAA's centred 30-year base), season assigned to its central month; `noaa_oni_z` standardized over 1993-2012.

## Grid masking (NASA)
- {'basins_excluded': 'basin_flag absent: no ocean mask applied', 'counts_rule': 'counts absent: not applied'}

## Checks
- Baseline means: all 3 series within 0 +/- 0.01 mm.
- Time monotonic, no duplicate (date, region, variable) rows, units present.
- Global series vs NASA GMSL indicator: skipped: NASA data not present.
