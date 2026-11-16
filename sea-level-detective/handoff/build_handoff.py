"""Assemble the team hand-off workbook (one sheet per table) and one CSV per sheet.

Only organizes existing outputs; no statistics are computed here. Sources:
  ../ntr/results/        NTR study and exploration, computed on the DGX (explore_*.py, model.py)
  ../pipeline/results/   E1 trend-test simulation and E4 tide-gauge fits
  ../pipeline/data_processed/  standard-format monthly sea level
Run: ..\\.venv\\Scripts\\python.exe build_handoff.py
"""
import json
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HERE = Path(__file__).resolve().parent
NTR = HERE.parent / "ntr" / "results"
PIPE = HERE.parent / "pipeline"
OUT_XLSX = HERE / "SeaLevelDetective_data_handoff.xlsx"
CSV_DIR = HERE / "csv"
FONT, BOLD = Font(name="Arial", size=10), Font(name="Arial", size=10, bold=True)
HEAD_FILL = PatternFill("solid", fgColor="DDE6F0")
TITLE = Font(name="Arial", size=14, bold=True)


def write_table(wb, name, df, note=None, widths=None):
    ws = wb.create_sheet(name)
    row0 = 1
    if note:
        ws.cell(1, 1, note).font = Font(name="Arial", size=10, italic=True)
        ws.cell(1, 1).alignment = Alignment(wrap_text=False)
        row0 = 3
    for j, col in enumerate(df.columns, 1):
        c = ws.cell(row0, j, str(col))
        c.font, c.fill, c.alignment = BOLD, HEAD_FILL, Alignment(wrap_text=True, vertical="top")
    for i, rec in enumerate(df.itertuples(index=False), row0 + 1):
        for j, v in enumerate(rec, 1):
            if isinstance(v, float) and v != v:
                v = None
            elif isinstance(v, (list, dict)):
                v = json.dumps(v)
            elif hasattr(v, "item"):
                v = v.item()
            c = ws.cell(i, j, v)
            c.font = FONT
            if isinstance(v, float):
                c.number_format = "0.000" if abs(v) < 10 else "0.0"
    ws.freeze_panes = ws.cell(row0 + 1, 2)
    ws.auto_filter.ref = f"A{row0}:{get_column_letter(len(df.columns))}{row0 + len(df)}"
    for j, col in enumerate(df.columns, 1):
        longest = max([len(str(col))] + [len(str(x)) for x in df.iloc[:200, j - 1].astype(str)])
        ws.column_dimensions[get_column_letter(j)].width = (widths or {}).get(col, min(max(10, longest + 2), 48))
    CSV_DIR.mkdir(exist_ok=True)
    df.to_csv(CSV_DIR / f"{name}.csv", index=False)
    return ws


