"""Read NASA grids once, aggregate boxes and monthly 1-degree cells, parse ASCII."""
import re
import numpy as np
import pandas as pd
import xarray as xr
from config import RAW, PROCESSED, BOXES, NASA_COLLECTIONS, ensure_dirs
from common import save_json, metadata
from preprocess import mask_ocean, GRID_LOG


def normalize_grid(ds):
    """Decode SSHA in metres, coordinate aliases, CF fill values and documented flags."""
    rename = {}
    for canonical, aliases in {"latitude": ("latitude", "lat"),
                               "longitude": ("longitude", "lon"),
                               "ssha": ("ssha", "sla", "sea_surface_height_anomaly")}.items():
        found = next((key for key in aliases if key in ds), None)
        if found is None:
            raise ValueError(f"Missing {canonical}; variables: {list(ds.variables)}")
        if found != canonical:
            rename[found] = canonical
    ds = ds.rename(rename)
    for coord in ("latitude", "longitude"):
        if ds[coord].ndim != 1:
            raise ValueError("Expected rectilinear one-dimensional latitude/longitude")
        dim = ds[coord].dims[0]
        if dim != coord:
            ds = ds.swap_dims({dim: coord})
    data = ds.ssha
    units = str(data.attrs.get("units", "")).lower().strip()
    if units not in {"m", "meter", "meters", "metre", "metres"}:
        raise ValueError(f"Expected SSHA metres, found units={units!r}; inspect the source before conversion")
    if "valid_range" in data.attrs:
        lo, hi = data.attrs["valid_range"]
        data = data.where((data >= lo) & (data <= hi))
    for bound, operator in (("valid_min", np.greater_equal), ("valid_max", np.less_equal)):
        if bound in data.attrs:
            data = data.where(operator(data, data.attrs[bound]))
    for name in str(ds.ssha.attrs.get("ancillary_variables", "")).split():
        flag = ds[name]
        meanings = str(flag.attrs.get("flag_meanings", "")).split()
        values = flag.attrs.get("flag_values")
        masks = flag.attrs.get("flag_masks")
        if not meanings:
            continue
        bad = [i for i, meaning in enumerate(meanings)
               if any(word in meaning.lower() for word in ("bad", "invalid", "land", "missing"))]
        good = [i for i, meaning in enumerate(meanings) if meaning.lower() in ("good", "valid", "good_data")]
        if masks is not None:
            for i in bad:
                data = data.where((flag.fillna(0).astype("int64") & int(masks[i])) == 0)
        elif values is not None and good:
            data = data.where(flag.isin([values[i] for i in good]))
        elif values is not None:
            data = data.where(~flag.isin([values[i] for i in bad]))
        else:
            raise ValueError(f"Cannot interpret ancillary quality flag {name}")
    data = mask_ocean(ds, data)  # ocean basins only; counts == 0 -> NaN (DATA_STANDARD.md)
    data = data.assign_coords(longitude=(data.longitude+180) % 360-180)
    data = data.sortby("latitude").sortby("longitude")
    if len(np.unique(data.longitude)) != data.sizes["longitude"]:
        raise ValueError("Duplicate longitudes after normalization")
    return data * 1000  # metres -> millimetres exactly once


def box_mean(data, bounds):
    """Cos(latitude)-weighted ocean-cell mean in mm, ignoring missing cells."""
    south, north, west, east = bounds
    lon = data.longitude
    longitude_mask = ((lon >= west) & (lon <= east)) if west <= east else ((lon >= west) | (lon <= east))
    part = data.where((data.latitude >= south) & (data.latitude <= north) & longitude_mask, drop=True)
    if not part.size:
        return np.nan
    return float(part.weighted(np.cos(np.deg2rad(part.latitude))).mean(("latitude", "longitude")))


