"""Where on Earth, and how far ahead, is New York Harbor's surge season written?

1. Teleconnection maps (NASA GISTEMP v4, 2 x 2 degree): for each month Jan..Dec of the season's start year, the
   Spearman correlation between the cell's temperature anomaly in that month and the Oct-Apr surge days at the
   Battery that follow. A linear trend in time is removed from both first. Seasons 1981-2025 (n about 43).
   Exploratory: thousands of cells, no field-significance correction; the confirmed predictor is the Nino3.4 box.
2. Space-time table: every predictor's location, great-circle distance to the Battery, same-month correlation with
   monthly NTR (prewhitened, train) and season-ahead skill (leave-one-out), from explore.json.
Writes results/explore_maps.json and results/explore_space_time.json.
"""
import json
import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats as sp
from config_ntr import RAW, PROCESSED, RESULTS, ensure_dirs

BATTERY = (40.70, -74.01)
LOC = {  # representative location of each predictor (lat, lon) and a readable name
    "oni": (0, -145, "Equatorial Pacific (NOAA ONI)"), "nino34_giss": (0, -145, "Equatorial Pacific (NASA GISTEMP Nino3.4)"),
    "pdo_ncei": (40, -170, "North Pacific (PDO)"), "npi_power": (50, -165, "Aleutian low (NASA POWER)"),
    "pna_cpc": (55, -115, "Pacific-North America pattern"), "nao_cpc": (51, -24, "North Atlantic (NOAA NAO)"),
    "nao_power": (51, -24, "North Atlantic (NASA POWER NAO)"), "ao_cpc": (85, 0, "Arctic (AO)"),
    "polar_slp_power": (85, 0, "Arctic pressure (NASA POWER)"), "qbo_cpc": (1, 104, "Tropical stratosphere (QBO)"),
    "seaice_arctic": (80, -170, "Arctic sea ice"), "natl_giss": (30, -40, "North Atlantic SST (NASA GISTEMP)"),
    "subpolar_giss": (55, -35, "Subpolar gyre SST (NASA GISTEMP)"), "nwatl_shelf_giss": (40, -67, "NW Atlantic shelf SST (NASA GISTEMP)"),
    "trop_natl_giss": (15, -50, "Tropical N. Atlantic SST (NASA GISTEMP)"), "wind_ne_power": (40.25, -73, "NY Bight wind (NASA POWER)"),
    "slp_nybight_power": (40.25, -73, "NY Bight pressure (NASA POWER)"), "storminess_power": (40.25, -73, "NY Bight storminess (NASA POWER)"),
    "msl_bermuda": (32.37, -64.70, "Bermuda sea level"), "msl_portland": (43.66, -70.25, "Portland sea level"),
    "msl_boston": (42.35, -71.05, "Boston sea level"), "msl_montauk": (41.05, -71.96, "Montauk sea level"),
    "msl_kings_point": (40.81, -73.77, "Kings Point sea level"), "msl_sandy_hook": (40.47, -74.01, "Sandy Hook sea level"),
    "msl_atlantic_city": (39.36, -74.42, "Atlantic City sea level"), "msl_sewells_point": (36.95, -76.33, "Sewells Point sea level"),
    "msl_charleston": (32.78, -79.92, "Charleston sea level"), "msl_key_west": (24.55, -81.81, "Key West sea level"),
    "hudson_flow": (42.75, -73.69, "Hudson River discharge")}


def gc_km(a, b):
    la1, lo1, la2, lo2 = map(np.deg2rad, (a[0], a[1], b[0], b[1]))
    h = np.sin((la2 - la1) / 2) ** 2 + np.cos(la1) * np.cos(la2) * np.sin((lo2 - lo1) / 2) ** 2
    return float(2 * 6371 * np.arcsin(np.sqrt(h)))


def detrend(v, t):
    ok = np.isfinite(v)
    if ok.sum() < 30:
        return np.full_like(v, np.nan, dtype=float)
    c = np.polyfit(t[ok], v[ok], 1)
    return v - np.polyval(c, t)


def main():
    ensure_dirs()
    tgt = pd.read_csv(PROCESSED / "ntr_monthly.csv", parse_dates=["date"], index_col="date").asfreq("MS")["surge_days"]
    years = np.arange(1980, 2026)   # same 43 complete winters as the season models (1980/81 .. 2025/26)
    y = np.array([tgt.loc[f"{yv}-10":f"{yv + 1}-04"].sum() if tgt.loc[f"{yv}-10":f"{yv + 1}-04"].count() >= 6 else np.nan for yv in years])
    keep = np.isfinite(y)
    yrs, yd = years[keep], detrend(y[keep], years[keep].astype(float))
    ds = xr.open_dataset(RAW / "explore" / "gistemp1200.nc")
    T = ds["tempanomaly"]
    lat, lon = T.lat.values, T.lon.values
    maps = {}
    for m in range(1, 13):
        field = np.stack([T.sel(time=f"{yv}-{m:02d}").values.squeeze() for yv in yrs])     # (season, lat, lon)
        cells = []
        for i in range(len(lat)):
            for j in range(len(lon)):
                x = detrend(field[:, i, j].astype(float), yrs.astype(float))
                ok = np.isfinite(x)
                if ok.sum() < 35:
                    continue
                r = sp.spearmanr(x[ok], yd[ok]).statistic
                if abs(r) >= 0.2:
                    cells.append([float(lat[i]), float(lon[j]), round(float(r), 3)])
        maps[m] = cells
        strong = [c for c in cells if abs(c[2]) >= 0.3]
        print(f"month {m:>2}: {len(cells)} cells with |r|>=0.2, {len(strong)} with |r|>=0.3, max |r| {max(abs(c[2]) for c in cells):.2f}", flush=True)
    n = int(keep.sum())
    out = {"n_seasons": n, "years": [int(yrs[0]), int(yrs[-1])], "r_p05": float(sp.t.ppf(0.975, n - 2) / np.sqrt(n - 2 + sp.t.ppf(0.975, n - 2) ** 2)),
           "battery": BATTERY, "nino34_box": [-5, 5, -170, -120], "maps": maps,
           "note": "Spearman correlation after removing linear trends; exploratory, no field-significance correction."}
    (RESULTS / "explore_maps.json").write_text(json.dumps(out, separators=(",", ":")))

    ex = json.loads((RESULTS / "explore.json").read_text())
    lag0 = ex["monthly"]["mean NTR, all months"]["lag0"]
    season = {r["predictor"]: r for r in ex["season"]["table"]}
    rows = []
    for name, (la, lo, label) in LOC.items():
        s = season.get(name, {})
        rows.append({"predictor": name, "label": label, "lat": la, "lon": lo, "distance_km": round(gc_km(BATTERY, (la, lo))),
                     "nasa": bool(ex["sources"].get(name, {}).get("nasa", False)),
                     "same_month_r": lag0.get(name), "season_loo_skill": s.get("loo_skill"), "season_test_skill": s.get("test_skill"),
                     "season_rr": s.get("rr_all"), "season_confirmed": bool(s.get("confirmed", False))})
    (RESULTS / "explore_space_time.json").write_text(json.dumps(rows, indent=1))
    for r in sorted(rows, key=lambda r: r["distance_km"]):
        print(f"{r['distance_km']:>6} km  {r['label'][:44]:<44} same-month r {r['same_month_r'] if r['same_month_r'] is not None else float('nan'):+.2f}  "
              f"season LOO {r['season_loo_skill'] if r['season_loo_skill'] is not None else float('nan'):+.3f}  {'CONFIRMED' if r['season_confirmed'] else ''}")


if __name__ == "__main__":
    main()
