"""West Coast version of site/data/local_gauges.json: monthly mean sea level at West Coast tide gauges.

NOAA CO-OPS monthly_mean, datum MSL, metric, mm; each month minus the same calendar month's 1993-2012 average
(same baseline as the New York file), rounded to whole mm, months 1980-01 .. latest. Los Angeles comes first with
id "battery", because the globe draws gauges[0] / id "battery" as the target gauge.
Check: the same code is run on the cached New York Boston file and compared with the published Boston values.
Writes site_data/local_gauges_west.json.
"""
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
RAW, OUT = HERE / "data_raw" / "monthly_mean", HERE / "site_data"
NOAA_API = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
GAUGES = [("battery", "9410660", "Los Angeles, CA"), ("la_jolla", "9410230", "La Jolla, CA"),
          ("san_diego", "9410170", "San Diego, CA"), ("santa_barbara", "9411340", "Santa Barbara, CA"),
          ("port_san_luis", "9412110", "Port San Luis, CA"), ("monterey", "9413450", "Monterey, CA"),
          ("san_francisco", "9414290", "San Francisco, CA"), ("crescent_city", "9419750", "Crescent City, CA"),
          ("astoria", "9439040", "Astoria, OR"), ("neah_bay", "9443090", "Neah Bay, WA"), ("seattle", "9447130", "Seattle, WA")]


def chunk(st, y0):
    p = RAW / f"msl_{st}_{y0}.json"
    if p.exists() and p.stat().st_size > 0:
        return json.loads(p.read_text())
    params = dict(product="monthly_mean", station=st, begin_date=f"{y0}0101", end_date=f"{min(y0 + 9, 2026)}1231",
                  datum="MSL", units="metric", time_zone="gmt", format="json", application="SeaLevelDetective")
    for attempt in range(4):
        try:
            r = requests.get(NOAA_API, params=params, timeout=120)
            if r.status_code == 200:
                p.write_text(r.text)
                return r.json()
        except requests.RequestException as exc:
            print(f"  {st} {y0}: {exc}", flush=True)
        time.sleep(3 * (attempt + 1))
    return {}


def monthly(payloads):
    parts, meta = {}, {}
    for pl in payloads:
        meta = pl.get("metadata", meta) or meta
        for r in pl.get("data", []):
            v = pd.to_numeric(r.get("MSL"), errors="coerce")
            parts[pd.Timestamp(int(r["year"]), int(r["month"]), 1)] = float(v) * 1000 if pd.notna(v) else np.nan
    return pd.Series(parts).sort_index(), meta


def anomaly(s):
    base = s.loc["1993-01":"2012-12"]
    clim = base.groupby(base.index.month).mean()
    return s - clim.reindex(s.index.month).to_numpy()


def main():
    RAW.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
    # check against the New York file's Boston series, built from the New York cache
    ny = HERE.parent / "data_raw" / "explore"
    b, _ = monthly([json.loads((ny / f"msl_8443970_{y0}.json").read_text()) for y0 in range(1970, 2030, 10)])
    print("Boston check (first 5, published -116 -70 -128 -93 -56):", [int(round(v)) for v in anomaly(b).loc["1980-01":"1980-05"]])
    series, gauges = {}, []
    for gid, st, name in GAUGES:
        s, meta = monthly([chunk(st, y0) for y0 in range(1970, 2030, 10)])
        if s.count() < 120:
            print(f"{name} {st}: only {s.count()} months, skipped", flush=True)
            continue
        series[gid] = anomaly(s)
        gauges.append({"id": gid, "name": name, "lat": round(float(meta["lat"]), 2), "lon": round(float(meta["lon"]), 2), "station": st})
        print(f"{name} {st}: {s.count()} months {s.first_valid_index():%Y-%m}..{s.last_valid_index():%Y-%m}, "
              f"base months {s.loc['1993':'2012'].count()}/240", flush=True)
    last = max(v.last_valid_index() for v in series.values())
    months = pd.date_range("1980-01-01", last, freq="MS")
    for g in gauges:
        a = series[g["id"]].reindex(months)
        g["anom"] = [None if pd.isna(v) else int(round(v)) for v in a]
    # keep the New York key set: id, name, lat, lon, anom (station number moved into the name list below)
    stations = {g["id"]: g.pop("station") for g in gauges}
    out = {"months": [f"{m:%Y-%m}" for m in months], "baseline": "same calendar month, 1993-2012 average = 0", "units": "mm",
           "gauges": gauges}
    (OUT / "local_gauges_west.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"local_gauges_west.json: {len(gauges)} gauges, {len(months)} months to {last:%Y-%m}; stations {stations}")


if __name__ == "__main__":
    main()
