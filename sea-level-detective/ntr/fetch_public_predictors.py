"""Public, no-login predictors for the NTR study (used when the NASA/MERRA-2 versions are not available).

Source: NCEP/NCAR Reanalysis 1 (NOAA), monthly means, served by the IRI/LDEO Data Library (Columbia University):
  nao_ncep     station-style NAO from mean sea-level pressure at Ponta Delgada and Stykkisholmur grid points:
               z(Azores) - z(Iceland), each standardized per calendar month over TRAIN, then re-standardized
  wind_ne_ms   10 m wind over the NY Bight (box 38-42N, 76-70W, wide enough to hold several 1.9-degree grid points),
               projected on the direction toward the SW (wind FROM the NE), m/s
Writes data_processed/public_predictors.csv. Same definitions as fetch_nasa_predictors.py (MERRA-2).
"""
import io
import numpy as np
import pandas as pd
import requests
from config_ntr import PROCESSED, NAO_POINTS, TRAIN, FIRST_YEAR, WIND_FROM_NE, ensure_dirs

IRI = "https://iridl.ldeo.columbia.edu/SOURCES/.NOAA/.NCEP-NCAR/.CDAS-1/.MONTHLY"
T = f"T/(Jan%20{FIRST_YEAR})/(Dec%202026)/RANGE"


def fetch(path):
    url = f"{IRI}/{path}/{T}/data.tsv"
    r = requests.get(url, timeout=180)
    r.raise_for_status()
    vals = [float(x) for x in r.text.split()]
    if len(vals) < 100:
        raise ValueError(f"Too few values from {url}: {r.text[:200]}")
    idx = pd.date_range(f"{FIRST_YEAR}-01-01", periods=len(vals), freq="MS")
    return pd.Series(vals, index=idx)


def main():
    ensure_dirs()
    out = {}
    for name, (lat, lon) in NAO_POINTS.items():
        out[f"slp_{name}_hpa"] = fetch(f".Intrinsic/.MSL/.pressure/X/{lon % 360:.2f}/VALUE/Y/{lat:.2f}/VALUE") / 100
    box = "X/284/290/RANGE/Y/38/42/RANGE/%5BX/Y%5Daverage"
    u = fetch(f".Diagnostic/.above_ground/.u/{box}")
    v = fetch(f".Diagnostic/.above_ground/.v/{box}")
    out["wind_ne_ms"] = WIND_FROM_NE[0] * u + WIND_FROM_NE[1] * v
    df = pd.DataFrame(out)
    train = df.loc[TRAIN[0]:TRAIN[1]]
    z = {}
    for name in NAO_POINTS:
        col = f"slp_{name}_hpa"
        clim = train[col].groupby(train.index.month).agg(["mean", "std"])
        z[name] = (df[col] - clim["mean"].reindex(df.index.month).to_numpy()) / clim["std"].reindex(df.index.month).to_numpy()
    nao = z["azores"] - z["iceland"]
    df["nao_ncep"] = nao / nao.loc[TRAIN[0]:TRAIN[1]].std()
    df.to_csv(PROCESSED / "public_predictors.csv", index_label="date")
    print(f"public predictors (NCEP/NCAR via IRI): {len(df)} months, {df.index.min():%Y-%m}..{df.index.max():%Y-%m}; "
          f"SLP Iceland mean {df['slp_iceland_hpa'].mean():.1f} hPa, Azores {df['slp_azores_hpa'].mean():.1f} hPa, "
          f"wind_ne mean {df['wind_ne_ms'].mean():+.2f} m/s", flush=True)


if __name__ == "__main__":
    main()
