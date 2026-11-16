"""Run the complete pipeline, or only public-data experiments with --no-nasa."""
import argparse
import json
import sys
from datetime import datetime, timezone
from config import RESULTS, ensure_dirs
from common import clean_json


def format_number(value):
    if value is None:
        return "N/A"
    return f"{value:.6g}" if isinstance(value, (int, float)) else str(value)


def interval(value, ci):
    return f"{format_number(value)} [{', '.join(format_number(v) for v in ci)}]" if ci else f"{format_number(value)} (CI N/A)"


def write_summary(results, no_nasa):
    """Human-readable results plus exact JSON appendix for every reported scalar."""
    results = clean_json(results)
    lines = ["# Sea Level Detective results", "", f"Generated: {datetime.now(timezone.utc).isoformat()}", "",
             f"Mode: {'no-NASA (public NOAA only)' if no_nasa else 'NASA + NOAA'}.", "",
             "All intervals are 95%. Trends: mm/year. Sea level: mm. ONI: degrees C. "
             "N/A denotes a descriptive quantity with no inferential interval, not zero uncertainty.", ""]
    if no_nasa:
        lines += ["E0, E2, E3 and NASA coastal comparisons were skipped. NASA authentication/downloads were not invoked.", ""]
    e1 = results["e1"]
    noise = e1["noise"]
    lines += ["## E1: synthetic detection", "", f"Noise: marginal SD {noise['sigma_mm']:.6g} mm; monthly phi {noise['phi']:.6g}. "
              f"{noise['method']}. Seed {e1['seed']}. Runtime {e1['elapsed_seconds']:.3f} seconds.", "",
              "Each cell is rejection proportion [binomial Wilson CI], n=1000 independent series per setting. "
              "Trend 0 reports false positives; positive trends report power. Two-sided alpha=0.05.", "",
              "| Years | Months | True trend (mm/yr) | Naive OLS | Plain MK | Hamed-Rao MK | Seasonal Kendall | AR(1)-OLS |",
              "|---:|---:|---:|---|---|---|---|---|"]
    from e1_synthetic import METHODS
    settings = e1["settings"]
    for years in sorted({r["window_years"] for r in settings}):
        for trend in sorted({r["true_trend_mm_yr"] for r in settings}):
            rows = {r["method"]: r for r in settings if r["window_years"] == years and r["true_trend_mm_yr"] == trend}
            lines.append(f"| {years} | {years*12} | {trend:g} | " + " | ".join(interval(rows[m]["estimate"], rows[m]["ci95"]) for m in METHODS) + " |")
    lines += ["", "Weatherhead comparison applies only to plain stationary AR(1) simulations. "
              "Weatherhead et al. (1998) formula for monthly data: SD and lag-1 autocorrelation of the monthly noise, trend per year, "
              "n* in years. Crossings use linear interpolation inside the tested bracket; no crossing CI.", "",
              "| Trend (mm/yr) | Weatherhead n* (years) | Empirical AR(1)-OLS 90% crossing |",
              "|---:|---:|---|"]
    for row in e1["weatherhead"]:
        cross = row["empirical_crossing"]
        description = f"{cross['years']:.6g} years; {cross['status']}" if cross["years"] is not None else cross["status"]
        lines.append(f"| {row['trend_mm_yr']} | {row['weatherhead_years']:.6g} | {description} |")
    lines += ["", "## E4: coasts", ""]
    for station, gauge in results["e4"]["gauges"].items():
        lines += [f"### {gauge['name']} ({station})", "", f"Record: {' to '.join(gauge['window'])}; n={gauge['n']} observed months; "
                  f"{gauge['missing_months']} missing calendar months. Relative sea level, datum MSL.", "",
                  "| Method | Trend [95% CI] (mm/yr) | p | Window | n |", "|---|---|---:|---|---:|"]
        for row in gauge["trends"]:
            lines.append(f"| {row['method']} | {interval(row['trend_mm_yr'], row['ci95_mm_yr'])} | {format_number(row.get('p'))} | {' to '.join(row['window'])} | {row['n']} |")
        fit = gauge["oni_fit"]
        lines += ["", f"ONI joint trend/harmonics/index fit: lag={fit['lag_months']} months; "
                  f"window={' to '.join(fit['window'])}; n={fit['n']}. Amplitude="
                  f"{interval(fit['index_coefficient'], fit['index_ci95'])} mm/degree C; "
                  f"trend={interval(fit['trend_mm_yr'], fit['ci95_mm_yr'])} mm/year. "
                  f"R² with index={fit['r2_with_index']:.6g}; without={fit['r2_without_index']:.6g}.", ""]
        for peak in gauge["peaks"]:
            lines.append(f"- {peak['event']}: peak={format_number(peak['peak_mm'])} mm in {peak['peak_month']}; "
                         f"window={' to '.join(peak['requested_window'])}; n={peak['n']}; {peak['method']}; {peak['ci_note']}.")
        lines.append("")
    winter = results["e4"]["battery_winters"]
    lines += ["### Battery cool-season comparison", "", f"{winter['method']}. Window: {' to '.join(winter['window'])}; n={winter['n']} complete winters.", "",
              f"El Nino winters: {interval(winter['el_nino']['mean_mm'], winter['el_nino']['ci95_mm'])} mm, n={winter['el_nino']['n']}. "
              f"Other winters: {interval(winter['other']['mean_mm'], winter['other']['ci95_mm'])} mm, n={winter['other']['n']}.", "",
              f"Difference: {interval(winter['difference_mm'], winter['ci95_mm'])} mm ({winter['ci_method']}); "
              f"Welch t={winter['welch_t']:.6g}, df={winter['welch_df']:.6g}, p={winter['welch_p']:.6g}. "
              f"Permutation p={winter['permutation_p']:.6g}, {winter['permutations']} permutations, seed={winter['seed']}.", ""]
    lines += ["## Method notes", ""]
    lines += [f"- {note}" for note in e1["notes"]+results["e4"]["notes"]]
    # Exact structured appendix retains windows, counts, methods and CIs without
    # silently discarding diagnostics or the numerous overlapping NASA windows.
    lines += ["", "## Complete numeric record", "",
              "This appendix includes every scalar result and diagnostic. Per-cell E2 fields are in the named NetCDF files; "
              "their arrays include coefficient, CI, n and effective n at each cell. "
              "Diagnostic counts, R², rho, observed peaks, timings and configuration constants have no inferential CI unless one is explicitly supplied.", "",
              "```json", json.dumps(results, indent=2, allow_nan=False), "```", ""]
    (RESULTS / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-nasa", action="store_true", help="Fetch NOAA and run only E1 and the gauge part of E4")
    args = parser.parse_args(argv)
    ensure_dirs()
    from fetch_noaa import main as fetch_noaa, NetworkUnavailable
    try:
        noaa = fetch_noaa()
    except NetworkUnavailable as exc:
        print(f"STOP: NOAA network access unavailable. No experiments were run.\n{exc}", file=sys.stderr)
        return 2
    results = {"noaa": noaa}
    if not args.no_nasa:
        from fetch_nasa import main as fetch_nasa
        from build_series import main as build_series
        fetch_nasa()
        build_series()
    from preprocess import main as preprocess
    results["preprocess"] = preprocess()  # standard-format files + checks (DATA_STANDARD.md)
    if not args.no_nasa:
        from e0_global import main as e0
        from e2_seesaw import main as e2
        from e3_windows import main as e3
        results.update(e0=e0(), e2=e2(), e3=e3())
    from e1_synthetic import main as e1
    from e4_coasts import main as e4
    results["e1"] = e1()
    results["e4"] = e4(no_nasa=args.no_nasa)
    write_summary(results, args.no_nasa)
    from export_site import main as export_site
    export_site()  # refresh ../site/data/ so the website shows these results
    print(f"Complete: {RESULTS / 'summary.md'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
