"""Fetch every candidate predictor for the NTR exploration (all public, no login). Cached under data_raw/explore/.

NASA
  NASA POWER (MERRA-2 based, power.larc.nasa.gov): daily U10M, V10M, SLP at the NY Bight; monthly SLP at Iceland,
      Azores, Aleutian low and the polar cap -> wind, storminess, NASA NAO, North Pacific index, polar pressure.
  NASA GISTEMP v4 gridded (data.giss.nasa.gov): sea-surface temperature indices (Nino3.4, North Atlantic, subpolar
      gyre, NW Atlantic shelf, tropical North Atlantic), each minus the global mean.
NOAA / others
  CPC ONI, NAO, AO, PNA, QBO; NCEI PDO; NSIDC Arctic sea-ice extent; CO-OPS monthly mean sea level at Bermuda and
  East Coast gauges; USGS Hudson River discharge; hourly NTR at five more East Coast gauges.
Writes data_processed/explore_monthly.csv (one column per raw predictor) and explore_sources.json.
"""
import gzip
import io
import json
import re
import shutil
import time
import numpy as np
import pandas as pd
import requests
import xarray as xr
from config_ntr import RAW, PROCESSED, NOAA_API, ONI_URL, FIRST_YEAR, LAST_YEAR, WIND_FROM_NE, ensure_dirs

EX = RAW / "explore"
SOURCES = {}
GAUGES = {"bermuda": "2695540", "portland": "8418150", "boston": "8443970", "montauk": "8510560",
          "kings_point": "8516945", "sandy_hook": "8531680", "atlantic_city": "8534720",
          "sewells_point": "8638610", "charleston": "8665530", "key_west": "8724580"}
SURGE_STATIONS = {"boston": "8443970", "sandy_hook": "8531680", "atlantic_city": "8534720",
                  "sewells_point": "8638610", "charleston": "8665530"}
POWER_POINTS = {"iceland": (65.08, -22.73), "azores": (37.74, -25.68), "aleutian": (50.0, -165.0),
                "polar": (85.0, 0.0), "nybight": (40.25, -73.0)}


def cached(name, url, params=None, binary=False, tries=4):
    path = EX / name
    if path.exists() and path.stat().st_size > 0:
        return path
    for attempt in range(tries):
        try:
            r = requests.get(url, params=params, timeout=300, headers={"User-Agent": "SeaLevelDetective/1.0"})
            if r.status_code == 200 and len(r.content) > 20:
                path.write_bytes(r.content) if binary else path.write_text(r.text, encoding="utf-8")
                return path
            print(f"  {name}: HTTP {r.status_code}, retry", flush=True)
        except requests.RequestException as exc:
            print(f"  {name}: {exc}", flush=True)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"Could not fetch {name} from {url}")


def ym_index(years, months):
    return pd.to_datetime(dict(year=years, month=months, day=1))


# ----------------------------------------------------------------------------------------- NASA POWER
def power_monthly(name, lat, lon):
    for end in (2026, 2025):
        try:
            p = cached(f"power_monthly_{name}_{end}.json", "https://power.larc.nasa.gov/api/temporal/monthly/point",
                       dict(parameters="SLP,TS", community="RE", longitude=lon, latitude=lat, start=1981, end=end, format="JSON"), tries=2)
            break
        except RuntimeError:
            continue
    par = json.loads(p.read_text())["properties"]["parameter"]
    out = {}
    for var, d in par.items():
        s = pd.Series({pd.Timestamp(int(k[:4]), int(k[4:]), 1): v for k, v in d.items() if int(k[4:]) <= 12}, dtype=float)
        out[var] = s.where(s > -900).sort_index()
    return out


def power_daily_nybight():
    lat, lon = POWER_POINTS["nybight"]
    parts = []
    for start, end in (("19810101", "19951231"), ("19960101", "20101231"), ("20110101", f"{LAST_YEAR}1031")):
        p = cached(f"power_daily_nybight_{start}.json", "https://power.larc.nasa.gov/api/temporal/daily/point",
                   dict(parameters="U10M,V10M,SLP", community="RE", longitude=lon, latitude=lat, start=start, end=end, format="JSON"))
        par = json.loads(p.read_text())["properties"]["parameter"]
        parts.append(pd.DataFrame({k: pd.Series(v, dtype=float) for k, v in par.items()}))
    d = pd.concat(parts)
    d.index = pd.to_datetime(d.index, format="%Y%m%d")
    return d.where(d > -900).sort_index()


