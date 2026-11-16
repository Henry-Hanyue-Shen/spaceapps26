"""Pacific seesaw: per-cell ENSO/ONI regression maps and fixed-lag sensitivity."""
import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats as sp
from config import ENSO_LAG, PROCESSED, FIGURES
from common import read_monthly, metadata, save_json
from stats import deseasonalize, regression


def map_regression(grid, index, lag):
    """Deseasonalized SSHA on an index, per cell; slope in mm/index unit.

    Confidence intervals use residual AR(1) effective sample size. These are
    pointwise descriptive intervals, without spatial multiple-testing control.
    """
    shifted = index.copy()
    shifted.index = shifted.index+pd.DateOffset(months=lag)
    aligned = shifted.reindex(pd.DatetimeIndex(grid.time.values))
    usable = aligned.notna().to_numpy()
    dates = pd.DatetimeIndex(grid.time.values)[usable]
    y = grid.values[usable].astype(float)
    x = aligned.to_numpy()[usable, None, None]
    valid = np.isfinite(y)
    n = valid.sum(axis=0)
    safe_n = np.maximum(n, 1)
    y0 = np.where(valid, y, 0)
    xm = np.where(valid, x, 0).sum(axis=0)/safe_n
    ym = y0.sum(axis=0)/safe_n
    dx, dy = np.where(valid, x-xm, 0), np.where(valid, y-ym, 0)
    ssx, ssy = (dx*dx).sum(axis=0), (dy*dy).sum(axis=0)
    covariance = (dx*dy).sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        beta = covariance/ssx
        residual = np.where(valid, y-ym-beta*(x-xm), np.nan)
        consecutive = np.diff(dates.year*12+dates.month) == 1
        pairs = valid[:-1] & valid[1:] & consecutive[:, None, None]
        counts = np.maximum(pairs.sum(axis=0), 1)
        a, b = np.where(pairs, residual[:-1], 0), np.where(pairs, residual[1:], 0)
        ac, bc = a.sum(axis=0)/counts, b.sum(axis=0)/counts
        a, b = np.where(pairs, a-ac, 0), np.where(pairs, b-bc, 0)
        rho = (a*b).sum(axis=0)/np.sqrt((a*a).sum(axis=0)*(b*b).sum(axis=0))
        rho = np.clip(np.nan_to_num(rho, nan=0), 0, .99)
        effective = np.minimum(n, np.maximum(3, n*(1-rho)/(1+rho)))
        se = np.sqrt(np.nansum(residual**2, axis=0)/np.maximum(n-2, 1)/ssx*n/effective)
        radius = sp.t.ppf(.975, np.maximum(effective-2, 1))*se
        r2 = covariance**2/(ssx*ssy)
    good = (n >= 24) & (ssx > 0)
    arrays = {"coefficient": beta, "ci95_low": beta-radius, "ci95_high": beta+radius,
              "r2": r2, "n": n.astype(float), "n_eff": effective}
    output = xr.Dataset({name: (("latitude", "longitude"), np.where(good, values, np.nan))
                         for name, values in arrays.items()},
                        coords={"latitude": grid.latitude, "longitude": grid.longitude})
    output.attrs.update(lag_months=lag, method="Deseasonalized SSHA on index; AR(1) effective-sample-size pointwise CI",
                        window_start=str(dates.min().date()), window_end=str(dates.max().date()))
    return output


def box_regression(series, index, lag):
    shifted = index.copy()
    shifted.index = shifted.index+pd.DateOffset(months=lag)
    pair = pd.concat([deseasonalize(series).rename("level"), shifted.rename("index")], axis=1).dropna()
    fit = regression(pair.level, np.column_stack((np.ones(len(pair)), pair["index"])), pair.index)
    return {**metadata(pair.level), "lag_months": lag,
            "method": "Deseasonalized SSHA on index; AR(1) effective-sample-size CI",
            "coefficient": fit["beta"][1], "ci95": fit["ci"][1].tolist(),
            "r2": fit["r2"], "rho": fit["rho"], "n_eff": fit["n_eff"]}


