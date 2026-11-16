"""Altimetry clue map: where does sea-surface height in a month go with New York's next winter of storm surges?

The gridded NASA-SSH product needs an Earthdata login, which this project does not have. NASA GIBS publishes the
JPL MEaSUREs L4 sea-surface-height-anomaly field (gridded multi-mission altimetry, every 5 days, Sep 1992 - Jan 2019)
as public colour-mapped tiles. This script turns those tiles back into numbers with GIBS's own colour scale
(62 colours, 1 cm steps, clipped at +-30 cm), averages three 5-day fields per month on a 2 x 2 degree grid, and then
repeats explore_maps.py's method: for each month Jan..Dec of the season's start year, the Spearman correlation between
the cell's sea-height anomaly and the Oct-Apr surge days at the Battery that follow, linear trends removed from both.
Winters 1993/94 .. 2018/19 (26). Exploratory, like the temperature map; the colour clipping caps the largest anomalies.

Writes results/explore_maps_ssh.json (same layout as explore_maps.json) and data_processed/ssh_gibs_monthly.npz.
"""
import io
import json
import time
import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen, Request
import numpy as np
import pandas as pd
from PIL import Image
from scipy import stats as sp
from config_ntr import RAW, PROCESSED, RESULTS, ensure_dirs
from explore_maps import detrend

LAYER = "JPL_MEaSUREs_L4_Sea_Surface_Height_Anomalies"
URL = "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/{layer}/default/{date}/GoogleMapsCompatible_Level6/1/{y}/{x}.png"
CACHE = RAW / "gibs_ssh"
Z, N = 1, 2                     # zoom 1: 2 x 2 tiles of 256 px = 512 px around the world (0.7 degree per pixel)
LAT = np.arange(-89, 90, 2.0)   # 2 x 2 degree cell centres, as GISTEMP
LON = np.arange(-179, 180, 2.0)


def layer_dates():
    out, d = [], dt.date(1992, 9, 30)
    while d <= dt.date(2017, 10, 19):
        out.append(d); d += dt.timedelta(days=5)
    d = dt.date(2017, 10, 29)
    while d <= dt.date(2019, 1, 22):
        out.append(d); d += dt.timedelta(days=5)
    return out


def fetch(date, y, x):
    f = CACHE / f"{date}_{y}_{x}.png"
    if f.exists() and f.stat().st_size > 0:
        return f.read_bytes()
    for attempt in range(4):
        try:
            b = urlopen(Request(URL.format(layer=LAYER, date=date, y=y, x=x), headers={"User-Agent": "sea-level-detective"}), timeout=60).read()
            f.write_bytes(b)
            return b
        except Exception:
            time.sleep(2 + 3 * attempt)
    return None


def value_lut(rows):
    """32^3 colour cube -> metres (NaN when no colour on the scale is close)."""
    pal = np.array([r[:3] for r in rows], float); val = np.array([r[3] for r in rows], float)
    q = np.arange(32768)
    rgb = np.stack([((q >> 10) << 3) + 4, (((q >> 5) & 31) << 3) + 4, ((q & 31) << 3) + 4], 1).astype(float)
    d = ((rgb[:, None, :] - pal[None, :, :]) ** 2).sum(2)
    k = d.argmin(1)
    return np.where(d[q, k] < 1600, val[k], np.nan)


def frame_to_grid(tiles, lut):
    img = np.zeros((256 * N, 256 * N, 4), np.uint8)
    for (y, x), b in tiles.items():
        img[y * 256:(y + 1) * 256, x * 256:(x + 1) * 256] = np.array(Image.open(io.BytesIO(b)).convert("RGBA"))
    q = ((img[..., 0] >> 3).astype(int) << 10) | ((img[..., 1] >> 3).astype(int) << 5) | (img[..., 2] >> 3).astype(int)
    v = np.where(img[..., 3] >= 128, lut[q], np.nan)
    mw = 256 * N
    g = np.full((len(LAT), len(LON)), np.nan)
    for i, la in enumerate(LAT):
        if abs(la) > 84:
            continue
        rows = []
        for dla in (-0.7, 0.0, 0.7):                     # sample across the cell: 3 x 3 pixels
            phi = np.deg2rad(la + dla)
            rows.append(int((1 - np.log(np.tan(phi) + 1 / np.cos(phi)) / np.pi) / 2 * mw))
        for j, lo in enumerate(LON):
            cols = [int(((lo + dlo + 180) / 360) * mw) % mw for dlo in (-0.7, 0.0, 0.7)]
            block = v[np.ix_(np.clip(rows, 0, mw - 1), cols)]
            if np.isfinite(block).sum() >= 5:
                g[i, j] = np.nanmean(block)
    return g