# ----------------------------------------------------------------------------------------- NASA GISTEMP
def gistemp_indices():
    gz = cached("gistemp1200_GHCNv4_ERSSTv5.nc.gz", "https://data.giss.nasa.gov/pub/gistemp/gistemp1200_GHCNv4_ERSSTv5.nc.gz", binary=True)
    nc = EX / "gistemp1200.nc"
    if not nc.exists():
        with gzip.open(gz, "rb") as fi, open(nc, "wb") as fo:
            shutil.copyfileobj(fi, fo)
    ds = xr.open_dataset(nc)
    t = ds["tempanomaly"].sel(time=slice(f"{FIRST_YEAR}-01-01", None))
    w = np.cos(np.deg2rad(t.lat))

    def box(s, n, west, east):
        return t.sel(lat=slice(s, n), lon=slice(west, east)).weighted(w).mean(("lat", "lon")).to_series()
    glob = box(-60, 60, -180, 180)
    out = {"nino34_giss": box(-5, 5, -170, -120) - glob, "natl_giss": box(0, 60, -80, 0) - glob,
           "subpolar_giss": box(50, 60, -50, -20) - glob, "nwatl_shelf_giss": box(35, 45, -75, -60) - glob,
           "trop_natl_giss": box(10, 20, -80, -20) - glob}
    for s in out.values():
        s.index = s.index.to_period("M").to_timestamp()
    return out


# ----------------------------------------------------------------------------------------- NOAA indices
def cpc_three_col(name, url):
    df = pd.read_csv(cached(name, url), sep=r"\s+", header=None, names=["y", "m", "v"])
    s = pd.Series(df.v.to_numpy(), index=ym_index(df.y, df.m))
    return s.where(s.abs() < 90)


def yearly_table(name, url, missing=90):
    """Rows of 'YYYY v1..v12'; the first occurrence of each year is kept (QBO file repeats blocks)."""
    seen, rows = set(), []
    for line in cached(name, url).read_text().splitlines():
        m = re.match(r"^\s*((?:18|19|20)\d\d)((?:\s+-?\d*\.\d+){12})\s*$", line)
        if m and m[1] not in seen:
            seen.add(m[1])
            for i, v in enumerate(m[2].split()):
                rows.append((pd.Timestamp(int(m[1]), i + 1, 1), float(v)))
    s = pd.Series(dict(rows)).sort_index()
    return s.where(s.abs() < missing)


def oni():
    df = pd.read_csv(cached("oni.txt", ONI_URL), sep=r"\s+")
    seasons = "DJF JFM FMA MAM AMJ MJJ JJA JAS ASO SON OND NDJ".split()
    return pd.Series(df.ANOM.to_numpy(), index=ym_index(df.YR, df.SEAS.map({s: i + 1 for i, s in enumerate(seasons)})))


def sea_ice():
    parts = []
    for m in range(1, 13):
        p = cached(f"seaice_N_{m:02d}.csv", f"https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/N_{m:02d}_extent_v4.0.csv")
        df = pd.read_csv(p, skipinitialspace=True)
        df.columns = [c.strip() for c in df.columns]
        parts.append(pd.Series(df["extent"].to_numpy(), index=ym_index(df["year"], df["mo"])))
    s = pd.concat(parts).sort_index()
    return s.where(s > 0)


# ----------------------------------------------------------------------------------------- gauges, river
def gauge_monthly(station):
    parts = []
    for y0 in range(1970, LAST_YEAR + 1, 10):
        p = cached(f"msl_{station}_{y0}.json", NOAA_API,
                   dict(product="monthly_mean", station=station, begin_date=f"{y0}0101", end_date=f"{min(y0 + 9, LAST_YEAR)}1231",
                        datum="MSL", units="metric", time_zone="gmt", format="json", application="SeaLevelDetective"))
        for r in json.loads(p.read_text()).get("data", []):
            v = pd.to_numeric(r.get("MSL"), errors="coerce")
            parts.append((pd.Timestamp(int(r["year"]), int(r["month"]), 1), float(v) * 1000 if pd.notna(v) else np.nan))
    return pd.Series(dict(parts)).sort_index()


def hudson():
    p = cached("usgs_hudson.rdb", "https://waterservices.usgs.gov/nwis/stat/",
               dict(format="rdb", sites="01358000", statReportType="monthly", statTypeCd="mean", parameterCd="00060",
                    startDT=f"{FIRST_YEAR}-01", endDT=f"{LAST_YEAR}-10"))
    lines = [l for l in p.read_text().splitlines() if l and not l.startswith("#")]
    df = pd.read_csv(io.StringIO("\n".join(lines)), sep="\t").iloc[1:]
    return pd.Series(pd.to_numeric(df["mean_va"]).to_numpy(), index=ym_index(df["year_nu"].astype(int), df["month_nu"].astype(int))).sort_index()


def hourly_ntr(station):
    """Hourly NTR (m) for another gauge, same definition as the Battery."""
    obs, pred = [], []
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        for product, store in (("hourly_height", obs), ("predictions", pred)):
            params = dict(product=product, station=station, begin_date=f"{year}0101", end_date=f"{year}1231", datum="MSL",
                          units="metric", time_zone="gmt", format="json", application="SeaLevelDetective")
            if product == "predictions":
                params["interval"] = "h"
            try:
                payload = json.loads(cached(f"{station}_{product}_{year}.json", NOAA_API, params, tries=2).read_text())
            except RuntimeError:
                continue
            rows = payload.get("data") or payload.get("predictions") or []
            if rows:
                store.append(pd.Series(pd.to_numeric([r["v"] for r in rows], errors="coerce"), index=pd.to_datetime([r["t"] for r in rows])))
    if not obs or not pred:
        return None
    o, p = pd.concat(obs), pd.concat(pred)
    o, p = o[~o.index.duplicated()], p[~p.index.duplicated()]
    return (o - p.reindex(o.index)).sort_index()


