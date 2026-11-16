"""Comparison figures for the deck, East (New York) vs West (Los Angeles), sized for their slide slots (figure inches
= slot px / 100, 250 dpi, so 13 pt text reads at about 18 px on a 1920-px slide). Runs on the DGX after fields.py.

fig_both_map.png   one map for both coasts: colour = mean of the two June clue fields (Spearman r between June NASA
                   MEaSUREs sea height and each coast's next-winter high-water days, 1993-2018), Gaussian-smoothed for
                   display (sigma = one 2-degree cell); outlines = p < 0.05 for each coast (smoothed field)
fig_lead.png       how early El Nino warns each coast: rate ratio per SD by the month Nino3.4 is read, 95% bands
fig_poisson.png    the historical winters and the quasi-Poisson fit, per coast: days ~ trend + June Nino3.4
fig_cover.png      NASA sea-surface height anomaly, November 2015 (strong El Nino), with the regions we use
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
from matplotlib.lines import Line2D
from scipy.ndimage import gaussian_filter, zoom
import statsmodels.api as sm

HERE = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
RED, BLUE, INK = "#8b3a2b", "#3a4e68", "#27211b"
DPI = 250
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 13, "axes.linewidth": 0.9, "axes.edgecolor": "#333333",
                     "xtick.color": "#333333", "ytick.color": "#333333", "axes.spines.top": False, "axes.spines.right": False})
F = np.load(HERE / "fields.npz")
LAT, LON = F["lat"], F["lon"]
gE = json.loads((HERE / "globe.json").read_text(encoding="utf-8"))
gW = json.loads((HERE / "globe_west.json").read_text(encoding="utf-8"))
LAND = json.loads((HERE / "land.json").read_text(encoding="utf-8"))
S, N, Wb, Eb = gE["nino34_box"]


def smooth(z, s=1.0):
    ok = np.isfinite(z)
    num = gaussian_filter(np.where(ok, z, 0.0), s, mode=("nearest", "wrap"))
    den = gaussian_filter(ok.astype(float), s, mode=("nearest", "wrap"))
    out = num / np.maximum(den, 1e-9)
    out[~ok] = np.nan
    return out


def draw_land(ax):
    polys = []
    for f in LAND["features"]:
        g = f["geometry"]
        for poly in ([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]):
            polys.append(Polygon(np.array(poly[0]), closed=True))
    ax.add_collection(PatchCollection(polys, facecolor="#dedad2", edgecolor="#dedad2", linewidth=0.3, zorder=3))


def regions(ax, targets, fs=12):
    ax.add_patch(Rectangle((Wb, S), Eb - Wb, N - S, fill=False, ec="black", lw=1.3, ls=(0, (4, 2)), zorder=4))
    ax.text(Wb + 1, N + 2.5, "Niño-3.4", fontsize=fs, fontweight="bold", zorder=5)
    for name, (la, lo), dx, dy in targets:
        ax.plot(lo, la, marker="*", ms=14, mfc="#f2c14e", mec="black", mew=0.8, zorder=6)
        ax.text(lo + dx, la + dy, name, fontsize=fs, fontweight="bold", zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", fc="#f1ece1", ec="none", alpha=0.85))


def boxed(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(True)


# ---------------------------------------------------------------- 1. one map, both coasts
rE, rW = smooth(F["r_ny"]), smooth(F["r_la"])
with np.errstate(all="ignore"):
    both = np.nanmean(np.stack([rE, rW]), 0)
k = 4   # display upsampling (bilinear) of the smoothed field
up = zoom(np.nan_to_num(both), k, order=1)
mask = zoom(np.isfinite(both).astype(float), k, order=1) < 0.5
dl = abs(LON[1] - LON[0]) / 2
flip = LAT[0] > LAT[-1]
if flip:
    up, mask = up[::-1], mask[::-1]
ext = (LON.min() - dl, LON.max() + dl, LAT.min() - dl, LAT.max() + dl)
fig, ax = plt.subplots(figsize=(7.6, 4.45))
im = ax.imshow(np.ma.array(up, mask=mask), origin="lower", extent=ext, cmap="RdBu_r", vmin=-0.6, vmax=0.6,
               interpolation="bilinear", zorder=1, aspect="equal")
LO, LA = np.meshgrid(LON, LAT)
ax.contour(LO, LA, np.nan_to_num(rE), levels=[float(F["r05_ny"])], colors=BLUE, linewidths=1.8, zorder=2)
ax.contour(LO, LA, np.nan_to_num(rW), levels=[float(F["r05_la"])], colors=RED, linewidths=1.8, linestyles="--", zorder=2)
draw_land(ax)
regions(ax, [("New York", gE["battery"], 3, 3), ("Los Angeles", gW["battery"], 3, 3)])
ax.set_xlim(-185, -20); ax.set_ylim(-30, 62); boxed(ax)
ax.set_xticks([-180, -140, -100, -60, -20])
ax.set_xlabel("Longitude [deg]"); ax.set_ylabel("Latitude [deg]")
ax.axhline(0, color="#555555", lw=0.5, ls=":", zorder=2)
ax.set_title("June sea height vs next winter, both coasts", fontsize=14)
ax.legend(handles=[Line2D([], [], color=BLUE, lw=1.8, label="New York, p < 0.05"),
                   Line2D([], [], color=RED, lw=1.8, ls="--", label="Los Angeles, p < 0.05")],
          loc="lower left", fontsize=11, frameon=True, framealpha=0.85, facecolor="#f1ece1", edgecolor="none")
cb = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.03); cb.set_label("Spearman r, mean of both coasts", fontsize=11)
fig.tight_layout(); fig.savefig(HERE / "fig_both_map.png", dpi=DPI, transparent=True); plt.close(fig)

# ---------------------------------------------------------------- 2. lead time, both coasts
MON = "J F M A M J J A S O N D".split()
fig, ax = plt.subplots(figsize=(6.3, 4.45))
ax.axvspan(9.5, 12.5, color="#d8cfbf", alpha=0.35, lw=0)
ax.text(11, 4.9, "season\nbegins", ha="center", va="top", fontsize=11, color="#6b5f51")
for G, name, col in [(gE, "New York", BLUE), (gW, "Los Angeles", RED)]:
    L = sorted([d for d in G["lead_curve"] if d["index"] == "nino34_giss"], key=lambda d: d["month"])
    m = np.array([d["month"] for d in L]); rr = np.array([d["rr"] for d in L])
    lo, hi = np.array([d["ci"][0] for d in L]), np.array([d["ci"][1] for d in L])
    ax.fill_between(m, lo, hi, color=col, alpha=0.14, lw=0)
    ax.plot(m, rr, color=col, lw=2.4, marker="o", ms=5, label=name)
    j = int(np.argmax(rr))
    ax.annotate(f"×{rr[j]:.2f}", (m[j], rr[j]), textcoords="offset points", xytext=(0, 10), ha="center", color=col, fontsize=13, fontweight="bold")
ax.axhline(1, color="#666666", lw=0.8, ls=":")
ax.set_xticks(range(1, 13)); ax.set_xticklabels(MON); ax.set_xlim(0.6, 12.4); ax.set_ylim(0.6, 6.2)
ax.set_xlabel("Month Niño-3.4 is read"); ax.set_ylabel("× days per SD of El Niño")
ax.set_title("How early El Niño warns each coast", fontsize=14)
ax.legend(loc="upper left", fontsize=11, frameon=False)
fig.tight_layout(); fig.savefig(HERE / "fig_lead.png", dpi=DPI, transparent=True); plt.close(fig)

# ---------------------------------------------------------------- 3. historical winters + quasi-Poisson fit
fig, axs = plt.subplots(1, 2, figsize=(8.1, 4.0), sharex=True)
for ax, G, name, days, col in [(axs[0], gE, "New York", "storm-surge days", BLUE), (axs[1], gW, "Los Angeles", "high-water days", RED)]:
    Wn = [w for w in G["winters"] if w.get("nino_june_sd") is not None and w.get("observed") is not None]
    yr = np.array([w["year"] for w in Wn], float); x = np.array([w["nino_june_sd"] for w in Wn]); y = np.array([w["observed"] for w in Wn])
    X = sm.add_constant(np.column_stack([yr - yr.mean(), x]))
    fit = sm.GLM(y, X, family=sm.families.Poisson()).fit(scale="X2")
    xs = np.linspace(x.min() - 0.2, x.max() + 0.2, 200)
    Xs = sm.add_constant(np.column_stack([np.zeros_like(xs), xs]), has_constant="add")
    eta = Xs @ fit.params; se = np.sqrt(np.einsum("ij,jk,ik->i", Xs, fit.cov_params(), Xs))
    ax.fill_between(xs, np.exp(eta - 1.96 * se), np.exp(eta + 1.96 * se), color=col, alpha=0.15, lw=0)
    ax.plot(xs, np.exp(eta), color=col, lw=2.4, label="quasi-Poisson fit")
    strong = x >= 1.2
    ax.scatter(x[~strong], y[~strong], s=24, color="white", edgecolor=INK, lw=0.9, zorder=3, label="a past winter")
    ax.scatter(x[strong], y[strong], s=34, color=col, edgecolor=INK, lw=0.9, zorder=4, label="strong El Niño")
    for xi, yi, ri in zip(x[strong], y[strong], yr[strong]):
        ax.annotate(f"{int(ri)}–{str(int(ri) + 1)[2:]}", (xi, yi), textcoords="offset points", xytext=(6, -15), ha="left", fontsize=10)
    rr = np.exp(fit.params[2])
    ax.text(0.04, 0.96, f"×{rr:.2f} per SD\n{len(y)} winters", transform=ax.transAxes, va="top", fontsize=12, color=col, fontweight="bold")
    ax.set_title(name, fontsize=13)
    ax.set_xlabel("June Niño-3.4 (SD)"); ax.set_ylabel(f"winter {days}")
    ax.set_ylim(bottom=0)
axs[1].legend(loc="upper left", bbox_to_anchor=(0.0, 0.80), fontsize=10, frameon=False, handlelength=1.4)
fig.tight_layout(); fig.savefig(HERE / "fig_poisson.png", dpi=DPI, transparent=True); plt.close(fig)

# ---------------------------------------------------------------- 3b. the same, stacked for a narrow slide column
fig, axs = plt.subplots(2, 1, figsize=(5.2, 4.9), sharex=True)
for ax, G, name, days, col in [(axs[0], gE, "New York", "storm-surge days", BLUE), (axs[1], gW, "Los Angeles", "high-water days", RED)]:
    Wn = [w for w in G["winters"] if w.get("nino_june_sd") is not None and w.get("observed") is not None]
    yr = np.array([w["year"] for w in Wn], float); x = np.array([w["nino_june_sd"] for w in Wn]); y = np.array([w["observed"] for w in Wn])
    X = sm.add_constant(np.column_stack([yr - yr.mean(), x]))
    fit = sm.GLM(y, X, family=sm.families.Poisson()).fit(scale="X2")
    xs = np.linspace(x.min() - 0.2, x.max() + 0.2, 200)
    Xs = sm.add_constant(np.column_stack([np.zeros_like(xs), xs]), has_constant="add")
    eta = Xs @ fit.params; se = np.sqrt(np.einsum("ij,jk,ik->i", Xs, fit.cov_params(), Xs))
    ax.fill_between(xs, np.exp(eta - 1.96 * se), np.exp(eta + 1.96 * se), color=col, alpha=0.15, lw=0)
    ax.plot(xs, np.exp(eta), color=col, lw=2.4)
    strong = x >= 1.2
    ax.scatter(x[~strong], y[~strong], s=20, color="white", edgecolor=INK, lw=0.8, zorder=3)
    ax.scatter(x[strong], y[strong], s=30, color=col, edgecolor=INK, lw=0.8, zorder=4)
    ax.text(0.03, 0.94, f"{name}  ×{np.exp(fit.params[2]):.2f} per SD", transform=ax.transAxes, va="top", fontsize=12, color=col, fontweight="bold")
    ax.set_ylabel("days"); ax.set_ylim(bottom=0)
axs[1].set_xlabel("June Niño-3.4 (SD)")
fig.tight_layout(); fig.savefig(HERE / "fig_poisson_col.png", dpi=DPI, transparent=True); plt.close(fig)

# ---------------------------------------------------------------- 4. cover: a real El Nino, slide-sized
fig, ax = plt.subplots(figsize=(9.0, 3.9))
pm = ax.pcolormesh(LON, LAT, F["ssh_2015_11"], cmap="RdBu_r", vmin=-0.3, vmax=0.3, shading="nearest", zorder=1)
draw_land(ax)
regions(ax, [("New York", gE["battery"], 3, 3), ("Los Angeles", gW["battery"], -36, 5)], fs=11)
ax.set_xlim(-180, 180); ax.set_ylim(-60, 70); ax.set_aspect("equal"); boxed(ax)
ax.set_xlabel("Longitude [deg]"); ax.set_ylabel("Latitude [deg]")
ax.set_title("NASA sea-surface height anomaly, November 2015 (strong El Niño)", fontsize=13)
cb = plt.colorbar(pm, ax=ax, fraction=0.025, pad=0.02); cb.set_label("anomaly [m]", fontsize=11)
fig.tight_layout(); fig.savefig(HERE / "fig_cover.png", dpi=DPI, transparent=True); plt.close(fig)
print("done")
