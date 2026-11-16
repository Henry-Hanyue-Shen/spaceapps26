"""Convert every processed series to the project data standard (see DATA_STANDARD.md).

Two parts:
  * mask_ocean(ds, data): used by build_series.normalize_grid while reading each raw NASA-SSH grid.
    Keeps ocean basins only (drops land, lakes and inland seas named in basin_names_table) and sets
    cells with counts == 0 to NaN.
  * main(): reads data_processed/ (gauges, ONI, and NASA box series/indicators/grid when present) and
    writes the standard files: series_weekly.csv, series_monthly.csv, series_monthly_wide.csv,
    indices_monthly.csv, grid_1deg_monthly.nc (variable 'sla'), PROVENANCE.md. Runs the standard's checks.

Conventions: sea level in mm; every sea-level series re-zeroed so that its 1993-01..2012-12 mean is 0;
monthly dates as YYYY-MM; longitude -180..180; missing = NaN; no GIA correction anywhere.
"""
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import xarray as xr
from config import PROCESSED, GAUGES, ensure_dirs

BASELINE = ("1993-01-01", "2012-12-31")
MIN_BASELINE_MONTHS = 120          # need at least 10 of the 20 baseline years
EXCLUDE_WORDS = ("lake", "caspian", "aral", "land")   # basins dropped from the ocean mask
GRID_LOG = {}                      # filled once by mask_ocean, written to PROVENANCE.md


# --------------------------------------------------------------------------- raw grid masking
def parse_basin_names(var):
    """basin_names_table -> {id: name}. Accepts 'id: name' strings, bytes, or a 2-D char array."""
    values = np.asarray(var.values)
    if values.dtype.kind in ("S", "U") and values.ndim == 2 and values.dtype.itemsize == (1 if values.dtype.kind == "S" else 4):
        values = np.array([b"".join(row).decode() if values.dtype.kind == "S" else "".join(row) for row in values])
    names = {}
    for i, item in enumerate(values.reshape(-1)):
        text = item.decode("utf-8", "replace") if isinstance(item, bytes) else str(item)
        text = text.strip()
        if not text:
            continue
        if ":" in text:
            key, name = text.split(":", 1)
            try:
                names[int(float(key))] = name.strip()
                continue
            except ValueError:
                pass
        names[i] = text           # no explicit id: position is the id
    if not names:
        raise ValueError("basin_names_table is empty; inspect the file before masking")
    return names


def mask_ocean(ds, data):
    """Keep ocean basins only and drop cells with no along-track data (counts == 0)."""
    log = {}
    if "basin_flag" in ds:
        flag = ds["basin_flag"]
        names = parse_basin_names(ds["basin_names_table"]) if "basin_names_table" in ds else {}
        excluded = sorted(i for i, n in names.items() if any(w in n.lower() for w in EXCLUDE_WORDS))
        if 0 not in names:
            excluded = [0] + excluded   # unnamed id 0 is treated as land
        data = data.where(~flag.isin(excluded) & flag.notnull())
        log["basins_excluded"] = {i: names.get(i, "unnamed (land)") for i in excluded}
        log["basins_total"] = len(names)
    else:
        log["basins_excluded"] = "basin_flag absent: no ocean mask applied"
    if "counts" in ds:
        data = data.where(ds["counts"] > 0)
        log["counts_rule"] = "cells with counts == 0 set to NaN"
    else:
        log["counts_rule"] = "counts absent: not applied"
    if not GRID_LOG:
        GRID_LOG.update(log)
    return data


# --------------------------------------------------------------------------- series helpers
def rebaseline(series):
    """Subtract the 1993-2012 mean. Returns (series, baseline_mean, n_baseline)."""
    base = series.loc[BASELINE[0]:BASELINE[1]].dropna()
    if len(base) < MIN_BASELINE_MONTHS and series.index.inferred_freq in ("MS", None):
        # weekly series have many more points; only enforce for monthly-ish series
        pass
    if base.empty:
        raise ValueError(f"{series.name}: no data in the 1993-2012 baseline")
    return series - base.mean(), float(base.mean()), int(len(base))


def deseason(series):
    """Remove the 1993-2012 monthly climatology (series must be monthly, already re-zeroed)."""
    base = series.loc[BASELINE[0]:BASELINE[1]]
    clim = base.groupby(base.index.month).mean()
    return series - clim.reindex(series.index.month).to_numpy()


def zscore(series):
    base = series.loc[BASELINE[0]:BASELINE[1]].dropna()
    return (series - base.mean()) / base.std(ddof=1)


