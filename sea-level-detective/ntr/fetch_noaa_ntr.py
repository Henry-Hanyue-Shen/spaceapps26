"""NOAA (no login): Battery hourly observed water level and hourly tide predictions, ONI and CPC NAO.

Writes data_processed/ntr_hourly.csv (time, obs_m, pred_m, ntr_m), oni.csv, cpc_nao.csv.
NTR = observed hourly height minus predicted astronomical tide, both on datum MSL, metres, GMT.
"""
import io
import json
import time
import pandas as pd
import requests
from config_ntr import (RAW, PROCESSED, STATION, FIRST_YEAR, LAST_YEAR, NOAA_API, ONI_URL, CPC_NAO_URL, ensure_dirs)


def get_json(params, path):
    if path.exists():
        return json.loads(path.read_text())
    for attempt in range(3):
        r = requests.get(NOAA_API, params=params, timeout=120)
        if r.status_code == 200:
            payload = r.json()
            path.write_text(json.dumps(payload))
            return payload
        time.sleep(3 * (attempt + 1))
    r.raise_for_status()


def fetch_year(year, product):
    params = dict(product=product, station=STATION, begin_date=f"{year}0101", end_date=f"{year}1231",
                  datum="MSL", units="metric", time_zone="gmt", format="json", application="SeaLevelDetective")
    if product == "predictions":
        params["interval"] = "h"
    payload = get_json(params, RAW / f"{STATION}_{product}_{year}.json")
    rows = payload.get("data") or payload.get("predictions") or []
    if not rows:
        msg = str(payload.get("error", ""))
        print(f"  {year} {product}: no data {msg[:80]}", flush=True)
        return pd.Series(dtype=float)
    s = pd.Series(pd.to_numeric([r["v"] for r in rows], errors="coerce"),
                  index=pd.to_datetime([r["t"] for r in rows]))
    return s[~s.index.duplicated()]


def main():
    ensure_dirs()
    obs, pred = [], []
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        o, p = fetch_year(year, "hourly_height"), fetch_year(year, "predictions")
        obs.append(o); pred.append(p)
        print(f"{year}: {o.count()} observed hours, {p.count()} predicted hours", flush=True)
    frame = pd.concat([pd.concat(obs).rename("obs_m"), pd.concat(pred).rename("pred_m")], axis=1).sort_index()
    frame = frame[~frame.index.duplicated()]
    frame["ntr_m"] = frame["obs_m"] - frame["pred_m"]
    frame.to_csv(PROCESSED / "ntr_hourly.csv", index_label="time")
    # ONI: three-month seasons mapped to the central month (degrees C)
    oni = pd.read_csv(io.StringIO(requests.get(ONI_URL, timeout=60).text), sep=r"\s+")
    seasons = "DJF JFM FMA MAM AMJ MJJ JJA JAS ASO SON OND NDJ".split()
    oni["month"] = oni.SEAS.map({s: i + 1 for i, s in enumerate(seasons)})
    oni.index = pd.to_datetime(dict(year=oni.YR, month=oni.month, day=1))
    oni["ANOM"].rename("oni").to_csv(PROCESSED / "oni.csv", index_label="date")
    # CPC NAO (standardized monthly index)
    nao = pd.read_csv(io.StringIO(requests.get(CPC_NAO_URL, timeout=60).text), sep=r"\s+", header=None,
                      names=["year", "month", "nao"])
    nao.index = pd.to_datetime(dict(year=nao.year, month=nao.month, day=1))
    nao["nao"].to_csv(PROCESSED / "cpc_nao.csv", index_label="date")
    print(f"NOAA: {frame['ntr_m'].count()} hourly NTR values, ONI {len(oni)}, NAO {len(nao)} months", flush=True)


if __name__ == "__main__":
    main()
