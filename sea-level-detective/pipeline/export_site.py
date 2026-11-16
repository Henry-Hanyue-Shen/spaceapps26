"""Export standard-format series and results to ../site/data/ for the static website.

Writes:
  series.json          regions (monthly sea level, mm, 1993-2012 = 0), ENSO indices, E1 table, metadata
  reference_fits.json  Python fits used by site/tests to check that the browser statistics match stats.py
"""
import json
import numpy as np
import pandas as pd
from config import ROOT, PROCESSED, RESULTS
from common import clean_json
from stats import fit_with_index, regression, years

SITE_DATA = ROOT.parent / "site" / "data"
LABELS = {
    "gauge_the_battery": ("The Battery, New York (tide gauge)", "NOAA CO-OPS 8518750", "gauge"),
    "gauge_la_jolla": ("La Jolla, California (tide gauge)", "NOAA CO-OPS 9410230", "gauge"),
    "gauge_san_francisco": ("San Francisco, California (tide gauge)", "NOAA CO-OPS 9414290", "gauge"),
    "global": ("Global ocean (NASA satellites)", "NASA-SSH", "nasa"),
    "west_pacific": ("Western equatorial Pacific (NASA satellites)", "NASA-SSH", "nasa"),
    "east_pacific": ("Eastern equatorial Pacific (NASA satellites)", "NASA-SSH", "nasa"),
    "california_shelf": ("California coast (NASA satellites)", "NASA-SSH", "nasa"),
    "ny_bight": ("New York Bight (NASA satellites)", "NASA-SSH", "nasa"),
    "global_nasa_gmsl_indicator": ("Global mean sea level (NASA indicator)", "NASA_SSH_GMSL_INDICATOR", "nasa"),
}
INDEX_LABELS = {"noaa_oni": "NOAA Oceanic Niño Index (°C)", "nasa_enso": "NASA-SSH ENSO indicator"}


def series_payload(frame):
    s = frame.set_index("date")["value"]
    return {"dates": list(s.index), "values": [None if pd.isna(v) else round(float(v), 2) for v in s.to_numpy()]}