def coarsen_1deg(data):
    """Bin regular <=1-degree grids by degree edges, area-weighting ocean pixels."""
    latitude, longitude = data.latitude.values, data.longitude.values
    for coord in (latitude, longitude):
        if len(coord) > 1 and (np.diff(coord).max() > 1.00001 or np.diff(coord).min() <= 0):
            raise ValueError("Expected sorted native grid at 1 degree or finer")
    latbins = np.floor(np.clip(latitude, -90, 89.999999)).astype(int)
    lonbins = np.floor(longitude).astype(int)
    latlabels, lati = np.unique(latbins, return_inverse=True)
    lonlabels, loni = np.unique(lonbins, return_inverse=True)
    target = (lati[:, None]*len(lonlabels)+loni[None, :]).ravel()
    weights = np.broadcast_to(np.cos(np.deg2rad(latitude))[:, None], data.shape).ravel()
    values = data.values.ravel()
    good = np.isfinite(values)
    count = len(latlabels)*len(lonlabels)
    numerator = np.bincount(target[good], weights=weights[good]*values[good], minlength=count)
    denominator = np.bincount(target[good], weights=weights[good], minlength=count)
    mean = np.divide(numerator, denominator, out=np.full(count, np.nan), where=denominator > 0)
    return xr.DataArray(mean.reshape(len(latlabels), len(lonlabels)), dims=("latitude", "longitude"),
                        coords={"latitude": latlabels+.5, "longitude": lonlabels+.5}, name="ssha")


