"""Equatorial Hovmoller for the website's "How El Nino moves the ocean" panel, in the site's own look: serif type,
the globe's ink scale (iron-gall blue - parchment - red chalk), transparent background. Runs on the DGX.

Data: NASA JPL MEaSUREs gridded sea-surface height anomaly as monthly 2-degree grids (ntr/explore_ssh_gibs.py,
data_processed/ssh_gibs_monthly.npz), averaged over the cells between 2S and 2N, 170W-100W, January 2015 - July 2016, minus each month's
global-mean sea height (cos-latitude weighted) so sea-level rise does not mask the El Nino signal.
For display the monthly field is interpolated in time (cubic) and smoothed lightly along longitude.
Usage: python plot_hov.py <ssh_gibs_monthly.npz> <out dir>
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d

npz, OUT = Path(sys.argv[1]), Path(sys.argv[2])
g = np.load(npz)
ssh, LAT, LON, months = g["ssh_m"].astype(float), g["lat"], g["lon"], [str(m) for m in g["months"]]
sel = [i for i, m in enumerate(months) if "2015-01" <= m <= "2016-07"]
rows = np.abs(LAT) <= 2.0
cols = (LON >= -171) & (LON <= -99)
# remove each month's global-mean sea height (cos-latitude weighted) so the El Nino pattern is not hidden by sea-level rise
wts = np.cos(np.deg2rad(LAT))[:, None] * np.ones((1, LON.size))
with np.errstate(all="ignore"):
    gmean = np.array([np.nansum(np.where(np.isfinite(ssh[i]), ssh[i] * wts, 0)) / np.nansum(np.where(np.isfinite(ssh[i]), wts, 0)) for i in sel])
    band = np.nanmean(ssh[sel][:, rows][:, :, cols], axis=1) - gmean[:, None]   # months x lon
lon = LON[cols]
t = np.arange(len(sel), dtype=float)                                  # month index, 0 = Jan 2015
tf = np.linspace(0, t[-1], 240)
fine = interp1d(t, band, kind="cubic", axis=0)(tf)
fine = gaussian_filter1d(fine, 0.8, axis=1, mode="nearest")

INK = "#3b2614"
cmap = LinearSegmentedColormap.from_list("ink", ["#26364d", "#3a4e68", "#9aa6b2", "#ede6d6", "#c49a8a", "#8b3a2b", "#5e2318"])
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 12, "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK, "axes.edgecolor": INK, "axes.linewidth": 0.8})
fig, ax = plt.subplots(figsize=(6.0, 5.6))
pm = ax.pcolormesh(lon, tf, fine, cmap=cmap, vmin=-0.25, vmax=0.25, shading="gouraud", rasterized=True)
ticks = [0, 3, 6, 9, 12, 15, 18]
names = ["Jan 2015", "Apr", "Jul", "Oct", "Jan 2016", "Apr", "Jul"]
ax.set_yticks(ticks); ax.set_yticklabels(names)
ax.set_xticks([-160, -140, -120, -100]); ax.set_xticklabels(["160°W", "140°W", "120°W", "100°W"])
ax.set_xlabel("Longitude along the equator (2°S–2°N)")
ax.set_title("Sea height along the equator, 2015–16", fontsize=13, pad=10)
for sp in ax.spines.values():
    sp.set_color(INK)
cb = plt.colorbar(pm, ax=ax, fraction=0.05, pad=0.03, extend="both")
cb.set_label("sea height vs global mean [m]"); cb.outline.set_edgecolor(INK)
fig.tight_layout()
fig.savefig(OUT / "fig_hovmoller.png", dpi=220, transparent=True)
print("hovmoller", band.shape, np.nanmin(band).round(3), np.nanmax(band).round(3), "global mean removed:", gmean.min().round(3), gmean.max().round(3))