def main():
    ensure_dirs(); CACHE.mkdir(parents=True, exist_ok=True)
    rows = json.loads((RAW / "explore" / "gibs_colormaps.json").read_text())["ssh"]
    lut = value_lut(rows)
    dates = layer_dates()
    months = pd.period_range("1993-01", "2018-12", freq="M")
    pick = {}
    for p in months:
        ds = [d for d in dates if d.year == p.year and d.month == p.month]
        pick[p] = [ds[k] for k in sorted({0, len(ds) // 2, len(ds) - 1})] if ds else []
    jobs = [(str(d), y, x) for p in months for d in pick[p] for y in range(N) for x in range(N)]
    print(f"{len(months)} months, {sum(len(v) for v in pick.values())} fields, {len(jobs)} tiles", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(24) as ex:
        got = list(ex.map(lambda a: fetch(*a), jobs))
    tiles = {a: b for a, b in zip(jobs, got)}
    print(f"tiles fetched in {time.time() - t0:.0f} s; missing {sum(b is None for b in got)}", flush=True)
    grid = np.full((len(months), len(LAT), len(LON)), np.nan)
    for k, p in enumerate(months):
        fields = []
        for d in pick[p]:
            t = {(y, x): tiles[(str(d), y, x)] for y in range(N) for x in range(N)}
            if all(b for b in t.values()):
                fields.append(frame_to_grid(t, lut))
        if fields:
            with np.errstate(all="ignore"):
                grid[k] = np.nanmean(np.stack(fields), 0)
    np.savez_compressed(PROCESSED / "ssh_gibs_monthly.npz", ssh_m=grid.astype("float32"), lat=LAT, lon=LON,
                        months=np.array([str(p) for p in months]))
    print(f"grid built; ocean cells per month ~{int(np.isfinite(grid).sum((1, 2)).mean())}", flush=True)

    tgt = pd.read_csv(PROCESSED / "ntr_monthly.csv", parse_dates=["date"], index_col="date").asfreq("MS")["surge_days"]
    years = np.arange(1993, 2019)
    y = np.array([tgt.loc[f"{yv}-10":f"{yv + 1}-04"].sum() if tgt.loc[f"{yv}-10":f"{yv + 1}-04"].count() >= 6 else np.nan for yv in years])
    keep = np.isfinite(y)
    yrs = years[keep]; yd = detrend(y[keep], yrs.astype(float)) if keep.sum() >= 30 else y[keep] - np.polyval(np.polyfit(yrs, y[keep], 1), yrs)
    idx = {p: k for k, p in enumerate(months)}
    maps = {}
    for m in range(1, 13):
        field = np.stack([grid[idx[pd.Period(f"{yv}-{m:02d}", "M")]] for yv in yrs])
        cells = []
        for i in range(len(LAT)):
            for j in range(len(LON)):
                x = field[:, i, j]
                ok = np.isfinite(x)
                if ok.sum() < 20 or np.nanstd(x) == 0:
                    continue
                xd = x.copy(); c = np.polyfit(yrs[ok].astype(float), x[ok], 1); xd[ok] = x[ok] - np.polyval(c, yrs[ok])
                r = sp.spearmanr(xd[ok], yd[ok]).statistic
                if np.isfinite(r) and abs(r) >= 0.2:
                    cells.append([float(LAT[i]), float(LON[j]), round(float(r), 3)])
        maps[m] = cells
        print(f"month {m:>2}: {len(cells)} cells |r|>=0.2, max |r| {max([abs(c[2]) for c in cells] or [0]):.2f}", flush=True)
    n = int(keep.sum())
    tc = sp.t.ppf(0.975, n - 2)
    out = {"n_seasons": n, "years": [int(yrs[0]), int(yrs[-1])], "r_p05": float(tc / np.sqrt(n - 2 + tc ** 2)), "maps": maps,
           "source": "NASA JPL MEaSUREs L4 gridded sea-surface-height anomaly (via NASA GIBS tiles, GIBS colour scale inverted; +-30 cm clip)",
           "note": "Spearman correlation after removing linear trends; exploratory, no field-significance correction."}
    (RESULTS / "explore_maps_ssh.json").write_text(json.dumps(out, separators=(",", ":")))
    nino = [c for c in maps[6] if -5 <= c[0] <= 5 and -170 <= c[1] <= -120]
    print(f"June, Nino3.4 box: {len(nino)} cells kept, mean r {np.mean([c[2] for c in nino]) if nino else float('nan'):+.2f}; n={n}, r_p05={out['r_p05']:.2f}")


if __name__ == "__main__":
    main()
