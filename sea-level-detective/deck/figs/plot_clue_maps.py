"""Publication-style maps for the deck (Zyskin: real figures, not website screenshots). Runs on the DGX after fields.py.

Inputs next to this script: fields.npz (fields.py), globe.json / globe_west.json (Nino3.4 box, gauge positions),
land.json (Natural Earth outlines). Outputs (300 dpi):
  fig_ssh_2015.png  NASA sea-surface height anomaly, November 2015 (strong El Nino), with the regions we use
  fig_east.png      June sea height vs New York's next-winter storm-surge days (Spearman r, every ocean cell)
  fig_west.png      the same for Los Angeles' next-winter high-water days
"""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from matplotlib.collections import PatchCollection

HERE = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 10, "axes.linewidth": 0.8,
                     "axes.edgecolor": "#333333", "xtick.color": "#333333", "ytick.color": "#333333"})

F = np.load(HERE / "fields.npz")
LAT, LON = F["lat"], F["lon"]
gE = json.loads((HERE / "globe.json").read_text(encoding="utf-8"))
gW = json.loads((HERE / "globe_west.json").read_text(encoding="utf-8"))
LAND = json.loads((HERE / "land.json").read_text(encoding="utf-8"))
BOX = gE["nino34_box"]
NY, LA = gE["battery"], gW["battery"]


def draw_land(ax):
    polys = []
    for f in LAND["features"]:
        g = f["geometry"]
        for poly in ([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]):
            polys.append(Polygon(np.array(poly[0]), closed=True))
    # one fill colour and no outlines: coasts read against the ocean, country borders disappear
    ax.add_collection(PatchCollection(polys, facecolor="#dedad2", edgecolor="#dedad2", linewidth=0.3, zorder=3))


def regions(ax, targets, nino=True):
    if nino:
        s, n, w, e = BOX
        ax.add_patch(Rectangle((w, s), e - w, n - s, fill=False, ec="black", lw=1.3, ls=(0, (4, 2)), zorder=4))
        ax.text(w + 1, n + 2.2, "Niño-3.4", fontsize=9, fontweight="bold", zorder=5)
    for name, (la, lo), dx, dy in targets:
        ax.plot(lo, la, marker="*", ms=13, mfc="#f2c14e", mec="black", mew=0.8, zorder=6)
        ax.text(lo + dx, la + dy, name, fontsize=9, fontweight="bold", zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))


def frame(ax, extent, title):
    ax.set_xlim(extent[0], extent[1]); ax.set_ylim(extent[2], extent[3]); ax.set_aspect("equal")
    ax.set_xlabel("Longitude [deg]"); ax.set_ylabel("Latitude [deg]")
    ax.axhline(0, color="#555555", lw=0.5, ls=":", zorder=2)
    ax.set_title(title, fontsize=10.5)


# 1. a real El Nino in NASA altimetry
z = F["ssh_2015_11"]
fig, ax = plt.subplots(figsize=(12, 5.2))
pm = ax.pcolormesh(LON, LAT, z, cmap="RdBu_r", vmin=-0.3, vmax=0.3, shading="nearest", zorder=1)
draw_land(ax)
regions(ax, [("New York", NY, 3, 3), ("Los Angeles", LA, -26, 4)])
frame(ax, (-180, 180, -60, 70), "NASA sea-surface height anomaly, November 2015 (strong El Niño)\n"
      "NASA JPL MEaSUREs gridded altimetry · the regions this project links")
cb = plt.colorbar(pm, ax=ax, fraction=0.025, pad=0.015); cb.set_label("Sea-surface height anomaly [m]", fontsize=9)
fig.tight_layout(); fig.savefig(HERE / "fig_ssh_2015.png", dpi=300); plt.close(fig)

# 2-3. the clue maps, both coasts on the same Pacific-Americas window
ext = (-185, -20, -30, 62)
for key, tgt, name, lab, days, out in [("ny", NY, "New York", "East Coast · New York", "storm-surge days", "fig_east.png"),
                                       ("la", LA, "Los Angeles", "West Coast · Los Angeles", "high-water days", "fig_west.png")]:
    r, r05, n = F[f"r_{key}"], float(F[f"r05_{key}"]), int(F[f"n_{key}"])
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    pm = ax.pcolormesh(LON, LAT, r, cmap="RdBu_r", vmin=-0.7, vmax=0.7, shading="nearest", zorder=1)
    LO, LAg = np.meshgrid(LON, LAT)
    ax.contour(LO, LAg, np.nan_to_num(np.abs(r)), levels=[r05], colors="#222222", linewidths=0.7, linestyles="--", zorder=2)
    draw_land(ax)
    regions(ax, [(name, tgt, 3, 2.5)])
    frame(ax, ext, f"{lab}: June sea height vs next winter's {days}\nNASA MEaSUREs, {n} winters 1993–2018 · dashed: p < 0.05")
    cb = plt.colorbar(pm, ax=ax, fraction=0.03, pad=0.04); cb.set_label("Spearman r (detrended)", fontsize=9)
    fig.tight_layout(); fig.savefig(HERE / out, dpi=300); plt.close(fig)
print("done")
