"""Assemble the West (Los Angeles) site files from westcoast/la/results, with the same keys as
pipeline/export_site.py writes for New York. Writes site_data/{ntr,globe,signal_winters,clue_map_ssh}_west.json
(local_gauges_west.json comes from wc_site_gauges.py).

Keys with no West equivalent are kept and set to null:
  ntr.sources.nao / .wind, ntr.lag_analysis.nao / .wind   NAO and New York Bight wind are New York predictors
  ntr.models                                              the monthly-mean NTR models are built on those predictors
"""
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
R, OUT = HERE / "la" / "results", HERE / "site_data"
NY_ONLY = ("nao", "wind")


def clean_json(value):   # as pipeline/common.py
    if isinstance(value, dict):
        return {str(k): clean_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [clean_json(v) for v in value]
    if isinstance(value, np.generic):
        return clean_json(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, (pd.Timestamp, pd.Period)):
        return str(value)
    return value


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ntr = json.loads((R / "ntr.json").read_text(encoding="utf-8"))
    seasons = pd.read_csv(R / "ntr_seasons.csv")
    seasons = seasons[seasons["start_year"] <= 2025]
    site_ntr = {"sources": {k: (None if k in NY_ONLY else v) for k, v in ntr["sources"].items()},
                "threshold_m": ntr["surge_threshold_m"],
                "seasons": [{"start_year": int(r.start_year), "surge_days": None if pd.isna(r.surge_days) else float(r.surge_days),
                             "enso_aug_sd": None if pd.isna(r.enso_aug) else round(float(r.enso_aug), 2), "months": int(r.months)}
                            for r in seasons.itertuples()],
                "season_outlook": ntr.get("season_outlook"),
                "lag_analysis": {k: (None if k in NY_ONLY else [{"lag": l["lag"], "r": l["r"], "significant": l["significant"]}
                                                                for l in v["all_months"]["lags"]])
                                 for k, v in ntr["lag_analysis"].items()},
                "models": None}
    (OUT / "ntr_west.json").write_text(json.dumps(clean_json(site_ntr), indent=1), encoding="utf-8")

    maps = json.loads((R / "explore_maps.json").read_text(encoding="utf-8"))
    ex = json.loads((R / "explore.json").read_text(encoding="utf-8"))
    space = json.loads((R / "explore_space_time.json").read_text(encoding="utf-8"))
    globe = {"n_seasons": maps["n_seasons"], "years": maps["years"], "r_p05": maps["r_p05"], "battery": maps["battery"],
             "nino34_box": maps["nino34_box"], "note": maps["note"],
             "maps": {m: [[c[0], c[1], round(c[2], 2)] for c in cells] for m, cells in maps["maps"].items()},
             "r_min_kept": 0.2,
             "predictors": space,
             "lead_curve": [{"index": r["index"], "month": r["month"], "rr": r["rr_all"], "ci": r["rr_all_ci"], "p": r["p_all"],
                             "loo": r["loo_skill"]} for r in ex["enso_lead_curve"]],
             "outlook": ex.get("outlook_2026", []),
             "screen": {k: {"tests": v["tests"], "discoveries": v["discoveries"], "confirmed": len(v["confirmed"])} for k, v in ex["monthly"].items()},
             "n_predictors": ex["n_predictors"], "train": ex["train"], "test": ex["test"]}
    sp = pd.read_csv(R / "season_predictions.csv").dropna(subset=["observed_surge_days", "pred_nasa_nino34_june_leave_one_out", "pred_trend_only_leave_one_out"])
    globe["winters"] = [{"year": int(r.season_start_year), "observed": float(r.observed_surge_days),
                         "model": round(float(r.pred_nasa_nino34_june_leave_one_out), 1),
                         "trend": round(float(r.pred_trend_only_leave_one_out), 1),
                         "nino_june_sd": round(float(r.nasa_nino34_june_sd), 2)} for r in sp.itertuples()]
    globe["surge_dates"] = json.loads((R / "surge_dates.json").read_text(encoding="utf-8"))
    (OUT / "globe_west.json").write_text(json.dumps(clean_json(globe), separators=(",", ":")), encoding="utf-8")
    (OUT / "clue_map_ssh_west.json").write_text((R / "explore_maps_ssh.json").read_text(encoding="utf-8"), encoding="utf-8")
    (OUT / "signal_winters_west.json").write_text((R / "signal_winters.json").read_text(encoding="utf-8"), encoding="utf-8")

    o, a = site_ntr["season_outlook"], site_ntr["season_outlook"]["all_seasons"]
    valid = [s["surge_days"] for s in site_ntr["seasons"] if s["surge_days"] is not None]
    strong = list(o["strong_el_nino_seasons"].values())
    print(f"threshold {site_ntr['threshold_m']:.4f} m; all seasons n {a['n']}: RR {a['rate_ratio_per_sd']:.3f} [{a['ci95'][0]:.3f}, {a['ci95'][1]:.3f}] "
          f"p {a['p']:.2g}, LOO RR {a['leave_one_out_rr_range']}; test skill {o['test_deviance_skill_vs_trend_only']:.3f} "
          f"(train RR {o['rate_ratio_per_sd']:.3f}); strong El Nino {o['strong_el_nino_seasons']} mean {np.mean(strong):.1f} vs avg {np.mean(valid):.1f}")
    if "outlook" in o:
        q = o["outlook"]
        print(f"outlook {q['season']}: Aug ENSO {q['enso_aug_sd']:+.2f} SD -> {q['expected_surge_days']:.1f} [{q['expected_ci95'][0]:.1f}, "
              f"{q['expected_ci95'][1]:.1f}] vs trend {q['trend_only_expected']:.1f}, extrapolation {q['extrapolation']}")
    for r in globe["lead_curve"]:
        if (r["index"], r["month"]) in (("oni", 8), ("nino34_giss", 6)):
            print(f"lead curve {r['index']} m{r['month']}: RR {r['rr']:.3f} [{r['ci'][0]:.3f}, {r['ci'][1]:.3f}] p {r['p']:.2g} LOO {r['loo']:+.3f}")
    for r in globe["outlook"]:
        print(f"globe outlook {r['index']} m{r['month']}: {r['value_sd']:+.2f} SD -> {r['expected']:.1f} [{r['ci'][0]:.1f}, {r['ci'][1]:.1f}] "
              f"vs trend {r['trend_only']:.1f}{' (beyond observed)' if r['extrapolation'] else ''}")
    print(f"winters {len(globe['winters'])}, screen {globe['screen']}, surge_dates top {globe['surge_dates']['top_days'][:3]}")


if __name__ == "__main__":
    main()