def main():
    ensure_dirs()
    EX.mkdir(parents=True, exist_ok=True)
    cols = {}

    def add(name, series, source, nasa=False):
        s = series.copy()
        s.index = pd.DatetimeIndex(s.index).to_period("M").to_timestamp()
        cols[name] = s.groupby(level=0).mean()
        SOURCES[name] = {"source": source, "nasa": nasa}
        print(f"{name}: {cols[name].count()} months {cols[name].first_valid_index():%Y-%m}..{cols[name].last_valid_index():%Y-%m}", flush=True)

    # NASA POWER
    pm = {k: power_monthly(k, *POWER_POINTS[k]) for k in ("iceland", "azores", "aleutian", "polar")}
    add("slp_iceland_power", pm["iceland"]["SLP"], "NASA POWER (MERRA-2) SLP, 65.08N 22.73W, kPa", True)
    add("slp_azores_power", pm["azores"]["SLP"], "NASA POWER (MERRA-2) SLP, 37.74N 25.68W, kPa", True)
    add("npi_power", pm["aleutian"]["SLP"], "NASA POWER (MERRA-2) SLP at 50N 165W (Aleutian low / North Pacific index proxy)", True)
    add("polar_slp_power", pm["polar"]["SLP"], "NASA POWER (MERRA-2) SLP at 85N (polar pressure, AO proxy)", True)
    d = power_daily_nybight()
    d.to_csv(PROCESSED / "power_daily_nybight.csv", index_label="date")
    wind_ne = WIND_FROM_NE[0] * d["U10M"] + WIND_FROM_NE[1] * d["V10M"]
    add("wind_ne_power", wind_ne.resample("MS").mean(), "NASA POWER (MERRA-2) NY Bight 10 m wind from the NE, m/s", True)
    add("slp_nybight_power", d["SLP"].resample("MS").mean(), "NASA POWER (MERRA-2) NY Bight SLP, kPa", True)
    add("storminess_power", d["SLP"].resample("MS").std(), "NASA POWER (MERRA-2) NY Bight: SD of daily SLP within the month", True)
    # NASA GISTEMP
    for k, s in gistemp_indices().items():
        add(k, s, f"NASA GISTEMP v4 gridded, box mean minus 60S-60N mean ({k})", True)
    # NOAA indices
    add("oni", oni(), "NOAA CPC Oceanic Nino Index")
    add("nao_cpc", cpc_three_col("nao.txt", "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii"), "NOAA CPC NAO")
    add("ao_cpc", cpc_three_col("ao.txt", "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii"), "NOAA CPC AO")
    add("pna_cpc", cpc_three_col("pna.txt", "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.pna.monthly.b5001.current.ascii"), "NOAA CPC PNA")
    add("qbo_cpc", yearly_table("qbo.txt", "https://www.cpc.ncep.noaa.gov/data/indices/qbo.u50.index", missing=900), "NOAA CPC QBO 50 hPa zonal wind")
    add("pdo_ncei", yearly_table("pdo.txt", "https://www.ncei.noaa.gov/pub/data/cmb/ersst/v5/index/ersst.v5.pdo.dat"), "NOAA NCEI PDO (ERSST v5)")
    add("seaice_arctic", sea_ice(), "NSIDC Sea Ice Index v4, Arctic extent (NASA DAAC at NSIDC)")
    # gauges and river
    for name, st in GAUGES.items():
        add(f"msl_{name}", gauge_monthly(st), f"NOAA CO-OPS {st} monthly mean sea level, mm")
    add("hudson_flow", hudson(), "USGS 01358000 Hudson River at Green Island, monthly mean discharge")
    pd.DataFrame(cols).sort_index().loc[f"{FIRST_YEAR}-01-01":].to_csv(PROCESSED / "explore_monthly.csv", index_label="date")
    (PROCESSED / "explore_sources.json").write_text(json.dumps(SOURCES, indent=1))
    # hourly NTR at other gauges -> surge days per month (same definition as the Battery)
    from config_ntr import SURGE_THRESHOLD_M
    surge = {}
    for name, st in SURGE_STATIONS.items():
        h = hourly_ntr(st)
        if h is None:
            print(f"surge {name}: no data", flush=True)
            continue
        ok = h.resample("D").count() >= 20
        dm = h.resample("D").mean().where(ok)
        days = ((dm - dm.rolling(365, center=True, min_periods=300).mean()) > SURGE_THRESHOLD_M) & ok
        hours = h.resample("MS").count()
        expected = hours.index.days_in_month * 24
        surge[name] = days.resample("MS").sum().astype(float).where(hours >= 0.8 * expected)
        print(f"surge {name}: {int(surge[name].sum())} surge days, {surge[name].count()} valid months", flush=True)
    pd.DataFrame(surge).to_csv(PROCESSED / "explore_surge_days.csv", index_label="date")


if __name__ == "__main__":
    main()
