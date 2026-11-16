"""Descriptive, overlapping 10-year Sen trends; no pass/fail gate."""
import pandas as pd
from config import BOXES, ENSO_LAG, PROCESSED
from common import read_monthly, save_json
from stats import fit_with_index, sen_slope


def window_slopes(raw, removed):
    """Monthly-stepped 120-month windows; compare identical observed month pairs."""
    pair = pd.concat([raw.rename("raw"), removed.rename("index_removed")], axis=1)
    valid = pair.dropna()
    if valid.empty:
        raise ValueError("No raw/index-removed overlap")
    pair = pair.loc[valid.index.min():valid.index.max()].asfreq("MS")
    records = []
    for start in range(max(0, len(pair)-119)):
        part = pair.iloc[start:start+120].dropna()
        if len(part) < 3:
            continue
        records.append({"requested_window": [str(pair.index[start].date()), str(pair.index[start+119].date())],
                        "coverage_fraction": len(part)/120, "raw": sen_slope(part.raw),
                        "index_removed": sen_slope(part.index_removed)})
    return records


def main():
    boxes = read_monthly("box_monthly.csv")
    indices = {"nasa_enso": read_monthly("indicators.csv").enso,
               "noaa_oni": read_monthly("oni.csv").oni_c}
    results, rows = {}, []
    for box in BOXES:
        print(f"E3: overlapping windows, {box}", flush=True)
        results[box] = {"full_raw": sen_slope(boxes[box]), "indices": {}}
        for name, index in indices.items():
            fit = fit_with_index(boxes[box], index, ENSO_LAG)
            removed = fit.pop("index_removed")
            removed.to_csv(PROCESSED / f"{box}_{name}_removed.csv", index_label="date")
            matched = pd.concat([boxes[box].rename("raw"), removed.rename("removed")], axis=1).dropna()
            windows = window_slopes(boxes[box], removed)
            results[box]["indices"][name] = {"fit": fit, "full_matched_raw": sen_slope(matched.raw),
                                            "full_removed": sen_slope(matched.removed), "windows": windows}
            for record in windows:
                rows.append({"box": box, "index": name, "start": record["requested_window"][0],
                             "end": record["requested_window"][1], "n": record["raw"]["n"],
                             "raw_mm_yr": record["raw"]["trend_mm_yr"],
                             "removed_mm_yr": record["index_removed"]["trend_mm_yr"]})
    pd.DataFrame(rows).to_csv(PROCESSED / "window_trends.csv", index=False)
    return save_json("e3.json", {"experiment": "E3", "boxes": results,
                                "notes": ["Every monthly-start 10-year calendar window; overlapping estimates are descriptive, not independent tests.",
                                          "Raw and removed window slopes use identical months; coverage is reported.",
                                          "Index coefficient estimated once on each full matched record; only its index component is subtracted.",
                                          "No pass/fail gate. Sen CIs assume independent errors and do not propagate index-fit uncertainty."]})


if __name__ == "__main__":
    main()