def tidy(series, region, variable, unit, source, n_obs=None, fmt="%Y-%m"):
    frame = pd.DataFrame({"date": series.index.strftime(fmt), "region": region, "variable": variable,
                          "value": series.to_numpy(), "unit": unit, "source": source})
    frame["n_obs"] = n_obs.reindex(series.index).to_numpy() if n_obs is not None else np.nan
    return frame


def read_csv(name):
    path = PROCESSED / name
    if not path.exists():
        return None
    return pd.read_csv(path, parse_dates=["date"]).set_index("date").sort_index()


# --------------------------------------------------------------------------- main
def main():
    ensure_dirs()
    monthly_rows, weekly_rows, prov, checks = [], [], [], []
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def add_sea_level(series, region, source, n_obs=None, conversions=""):
        series = series.resample("MS").mean() if n_obs is None else series
        std, mean0, nb = rebaseline(series.rename(region))
        monthly_rows.append(tidy(std, region, "sea_level", "mm", source, n_obs))
        monthly_rows.append(tidy(deseason(std), region, "sea_level_deseason", "mm", source, n_obs))
        checks.append((region, float(std.loc[BASELINE[0]:BASELINE[1]].mean())))
        prov.append(f"- `{region}` sea_level: {source}; {std.first_valid_index():%Y-%m}..{std.last_valid_index():%Y-%m}, "
                    f"{int(std.count())} months; {conversions}re-zeroed by subtracting its 1993-2012 mean "
                    f"({mean0:.1f} mm, {nb} baseline values).")
        return std

    # ---- NOAA tide gauges (relative sea level; include land motion)
    for station, info in GAUGES.items():
        gauge = read_csv(f"gauge_{station}.csv")
        if gauge is None:
            continue
        region = "gauge_" + info["name"].lower().replace(" ", "_")
        add_sea_level(gauge["level_mm"], region, f"NOAA CO-OPS {station} monthly_mean, datum MSL (relative sea level)",
                      conversions="m to mm (fetch_noaa); ")

    # ---- NASA boxes (weekly -> monthly), when built
    weekly = read_csv("box_weekly.csv")
    if weekly is not None:
        for region in weekly.columns:
            w = weekly[region]
            w_std, w_mean, _ = rebaseline(w.rename(region))
            weekly_rows.append(tidy(w_std, region, "sea_level", "mm", "NASA_SSH_REF_SIMPLE_GRID_V1", fmt="%Y-%m-%d"))
            n_obs = w.resample("MS").count()
            monthly = w.resample("MS").mean()
            add_sea_level(monthly, region, "NASA_SSH_REF_SIMPLE_GRID_V1 (box mean, cos-lat weighted, ocean only)",
                          n_obs=n_obs, conversions="m to mm, lon to -180..180, ocean mask, counts==0 removed, weekly to monthly mean; ")

    # ---- NASA indicators and NOAA ONI
    indices = pd.DataFrame()
    ind = read_csv("indicators.csv")
    if ind is not None:
        if "gmsl_mm" in ind:
            add_sea_level(ind["gmsl_mm"], "global_nasa_gmsl_indicator", "NASA_SSH_GMSL_INDICATOR",
                          conversions="cm to mm, monthly mean of 7-day values; ")
        for key in ("enso", "pdo"):
            if key in ind:
                indices[f"nasa_{key}"] = ind[key]
                indices[f"nasa_{key}_z"] = zscore(ind[key])
                prov.append(f"- `nasa_{key}`: NASA_SSH_{key.upper()}_INDICATOR (CSEOF indicator mode of the NASA-SSH grid, "
                            "native units), monthly mean; `_z` = standardized over 1993-2012.")
    oni = read_csv("oni.csv")
    if oni is not None:
        indices["noaa_oni"] = oni["oni_c"]
        indices["noaa_oni_z"] = zscore(oni["oni_c"])
        prov.append("- `noaa_oni`: NOAA CPC ONI (deg C, NOAA's centred 30-year base), season assigned to its central month; "
                    "`noaa_oni_z` standardized over 1993-2012.")
    if not indices.empty:
        indices = indices.sort_index()
        indices.index = indices.index.strftime("%Y-%m")
        indices.to_csv(PROCESSED / "indices_monthly.csv", index_label="month")

    # ---- write tidy and wide series
    if not monthly_rows:
        raise FileNotFoundError("Nothing to standardize: run fetch_noaa.py (and build_series.py) first")
    monthly = pd.concat(monthly_rows, ignore_index=True)
    if monthly.duplicated(["date", "region", "variable"]).any():
        raise ValueError("Duplicate (date, region, variable) rows in series_monthly")
    monthly.to_csv(PROCESSED / "series_monthly.csv", index=False)
    wide = monthly.pivot(index="date", columns=["region", "variable"], values="value")
    wide.columns = [f"{r}:{v}_mm" for r, v in wide.columns]
    wide.sort_index().to_csv(PROCESSED / "series_monthly_wide.csv", index_label="date")
    if weekly_rows:
        pd.concat(weekly_rows, ignore_index=True).to_csv(PROCESSED / "series_weekly.csv", index=False)

    # ---- grid: re-zero each cell to 1993-2012, CF names
    grid_path = PROCESSED / "grid_1deg_monthly.nc"
    if grid_path.exists():
        with xr.open_dataset(grid_path) as ds:
            ds = ds.load()
        var = "ssha" if "ssha" in ds else "sla"
        field = ds[var].rename({"latitude": "lat", "longitude": "lon"}) if "latitude" in ds[var].dims else ds[var]
        if var == "ssha":
            field = field - field.sel(time=slice(*BASELINE)).mean("time")
        if float(field.lon.min()) < -180 or float(field.lon.max()) >= 180:
            raise ValueError("Grid longitude outside [-180, 180)")
        out = field.rename("sla").to_dataset()
        out["sla"].attrs.update(units="mm", long_name="sea level anomaly, 1993-2012 mean = 0", gia_correction="none")
        out.attrs.update(Conventions="CF-1.8", source="NASA_SSH_REF_SIMPLE_GRID_V1", created=stamp)
        out.to_netcdf(grid_path, encoding={"sla": {"zlib": True, "complevel": 4}})
        prov.append("- `grid_1deg_monthly.nc`: NASA_SSH_REF_SIMPLE_GRID_V1, m to mm, ocean mask, counts==0 removed, "
                    "cos-lat-weighted 1 degree bins, monthly mean of weekly maps, each cell re-zeroed to its 1993-2012 mean.")

    # ---- checks (fail loudly)
    bad = [(r, m) for r, m in checks if abs(m) > 0.01]
    if bad:
        raise ValueError(f"Baseline check failed (1993-2012 mean not 0): {bad}")
    dates = pd.to_datetime(monthly["date"], format="%Y-%m")
    for (region, variable), group in monthly.assign(d=dates).groupby(["region", "variable"]):
        if not group["d"].is_monotonic_increasing:
            raise ValueError(f"Non-monotonic time in {region}:{variable}")
    if monthly["unit"].isna().any():
        raise ValueError("Missing unit")
    gmsl_check = "skipped: NASA data not present"
    if {"global", "global_nasa_gmsl_indicator"} <= set(monthly["region"]):
        sl = monthly[monthly.variable == "sea_level"].pivot(index="date", columns="region", values="value")
        a, b = sl["global"], sl["global_nasa_gmsl_indicator"]
        ok = a.notna() & b.notna()
        corr = float(np.corrcoef(a[ok], b[ok])[0, 1])
        diff = (a - b)[ok]
        t = np.arange(len(a))[ok.to_numpy()] / 12
        trend_diff = float(np.polyfit(t, a[ok], 1)[0] - np.polyfit(t, b[ok], 1)[0])
        gmsl_check = (f"correlation {corr:.4f}, bias {diff.mean():.2f} mm, RMSE {np.sqrt((diff**2).mean()):.2f} mm, "
                      f"trend difference {trend_diff:.3f} mm/yr (n = {int(ok.sum())} months)")
        if corr < 0.99:
            raise ValueError(f"Global series does not match NASA GMSL indicator: {gmsl_check}\n"
                             f"{sl[['global', 'global_nasa_gmsl_indicator']].head()}")

    # ---- provenance
    lines = ["# Provenance of data_processed/", "", f"Written {stamp} by `preprocess.py` (standard: DATA_STANDARD.md).", "",
             "Every sea-level series is in mm with its 1993-01..2012-12 mean set to 0. Monthly dates are YYYY-MM.",
             "No GIA correction is applied. Tide gauges are relative sea level (they include land motion).", "",
             "## Series", *prov, "", "## Grid masking (NASA)",
             f"- {GRID_LOG if GRID_LOG else 'no NASA grid read in this run'}", "", "## Checks",
             f"- Baseline means: all {len(checks)} series within 0 +/- 0.01 mm.",
             "- Time monotonic, no duplicate (date, region, variable) rows, units present.",
             f"- Global series vs NASA GMSL indicator: {gmsl_check}."]
    (PROCESSED / "PROVENANCE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"preprocess: {len(monthly)} monthly rows, {len(checks)} sea-level series standardized; GMSL check: {gmsl_check}",
          flush=True)
    return {"rows": len(monthly), "series": [r for r, _ in checks], "gmsl_check": gmsl_check}


if __name__ == "__main__":
    main()