def main():
    SITE_DATA.mkdir(parents=True, exist_ok=True)
    monthly = pd.read_csv(PROCESSED / "series_monthly.csv")
    level = monthly[monthly.variable == "sea_level"]
    regions = {}
    for region, frame in level.groupby("region", sort=False):
        label, source, kind = LABELS.get(region, (region, "", "other"))
        regions[region] = {"label": label, "source": source, "kind": kind, **series_payload(frame)}
    indices = {}
    idx = pd.read_csv(PROCESSED / "indices_monthly.csv")
    for col, label in INDEX_LABELS.items():
        if col in idx:
            s = idx.set_index("month")[col]
            indices[col] = {"label": label, "dates": list(s.index),
                            "values": [None if pd.isna(v) else round(float(v), 4) for v in s.to_numpy()]}
    e1 = json.loads((RESULTS / "e1.json").read_text(encoding="utf-8"))
    payload = {"generated": pd.Timestamp.now(tz="UTC").isoformat(timespec="minutes"),
               "units": "mm; each series has its 1993-2012 mean = 0", "regions": regions, "indices": indices,
               "e1": {"noise": e1["noise"], "settings": e1["settings"], "weatherhead": e1["weatherhead"]}}
    (SITE_DATA / "series.json").write_text(json.dumps(clean_json(payload), separators=(",", ":")), encoding="utf-8")

    # NY Harbor NTR study (computed on the DGX by ../ntr/; results copied into ../ntr/results/)
    ntr_dir = ROOT.parent / "ntr" / "results"
    if (ntr_dir / "ntr.json").exists() and (ntr_dir / "ntr_seasons.csv").exists():
        ntr = json.loads((ntr_dir / "ntr.json").read_text(encoding="utf-8"))
        seasons = pd.read_csv(ntr_dir / "ntr_seasons.csv")
        seasons = seasons[seasons["start_year"] <= 2025]
        site_ntr = {"sources": ntr["sources"], "threshold_m": ntr["surge_threshold_m"],
                    "seasons": [{"start_year": int(r.start_year), "surge_days": None if pd.isna(r.surge_days) else float(r.surge_days),
                                 "enso_aug_sd": None if pd.isna(r.enso_aug) else round(float(r.enso_aug), 2), "months": int(r.months)}
                                for r in seasons.itertuples()],
                    "season_outlook": ntr.get("season_outlook"), "lag_analysis": {
                        k: [{"lag": l["lag"], "r": l["r"], "significant": l["significant"]} for l in v["all_months"]["lags"]]
                        for k, v in ntr["lag_analysis"].items()},
                    "models": {k: {"skill": v["skill_vs_climatology"], "rmse_mm": v["rmse_mm"]} for k, v in ntr["models"].items()}}
        (SITE_DATA / "ntr.json").write_text(json.dumps(clean_json(site_ntr), indent=1), encoding="utf-8")
        print(f"export_site: NTR study exported ({len(site_ntr['seasons'])} seasons)")

    # Globe: teleconnection maps, predictor locations, ENSO lead-time curve (computed on the DGX by ../ntr/explore_*.py)
    if (ntr_dir / "explore_maps.json").exists() and (ntr_dir / "explore.json").exists():
        maps = json.loads((ntr_dir / "explore_maps.json").read_text(encoding="utf-8"))
        ex = json.loads((ntr_dir / "explore.json").read_text(encoding="utf-8"))
        space = json.loads((ntr_dir / "explore_space_time.json").read_text(encoding="utf-8"))
        globe = {"n_seasons": maps["n_seasons"], "years": maps["years"], "r_p05": maps["r_p05"], "battery": maps["battery"],
                 "nino34_box": maps["nino34_box"], "note": maps["note"],
                 # every cell with |r| >= 0.2 as [lat, lon, r]; the site draws bars only at or above r_p05 and uses the
                 # rest when the visitor clicks a place
                 "maps": {m: [[c[0], c[1], round(c[2], 2)] for c in cells] for m, cells in maps["maps"].items()},
                 "r_min_kept": 0.2,
                 "predictors": space,
                 "lead_curve": [{"index": r["index"], "month": r["month"], "rr": r["rr_all"], "ci": r["rr_all_ci"], "p": r["p_all"],
                                 "loo": r["loo_skill"]} for r in ex["enso_lead_curve"]],
                 "outlook": ex.get("outlook_2026", []),
                 "screen": {k: {"tests": v["tests"], "discoveries": v["discoveries"], "confirmed": len(v["confirmed"])} for k, v in ex["monthly"].items()},
                 "n_predictors": ex["n_predictors"], "train": ex["train"], "test": ex["test"]}
        # "Test a winter": observed surge days vs predictions made without that winter (leave-one-out)
        sp_path = ntr_dir / "season_predictions.csv"
        if sp_path.exists():
            sp = pd.read_csv(sp_path).dropna(subset=["observed_surge_days", "pred_nasa_nino34_june_leave_one_out", "pred_trend_only_leave_one_out"])
            globe["winters"] = [{"year": int(r.season_start_year), "observed": float(r.observed_surge_days),
                                 "model": round(float(r.pred_nasa_nino34_june_leave_one_out), 1),
                                 "trend": round(float(r.pred_trend_only_leave_one_out), 1),
                                 "nino_june_sd": round(float(r.nasa_nino34_june_sd), 2)} for r in sp.itertuples()]
        ssh_path = ntr_dir / "explore_maps_ssh.json"   # altimetry clue map (explore_ssh_gibs.py), switchable on the globe
        if ssh_path.exists():
            (SITE_DATA / "clue_map_ssh.json").write_text(ssh_path.read_text(encoding="utf-8"), encoding="utf-8")
        sw_path = ntr_dir / "signal_winters.json"   # every signal x read-month x winter (explore_signal_winters.py)
        if sw_path.exists():
            (SITE_DATA / "signal_winters.json").write_text(sw_path.read_text(encoding="utf-8"), encoding="utf-8")
        sd_path = ntr_dir / "surge_dates.json"
        if sd_path.exists():
            globe["surge_dates"] = json.loads(sd_path.read_text(encoding="utf-8"))
        (SITE_DATA / "globe.json").write_text(json.dumps(clean_json(globe), separators=(",", ":")), encoding="utf-8")
        print(f"export_site: globe data exported ({sum(len(v) for v in globe['maps'].values())} cells, {len(space)} predictors)")

    # Reference fits: full overlap and a 1993-2012 window, with and without ONI.
    refs = []
    oni = idx.set_index(pd.to_datetime(idx["month"]))["noaa_oni"] if "noaa_oni" in idx else None
    for region, frame in level.groupby("region", sort=False):
        s = frame.set_index(pd.to_datetime(frame["date"]))["value"]
        for start, end in (("1993-01", "2012-12"), ("1950-01", "2025-12")):
            w = s.loc[start:end].dropna()
            if len(w) < 60:
                continue
            t = years(w.index)
            phase = 2*np.pi*(w.index.month.to_numpy()-1)/12
            base = np.column_stack((np.ones(len(t)), t-t.mean(), np.sin(phase), np.cos(phase), np.sin(2*phase), np.cos(2*phase)))
            plain = regression(w, base, w.index)
            entry = {"region": region, "start": start, "end": end, "trend": plain["beta"][1],
                     "ci": plain["ci"][1].tolist(), "rho": plain["rho"], "n_eff": plain["n_eff"]}
            if oni is not None:
                f = fit_with_index(w, oni, 0)
                entry.update(trend_enso=f["trend_mm_yr"], ci_enso=f["ci95_mm_yr"], coef_enso=f["index_coefficient"])
            refs.append(entry)
    (SITE_DATA / "reference_fits.json").write_text(json.dumps(clean_json(refs), indent=1), encoding="utf-8")
    print(f"export_site: {len(regions)} regions, {len(indices)} indices, {len(refs)} reference fits -> {SITE_DATA}")


if __name__ == "__main__":
    main()