def el_nino_periods(oni):
    """Consecutive >=0.5 C central months lasting at least five ONI seasons."""
    oni = oni.asfreq("MS")
    warm = oni >= .5
    periods = []
    for _, values in warm.groupby(warm.ne(warm.shift()).cumsum()):
        if values.iloc[0] and len(values) >= 5:
            periods.append((values.index[0], values.index[-1]+pd.offsets.MonthBegin(1)))
    return periods


def main():
    import matplotlib.pyplot as plt
    boxes, indicators, oni = read_monthly("box_monthly.csv"), read_monthly("indicators.csv"), read_monthly("oni.csv").oni_c
    with xr.open_dataset(PROCESSED / "grid_1deg_monthly.nc") as source:
        original = source.ssha.load()
    grid = original.groupby("time.month")-original.groupby("time.month").mean("time")
    result = {"experiment": "E2", "fixed_lag_months": ENSO_LAG, "indices": {},
              "notes": ["Lag was fixed before results. Positive lag means index leads sea level.",
                        "Per-cell slope/CI/n/R-squared arrays are stored in data_processed/e2_*_lag_*.nc.",
                        "Pointwise CIs are descriptive, with no spatial multiple-testing adjustment.",
                        "El Nino shading uses NOAA ONI >=0.5 C for at least five consecutive three-month seasons."]}
    for name, index in {"nasa_enso": indicators.enso, "noaa_oni": oni}.items():
        sensitivity = []
        for lag in sorted(set(range(7)) | {ENSO_LAG}):
            print(f"E2: {name}, lag {lag} months", flush=True)
            fitted = map_regression(grid, index, lag)
            units = "mm per degree C" if name == "noaa_oni" else "mm per native NASA ENSO unit"
            for variable in ("coefficient", "ci95_low", "ci95_high"):
                fitted[variable].attrs["units"] = units
            fitted.to_netcdf(PROCESSED / f"e2_{name}_lag_{lag}.nc")
            sensitivity.append({"lag_months": lag, "units": units,
                                "valid_grid_cells": int(fitted.coefficient.count()),
                                "west_pacific": box_regression(boxes.west_pacific, index, lag),
                                "east_pacific": box_regression(boxes.east_pacific, index, lag)})
            if lag == ENSO_LAG:
                values = fitted.coefficient.values
                if not np.isfinite(values).any():
                    raise ValueError(f"No valid cell regressions for {name}")
                limit = float(np.nanpercentile(np.abs(values), 98)) or 1.0
                fig, ax = plt.subplots(figsize=(11, 4.5))
                artist = ax.pcolormesh(fitted.longitude, fitted.latitude, values, cmap="RdBu_r",
                                       vmin=-limit, vmax=limit, shading="auto")
                ax.set(xlabel="Longitude (degrees E)", ylabel="Latitude (degrees N)",
                       title=f"SSHA regression on {name}, lag {lag} months")
                fig.colorbar(artist, ax=ax, label=units, extend="both")
                fig.tight_layout()
                fig.savefig(FIGURES / f"e2_{name}_map.png", dpi=160)
                plt.close(fig)
        fig, axes = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
        for ax, box in zip(axes, ("west_pacific", "east_pacific")):
            series = deseasonalize(boxes[box])
            ax.plot(series.index, series, label=box)
            for start, end in el_nino_periods(oni):
                ax.axvspan(start, end, alpha=.15, color="coral")
            ax.set(ylabel="SSHA anomaly (mm)", xlim=(series.index.min(), series.index.max()))
            ax.legend(loc="upper left")
            twin = ax.twinx()
            twin.plot(index.index, index, color="grey", alpha=.4)
            twin.set_ylabel(name)
        fig.suptitle("Pacific boxes; NOAA-defined El Nino periods shaded")
        fig.tight_layout()
        fig.savefig(FIGURES / f"e2_{name}_boxes.png", dpi=160)
        plt.close(fig)
        result["indices"][name] = {"sensitivity": sensitivity}
    return save_json("e2.json", result)


if __name__ == "__main__":
    main()
