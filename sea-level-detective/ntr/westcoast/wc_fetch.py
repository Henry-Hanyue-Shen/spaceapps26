"""West Coast gauges: hourly verified water level minus hourly astronomical prediction (NTR), same definition as the
Battery (NOAA CO-OPS, datum MSL, metric, GMT, one JSON per year and product).

Writes westcoast/data_processed/<station>_hourly.csv (time, ntr_m). Raw JSON is cached in westcoast/data_raw/.
"""
import json
import time
from pathlib import Path
import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
RAW, PROCESSED = HERE / "data_raw", HERE / "data_processed"
NOAA_API = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
STATIONS = {"san_francisco": "9414290", "los_angeles": "9410660", "la_jolla": "9410230", "seattle": "9447130"}
FIRST_YEAR, LAST_YEAR = 1980, 2026


def get(station, product, year):
    path = RAW / f"{station}_{product}_{year}.json"
    if path.exists() and path.stat().st_size > 0:
        return json.loads(path.read_text())
    params = dict(product=product, station=station, begin_date=f"{year}0101", end_date=f"{year}1231", datum="MSL",
                  units="metric", time_zone="gmt", format="json", application="SeaLevelDetective")
    if product == "predictions":
        params["interval"] = "h"
    for attempt in range(4):
        try:
            r = requests.get(NOAA_API, params=params, timeout=180)
            if r.status_code == 200:
                payload = r.json()
                if "error" not in payload or "No data" in str(payload.get("error")):
                    path.write_text(json.dumps(payload))
                return payload
        except (requests.RequestException, ValueError) as exc:
            print(f"  {station} {product} {year}: {exc}", flush=True)
        time.sleep(4 * (attempt + 1))
    return {}


def series(payload):
    rows = payload.get("data") or payload.get("predictions") or []
    if not rows:
        return pd.Series(dtype=float)
    s = pd.Series(pd.to_numeric([r["v"] for r in rows], errors="coerce"), index=pd.to_datetime([r["t"] for r in rows]))
    return s[~s.index.duplicated()]


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for name, st in STATIONS.items():
        obs, pred, missing = [], [], []
        for year in range(FIRST_YEAR, LAST_YEAR + 1):
            o, p = series(get(st, "hourly_height", year)), series(get(st, "predictions", year))
            if o.count() < 0.5 * 8760 and year < LAST_YEAR:
                missing.append(f"{year}:{o.count()}h")
            obs.append(o); pred.append(p)
        o, p = pd.concat(obs), pd.concat(pred)
        o, p = o[~o.index.duplicated()], p[~p.index.duplicated()]
        ntr = (o - p.reindex(o.index)).sort_index().rename("ntr_m")
        ntr.to_csv(PROCESSED / f"{st}_hourly.csv", index_label="time")
        print(f"{name} {st}: {ntr.count()} hourly NTR values {ntr.first_valid_index()}..{ntr.last_valid_index()}; "
              f"years with < 50% hours: {', '.join(missing) or 'none'}", flush=True)


if __name__ == "__main__":
    main()
