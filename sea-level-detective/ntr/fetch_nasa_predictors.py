"""NASA predictors for the NTR study (needs an Earthdata token).

MERRA-2 monthly single-level fields (M2TMNXSLV, NASA GMAO), read remotely with earthaccess (only the needed values):
  nao_merra2   station-style NAO: z(SLP Azores) - z(SLP Iceland), each standardized per calendar month over TRAIN,
               then the difference standardized again (dimensionless)
  wind_ne_ms   NY Bight box-mean 10 m wind projected on the direction toward the SW (i.e. wind FROM the NE), m/s
Writes data_processed/merra2_predictors.csv. ENSO (NASA_SSH_ENSO_INDICATOR) and the Gulf Stream SSH difference are read
from ../pipeline/data_processed/ by model.py.
"""
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import earthaccess
from config_ntr import (PROCESSED, MERRA2, NAO_POINTS, NY_BIGHT_BOX, WIND_FROM_NE, FIRST_YEAR, LAST_YEAR, TRAIN,
                        ensure_dirs)


def login():
    secret = Path("/secrets/earthdata_token")
    if not os.environ.get("EARTHDATA_TOKEN") and secret.exists():
        os.environ["EARTHDATA_TOKEN"] = secret.read_text().strip()
    if not os.environ.get("EARTHDATA_TOKEN"):
        raise SystemExit("No Earthdata token: set EARTHDATA_TOKEN or mount it at /secrets/earthdata_token")
    auth = earthaccess.login(strategy="environment")
    if not auth.authenticated:
        raise SystemExit("Earthdata login failed")


def read_one(fileobj):
    with xr.open_dataset(fileobj, engine="h5netcdf") as ds:
        t = pd.Timestamp(ds.time.values[0]).to_period("M").to_timestamp()
        row = {"date": t}
        for name, (lat, lon) in NAO_POINTS.items():
            row[f"slp_{name}_hpa"] = float(ds.SLP.isel(time=0).sel(lat=lat, lon=lon, method="nearest")) / 100
        s, n, w, e = NY_BIGHT_BOX
        box = ds[["U10M", "V10M"]].isel(time=0).sel(lat=slice(s, n), lon=slice(w, e))
        wts = np.cos(np.deg2rad(box.lat))
        u = float(box.U10M.weighted(wts).mean(("lat", "lon")))
        v = float(box.V10M.weighted(wts).mean(("lat", "lon")))
        row["wind_ne_ms"] = WIND_FROM_NE[0] * u + WIND_FROM_NE[1] * v
        return row


def main():
    ensure_dirs()
    login()
    granules = earthaccess.search_data(short_name=MERRA2, temporal=(f"{FIRST_YEAR}-01-01", f"{LAST_YEAR}-12-31"))
    print(f"MERRA-2 {MERRA2}: {len(granules)} monthly granules", flush=True)
    files = earthaccess.open(granules)
    with ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(read_one, files))
    df = pd.DataFrame(rows).set_index("date").sort_index()
    df = df[~df.index.duplicated()]
    train = df.loc[TRAIN[0]:TRAIN[1]]
    z = {}
    for name in NAO_POINTS:
        col = f"slp_{name}_hpa"
        clim = train[col].groupby(train.index.month).agg(["mean", "std"])
        z[name] = (df[col] - clim["mean"].reindex(df.index.month).to_numpy()) / clim["std"].reindex(df.index.month).to_numpy()
    nao = z["azores"] - z["iceland"]
    df["nao_merra2"] = nao / nao.loc[TRAIN[0]:TRAIN[1]].std()
    df.to_csv(PROCESSED / "merra2_predictors.csv", index_label="date")
    print(f"MERRA-2 predictors: {len(df)} months, {df.index.min():%Y-%m}..{df.index.max():%Y-%m}", flush=True)


if __name__ == "__main__":
    main()