def parse_indicator(path, key):
    """Inspect ASCII header; choose the unsmoothed index and convert GMSL cm to mm."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    header, records = [], []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("#", "%", ";")):
            header.append(stripped)
            continue
        fields = stripped.replace(",", " ").split()
        if not re.match(r"^\d{4}(?:[-/.]|\b)", fields[0]):
            header.append(stripped)
            continue
        records.append(fields)
    if not records:
        raise ValueError(f"No dated numeric records in {path.name}")
    first = records[0]
    if re.match(r"^\d{4}-\d{2}-\d{2}", first[0]):
        time_columns, mode = 1, "ISO date"
    elif len(first) >= 4 and re.fullmatch(r"\d{4}", first[0]) and 1 <= int(first[1]) <= 12 and 1 <= int(first[2]) <= 31:
        time_columns, mode = 3, "year month day"
    elif len(first) >= 3 and re.fullmatch(r"\d{4}", first[0]) and 1 <= int(first[1]) <= 12:
        time_columns, mode = 2, "year month"
    else:
        time_columns, mode = 1, "decimal year"
    # Prefer an explicitly numbered non-smoothed indicator column in the header.
    value_column = None
    for line in header:
        match = re.search(r"(?:col(?:umn)?\s*)?(\d+)\s*[:.)=-]\s*(.*)", line, re.I)
        if match:
            description = match[2].lower()
            smoothed = "smooth" in description and "unsmooth" not in description
            if (key in description or "indicator" in description or (key == "gmsl" and "sea level" in description)) and not smoothed:
                candidate = int(match[1])-1
                if time_columns <= candidate < len(first):
                    value_column = candidate
    if value_column is None:
        if len(first) == time_columns+1:
            value_column = time_columns
        else:
            # Also recognize a whitespace-separated column heading in the header.
            for line in reversed(header):
                names = line.lstrip("#%; ").replace(",", " ").split()
                if len(names) == len(first):
                    candidates = [i for i, name in enumerate(names) if i >= time_columns
                                  and (key in name.lower() or name.lower() == "indicator")
                                  and ("smooth" not in name.lower() or "unsmooth" in name.lower())]
                    if len(candidates) == 1:
                        value_column = candidates[0]
                        break
    if value_column is None:
        raise ValueError(f"Ambiguous indicator columns in {path.name}; inspect header:\n" + "\n".join(header))
    dates, values = [], []
    for fields in records:
        if mode == "ISO date":
            timestamp = pd.Timestamp(fields[0])
        elif mode.startswith("year month"):
            timestamp = pd.Timestamp(int(fields[0]), int(fields[1]), int(fields[2]) if time_columns == 3 else 1)
        else:
            fractional = float(fields[0])
            year = int(fractional)
            begin, end = pd.Timestamp(year, 1, 1), pd.Timestamp(year+1, 1, 1)
            timestamp = begin+(end-begin)*(fractional-year)
        value = float(fields[value_column])
        dates.append(timestamp)
        values.append(np.nan if abs(value) >= 999 else value*(10 if key == "gmsl" else 1))
    series = pd.Series(values, index=pd.DatetimeIndex(dates, name="date"), name="gmsl_mm" if key == "gmsl" else key)
    inspection = {"file": path.name, "header": header, "date_format": mode,
                  "value_column_1based": value_column+1, "units": "mm (source cm)" if key == "gmsl" else "native indicator unit"}
    return series.sort_index().resample("MS").mean(), inspection


def main():
    ensure_dirs()
    files = sorted([* (RAW / "nasa" / "grid").glob("*.nc"), * (RAW / "nasa" / "grid").glob("*.nc4")])
    if not files:
        raise FileNotFoundError("No NASA grid files in data_raw/nasa/grid")
    weekly, monthly_sum, monthly_count, inspection = [], {}, {}, {}
    template = None
    for number, path in enumerate(files):
        with xr.open_dataset(path, mask_and_scale=True) as ds:
            if number == 0:
                inspection["first_grid"] = {"file": path.name, "dimensions": dict(ds.sizes),
                                            "variables": {name: {"dimensions": list(v.dims),
                                                                   "attributes": {k: str(vv) for k, vv in v.attrs.items()}}
                                                          for name, v in ds.variables.items()}}
                print(f"Inspecting first NASA grid: {path.name}\n{ds}", flush=True)
            data = normalize_grid(ds).load()  # each source file is opened and read once
            if "time" not in data.dims:
                if "time" in ds and ds.time.size == 1:
                    timestamp = pd.Timestamp(ds.time.values.reshape(-1)[0])
                elif "time_coverage_start" in ds.attrs and "time_coverage_end" in ds.attrs:
                    start, end = pd.Timestamp(ds.attrs["time_coverage_start"]), pd.Timestamp(ds.attrs["time_coverage_end"])
                    timestamp = (start+(end-start)/2).tz_localize(None)
                else:
                    raise ValueError(f"No unambiguous observation time in {path.name}")
                data = data.expand_dims(time=[timestamp])
            for time_value in data.time.values:
                field = data.sel(time=time_value).squeeze(drop=True).transpose("latitude", "longitude")
                timestamp = pd.Timestamp(time_value)
                weekly.append({"date": timestamp, **{name: box_mean(field, bounds) for name, bounds in BOXES.items()}})
                coarse = coarsen_1deg(field)
                if template is None:
                    template = coarse
                elif not coarse.latitude.equals(template.latitude) or not coarse.longitude.equals(template.longitude):
                    raise ValueError("Native grid coordinates changed between granules")
                month = timestamp.to_period("M").to_timestamp()
                values = coarse.values
                if month not in monthly_sum:
                    monthly_sum[month] = np.zeros(values.shape)
                    monthly_count[month] = np.zeros(values.shape, dtype="uint16")
                monthly_sum[month] += np.nan_to_num(values, nan=0)
                monthly_count[month] += np.isfinite(values)
        if number % 100 == 0 or number == len(files)-1:
            print(f"NASA grids: {number+1}/{len(files)} read", flush=True)
    frame = pd.DataFrame(weekly).set_index("date").sort_index()
    if frame.index.has_duplicates:
        raise ValueError("Duplicate NASA grid dates; remove overlapping product versions")
    frame.to_csv(PROCESSED / "box_weekly.csv")
    frame.resample("MS").mean().to_csv(PROCESSED / "box_monthly.csv")
    times = sorted(monthly_sum)
    values = [np.divide(monthly_sum[t], monthly_count[t], out=np.full(template.shape, np.nan),
                        where=monthly_count[t] > 0) for t in times]
    grid = xr.DataArray(np.array(values, dtype="float32"), dims=("time", "latitude", "longitude"),
                        coords={"time": times, "latitude": template.latitude, "longitude": template.longitude},
                        name="ssha", attrs={"units": "mm", "aggregation": "cos(latitude) spatial weights; monthly arithmetic mean of weekly grids"})
    grid.to_dataset().to_netcdf(PROCESSED / "grid_1deg_monthly.nc", encoding={"ssha": {"zlib": True, "complevel": 4}})
    indicators, inspection["indicators"] = [], []
    for key in ("gmsl", "enso", "pdo"):
        paths = sorted((RAW / "nasa" / key).glob("*.txt"))
        preferred = RAW / "nasa" / key / f"{NASA_COLLECTIONS[key]}.txt"
        if preferred.exists():
            path = preferred
        elif len(paths) == 1:
            path = paths[0]
        else:
            raise ValueError(f"Cannot select unique current {key} indicator from {paths}")
        series, details = parse_indicator(path, key)
        indicators.append(series)
        inspection["indicators"].append({**details, **metadata(series)})
        print(f"Parsed {path.name}: {details['date_format']}, column {details['value_column_1based']}", flush=True)
    pd.concat(indicators, axis=1).to_csv(PROCESSED / "indicators.csv", index_label="date")
    inspection["ocean_mask"] = dict(GRID_LOG)
    return save_json("nasa_inspection.json", inspection)


if __name__ == "__main__":
    main()