def main():
    ex = json.loads((NTR / "explore.json").read_text(encoding="utf-8"))
    ntr = json.loads((NTR / "ntr.json").read_text(encoding="utf-8"))
    src = json.loads((NTR / "explore_sources.json").read_text(encoding="utf-8"))
    src.update({k: v for k, v in ex["sources"].items() if k not in src})
    seasons = pd.read_csv(NTR / "season_predictions.csv")
    monthly = pd.read_csv(NTR / "monthly_predictions.csv")
    coefs = pd.read_csv(NTR / "model_coefficients.csv")
    season_screen = pd.read_csv(NTR / "explore_season.csv")
    screen = pd.read_csv(NTR / "explore_screen.csv")
    predictors = pd.read_csv(NTR / "explore_monthly.csv")
    predictors["date"] = predictors["date"].str.slice(0, 7)
    space = pd.DataFrame(json.loads((NTR / "explore_space_time.json").read_text(encoding="utf-8")))
    maps = json.loads((NTR / "explore_maps.json").read_text(encoding="utf-8"))
    e1 = json.loads((PIPE / "results" / "e1.json").read_text(encoding="utf-8"))
    e4 = json.loads((PIPE / "results" / "e4.json").read_text(encoding="utf-8"))
    sea = pd.read_csv(PIPE / "data_processed" / "series_monthly_wide.csv")

    lead = pd.DataFrame([{"enso_index": r["index"], "month_of_start_year": r["month"], "months_before_october": r["months_before_october"],
                          "rate_ratio_per_sd": r["rr_all"], "ci95_low": r["rr_all_ci"][0], "ci95_high": r["rr_all_ci"][1], "p": r["p_all"],
                          "leave_one_out_skill": r["loo_skill"], "test_skill": r["test_skill"], "n_seasons": r["n_all"]} for r in ex["enso_lead_curve"]])
    outlook = pd.DataFrame([{"enso_index": r["index"], "month_2026": r["month"], "enso_value_sd": r["value_sd"], "largest_value_seen_sd": r["observed_max_sd"],
                             "extrapolation": r["extrapolation"], "expected_surge_days": r["expected"], "ci95_low": r["ci"][0], "ci95_high": r["ci"][1],
                             "trend_only_expected": r["trend_only"]} for r in ex["outlook_2026"]])
    resp = pd.DataFrame([{"calendar_month": r["month"], "rate_ratio_per_sd_august_oni": r["rr"], "ci95_low": r["ci"][0], "ci95_high": r["ci"][1],
                          "p": r["p"], "mean_surge_days": r["mean_days"], "n_years": r["n"]} for r in ex["response_by_month"]])
    mon_models = pd.DataFrame([{"model": k, "skill_vs_climatology": v["skill_vs_climatology"], "rmse_mm": v["rmse_mm"],
                                "rmse_climatology_mm": v["rmse_climatology_mm"], "n_train": v["n_train"], "n_test": v["n_test"]}
                               for k, v in ntr["models"].items()])
    gmap = pd.DataFrame([(int(m), c[0], c[1], c[2]) for m, cells in maps["maps"].items() for c in cells if abs(c[2]) >= maps["r_p05"]],
                        columns=["month_of_start_year", "lat", "lon", "spearman_r"])
    e1t = pd.DataFrame([{"record_years": r["window_years"], "true_trend_mm_per_yr": r["true_trend_mm_yr"], "test": r["method"],
                         "rejection_rate": r["estimate"], "ci95_low": r["ci95"][0], "ci95_high": r["ci95"][1], "n_series": r["n"]} for r in e1["settings"]])
    grow = []
    for st, g in e4["gauges"].items():
        for t in g["trends"]:
            grow.append({"gauge": g["name"], "station": st, "method": t["method"], "trend_mm_per_yr": t["trend_mm_yr"],
                         "ci95_low": t["ci95_mm_yr"][0], "ci95_high": t["ci95_mm_yr"][1], "p": t.get("p"), "window": "..".join(t["window"]), "n_months": t["n"]})
        o = g["oni_fit"]
        grow.append({"gauge": g["name"], "station": st, "method": "ONI amplitude (mm per deg C), joint fit with trend and seasons",
                     "trend_mm_per_yr": o["index_coefficient"], "ci95_low": o["index_ci95"][0], "ci95_high": o["index_ci95"][1], "p": None,
                     "window": "..".join(o["window"]), "n_months": o["n"]})
    gauges = pd.DataFrame(grow)
    sources = pd.DataFrame([{"column_or_dataset": k, "source": v["source"], "nasa_data": "yes" if v.get("nasa") else "no"} for k, v in src.items()])
    extra = pd.DataFrame([
        {"column_or_dataset": "Battery hourly water level and tide prediction (target)", "source": "NOAA CO-OPS station 8518750, products hourly_height and predictions, datum MSL, metres, GMT", "nasa_data": "no"},
        {"column_or_dataset": "Globe map temperature field", "source": "NASA GISTEMP v4 gridded (gistemp1200_GHCNv4_ERSSTv5), 2 x 2 degree, data.giss.nasa.gov", "nasa_data": "yes"},
        {"column_or_dataset": "Sea_level_monthly sheet", "source": "NOAA CO-OPS monthly mean sea level: The Battery 8518750, La Jolla 9410230, San Francisco 9414290", "nasa_data": "no"}])
    sources = pd.concat([extra, sources], ignore_index=True)

    te = seasons[seasons.period == "test"].dropna(subset=["observed_surge_days", "pred_oni_august_trainfit"])
    mae = lambda c: float((te["observed_surge_days"] - te[c]).abs().mean())
    a = ntr["season_outlook"]["all_seasons"]
    best = max((r for r in ex["enso_lead_curve"] if r["index"] == "nino34_giss"), key=lambda r: r["loo_skill"])
    st = {r["predictor"]: r for r in ex["season"]["table"]}
    key = pd.DataFrame([
        ["Surge days per cool season at the Battery (mean, 1980-2025)", round(float(seasons["observed_surge_days"].mean()), 1), "", "days", "Season_predictions"],
        ["August El Nino (NOAA ONI): surge days multiplied by, per 1 SD (43 winters)", round(a["rate_ratio_per_sd"], 2), f"{a['ci95'][0]:.2f} to {a['ci95'][1]:.2f}", "rate ratio", "ENSO_lead_time"],
        ["Same, leave-one-winter-out range", f"{a['leave_one_out_rr_range'][0]:.2f} to {a['leave_one_out_rr_range'][1]:.2f}", f"max p {a['leave_one_out_max_p']:.4f}", "rate ratio", "ntr/results/ntr.json"],
        ["NASA GISTEMP Nino3.4, Jul-Sep: held-out skill (2010-2025) vs trend only", round(st["nino34_giss"]["test_skill"], 2), "", "deviance skill", "Season_screening"],
        ["NOAA ONI, Jul-Sep: held-out skill (2010-2025) vs trend only", round(st["oni"]["test_skill"], 2), "", "deviance skill", "Season_screening"],
        [f"Best lead month (NASA Nino3.4): month {best['month']}, surge days multiplied by, per 1 SD", round(best["rr_all"], 2), f"{best['rr_all_ci'][0]:.2f} to {best['rr_all_ci'][1]:.2f}", "rate ratio", "ENSO_lead_time"],
        ["Held-out mean absolute error, trend only", round(mae("pred_trend_only_trainfit"), 2), "", "days per season", "Season_predictions"],
        ["Held-out mean absolute error, + ONI in August", round(mae("pred_oni_august_trainfit"), 2), "", "days per season", "Season_predictions"],
        ["Held-out mean absolute error, + NASA Nino3.4 in June", round(mae("pred_nasa_nino34_june_trainfit"), 2), "", "days per season", "Season_predictions"],
        ["Monthly screening: predictor x lead tests per target", ex["monthly"]["mean NTR, all months"]["tests"], "", "tests", "Monthly_screening"],
        ["Monthly screening: leading signals that add skill beyond persistence", 0, "1 confirmed on test (Portland, 1 month) but gain +0.001", "signals", "Monthly_screening"],
        ["Same-month model (wind + NAO + ONI): held-out skill for monthly mean NTR", round(ntr["models"]["all concurrent (best lag 0-6)"]["skill_vs_climatology"], 2), "", "skill vs climatology", "Monthly_models"],
        ["Trend tests, 10-year records with no trend: false-alarm rate, naive OLS", round(next(r["estimate"] for r in e1["settings"] if r["window_years"] == 10 and r["true_trend_mm_yr"] == 0 and r["method"] == "naive_ols"), 3), "should be 0.05", "fraction", "Trend_tests_E1"],
        ["Same, AR(1)-adjusted OLS (the test used)", round(next(r["estimate"] for r in e1["settings"] if r["window_years"] == 10 and r["true_trend_mm_yr"] == 0 and r["method"] == "ar1_ols"), 3), "should be 0.05", "fraction", "Trend_tests_E1"],
    ], columns=["result", "value", "interval_or_note", "unit", "where_to_find_it"])

    readme = [
        ("Sea Level Detective: data hand-off", TITLE),
        ("NASA Space Apps 2026, challenge 'Be An Earth System Trend Detective!'. Workbook built 2026-11-15.", FONT),
        ("", FONT),
        ("THEME", BOLD),
        ("Understanding New York Harbor's water level with OTHER (global) data: where on Earth the signal is, how far away, and how far ahead.", FONT),
        ("", FONT),
        ("WHAT IS PREDICTED", BOLD),
        ("Non-tidal residual (NTR) at the Battery = observed hourly water level minus predicted astronomical tide (NOAA).", FONT),
        ("Surge day = a day whose daily-mean NTR is more than 0.30 m above its 365-day running mean (as in Sweet & Zervas 2011). Cool season = October to April.", FONT),
        ("", FONT),
        ("SHEETS", BOLD),
        ("Key_results: headline numbers and the sheet each comes from.", FONT),
        ("Data_sources: every dataset and column, its provider, and whether it is NASA data.", FONT),
        ("Season_predictions: per winter, observed surge days vs the trend-only model and the El Nino models (fitted and leave-one-out).", FONT),
        ("Monthly_predictions: per month, observed NTR anomaly vs persistence and the same-month model; plus the inputs.", FONT),
        ("Model_coefficients: every fitted coefficient with its 95% interval.", FONT),
        ("Season_screening: 30 candidate signals (Jul-Sep average) tested as predictors of the coming winter's surge days.", FONT),
        ("ENSO_lead_time: the El Nino effect when El Nino is read in each month, January to December.", FONT),
        ("Outlook_2026_27: expected surge days for winter 2026-27 from each lead month; 'extrapolation' = beyond anything in the record.", FONT),
        ("Response_by_month: which cool-season month responds to August El Nino.", FONT),
        ("Space_time: each signal's location, distance to New York Harbor, same-month link and next-winter skill.", FONT),
        ("Monthly_models: held-out skill of the monthly models (first NTR study, train 1993-2012, test 2013 on).", FONT),
        ("Monthly_screening: prewhitened correlation of every signal at leads of 0 to 12 months, three targets; 'discovery' = passed FDR 10% on train.", FONT),
        ("Predictors_monthly: the processed monthly table of all candidate signals (raw units; see Data_sources).", FONT),
        ("Globe_map: the cells drawn on the website globe: correlation of NASA GISTEMP temperature in a month with the following winter's surge days.", FONT),
        ("Trend_tests_E1: simulation of five trend tests (false-alarm rate and power).", FONT),
        ("Gauge_trends_E4: sea-level trends and El Nino amplitude at three tide gauges.", FONT),
        ("Sea_level_monthly: monthly sea level at the three gauges, mm, 1993-2012 average = 0 (used by the website explorer).", FONT),
        ("", FONT),
        ("METHOD IN BRIEF", BOLD),
        ("Splits fixed before running: monthly train 1981-2010, test 2011 on; seasons train 1981-2009, test 2010-2025.", FONT),
        ("Every signal: train monthly climatology and train linear trend removed, then divided by its train standard deviation ('SD').", FONT),
        ("Season model: quasi-Poisson regression with log link, surge days ~ time + signal. 'Rate ratio per SD' = factor by which surge days multiply per 1 SD.", FONT),
        ("Skill = 1 - (model deviance or squared error) / (reference). Reference: trend-only for seasons, climatology for months. Above 0 = better than the reference.", FONT),
        ("Monthly screening: both series prewhitened with the signal's AR(1) filter; Benjamini-Hochberg FDR 10% over all signal x lead tests; then checked on test data.", FONT),
        ("", FONT),
        ("CAVEATS", BOLD),
        ("Globe_map is exploratory: thousands of cells, no field-significance correction. The confirmed predictor is the Nino3.4 region.", FONT),
        ("Outlook 2026-27: El Nino in summer 2026 is stronger than any summer in the record, so the model is extrapolating.", FONT),
        ("1997/98 has only 5 valid months at the Battery and is left out of the season totals.", FONT),
        ("The first NTR study (Monthly_models) used train 1993-2012; the exploration used the longer split above. Both are stated on their sheets.", FONT),
        ("Other East Coast gauges (repeat of the El Nino test) are not included: their hourly data were still downloading.", FONT),
        ("", FONT),
        ("WHERE THE CODE IS", BOLD),
        ("nasa_spaceapps_2026/ntr/ (NTR study, exploration; run on the DGX), pipeline/ (sea-level explorer), site/ (website). CSV copies of every sheet: handoff/csv/.", FONT),
    ]

    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    for i, (text, font) in enumerate(readme, 1):
        ws.cell(i, 1, text).font = font
    ws.column_dimensions["A"].width = 150
    write_table(wb, "Key_results", key, widths={"result": 78, "interval_or_note": 44, "where_to_find_it": 24})
    write_table(wb, "Data_sources", sources, widths={"column_or_dataset": 52, "source": 100})
    write_table(wb, "Season_predictions", seasons, "Surge days per cool season at the Battery. *_trainfit: model fitted on 1981-2009 (a forecast for 'test' rows). *_leave_one_out: fitted without that season. Predictors in SD units.")
    write_table(wb, "Monthly_predictions", monthly, "Monthly mean NTR anomaly at the Battery (mm; train climatology and trend removed). Models fitted on 1981-2010; 'test' rows are forecasts.")
    write_table(wb, "Model_coefficients", coefs, "Season models use a log link: exp_coefficient is the rate ratio per unit of the term. Monthly models are in mm.", widths={"model": 78})
    write_table(wb, "Season_screening", season_screen, "Jul-Sep signal -> Oct-Apr surge days. rr = rate ratio per SD. 'confirmed' = FDR discovery on train AND test skill > 0 AND leave-one-out skill > 0.")
    write_table(wb, "ENSO_lead_time", lead, "El Nino read in each month of the season's start year; all seasons 1981-2025. Months 10-12 fall inside the surge season.")
    write_table(wb, "Outlook_2026_27", outlook, "Expected Oct 2026-Apr 2027 surge days (95% interval for the mean, not for one season). Typical winter: about 10.")
    write_table(wb, "Response_by_month", resp, "August ONI -> surge days in each cool-season month, 1981-2025.")
    write_table(wb, "Space_time", space.sort_values("distance_km"), "same_month_r: prewhitened correlation with monthly mean NTR (train 1981-2010). season_*: Jul-Sep signal -> next winter's surge days.", widths={"label": 44})
    write_table(wb, "Monthly_models", mon_models, f"First NTR study: train {ntr['train'][0]}..{ntr['train'][1]}, test {ntr['test'][0]} on. Sources: {ntr['sources']}", widths={"model": 40})
    write_table(wb, "Monthly_screening", screen, "lead 0 = same month (reference, not tested). r_train: prewhitened correlation on 1981-2010. discovery: FDR 10% among leads 1-12.")
    write_table(wb, "Predictors_monthly", predictors, "Processed monthly values in raw units. Units and providers: see Data_sources. msl_* in mm; *_power pressure in kPa; wind in m/s; *_giss in deg C.")
    write_table(wb, "Globe_map", gmap, f"Spearman r between NASA GISTEMP cell temperature in the month and the following winter's surge days ({maps['n_seasons']} winters); only |r| >= {maps['r_p05']:.2f} kept. Exploratory.")
    write_table(wb, "Trend_tests_E1", e1t, f"1,000 simulated monthly records per setting; AR(1) noise SD {e1['noise']['sigma_mm']:.1f} mm, phi {e1['noise']['phi']:.2f}. At true trend 0 the rejection rate is the false-alarm rate (should be 0.05).")
    write_table(wb, "Gauge_trends_E4", gauges, "Monthly mean sea level (relative to land). Trends in mm/yr; the ONI rows are in mm per deg C.", widths={"method": 60})
    write_table(wb, "Sea_level_monthly", sea, "Monthly sea level, mm, each series re-zeroed to its 1993-2012 mean. *_deseason: 1993-2012 monthly climatology removed.")
    wb.save(OUT_XLSX)
    print(f"wrote {OUT_XLSX.name} with {len(wb.sheetnames)} sheets: {wb.sheetnames}")
    print(f"csv files: {len(list(CSV_DIR.glob('*.csv')))} in {CSV_DIR}")


if __name__ == "__main__":
    main()
