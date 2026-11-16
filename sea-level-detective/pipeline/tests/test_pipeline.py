"""Offline fixtures exercise ingestion and the NASA/network execution boundary."""
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
import xarray as xr
from config import ROOT
from fetch_noaa import parse_gauge, parse_oni, windows, NetworkUnavailable
from build_series import normalize_grid, box_mean, coarsen_1deg, parse_indicator
from e2_seesaw import map_regression, el_nino_periods
from e3_windows import window_slopes
from e4_coasts import winter_comparison
from common import clean_json


class IngestionTests(unittest.TestCase):
    def test_noaa_monthly_schema_and_units(self):
        series = parse_gauge({"data": [{"year": "2001", "month": "2", "MSL": "0.123"},
                                       {"year": "2001", "month": "3", "MSL": ""}]})
        self.assertEqual(series.iloc[0], 123)
        self.assertTrue(np.isnan(series.iloc[1]))
        self.assertEqual(series.index[0], pd.Timestamp("2001-02-01"))
        self.assertTrue(parse_gauge({"error": {"message": "No data was found"}}).empty)
        with self.assertRaises(ValueError):
            parse_gauge({"error": {"message": "Invalid datum"}})

    def test_windows_are_complete_nonoverlapping_ten_year_chunks(self):
        spans = list(windows(1990, date(2026, 11, 14)))
        self.assertEqual(spans[-1][1], pd.Timestamp("2026-10-31"))
        for i, (start, end) in enumerate(spans):
            self.assertLess(end, start+pd.DateOffset(years=10))
            if i:
                self.assertEqual(start, spans[i-1][1]+pd.Timedelta(days=1))

    def test_oni_central_month_and_djf_year(self):
        oni = parse_oni("SEAS YR TOTAL ANOM\nDJF 1998 28.0 2.1\nNDJ 1998 26.0 -1.2\n")
        self.assertEqual(oni.loc["1998-01-01"], 2.1)
        self.assertEqual(oni.loc["1998-12-01"], -1.2)

    def test_longitude_units_area_weights_and_coarsening(self):
        ds = xr.Dataset({"ssha": (("lat", "lon"), [[.01, .03], [.05, np.nan]])},
                        coords={"lat": [0.25, .75], "lon": [210.25, 210.75]})
        ds.ssha.attrs["units"] = "m"
        grid = normalize_grid(ds)
        self.assertAlmostEqual(float(grid.longitude[0]), -149.75)
        expected = (40*np.cos(np.deg2rad(.25))+50*np.cos(np.deg2rad(.75)))/(2*np.cos(np.deg2rad(.25))+np.cos(np.deg2rad(.75)))
        self.assertAlmostEqual(box_mean(grid, (0, 1, -150, -149)), expected)
        coarse = coarsen_1deg(grid)
        self.assertEqual(coarse.shape, (1, 1))
        self.assertAlmostEqual(float(coarse.values[0, 0]), expected)

    def test_cf_quality_flags_are_respected(self):
        ds = xr.Dataset({"ssha": (("latitude", "longitude"), [[.01, .99]]),
                         "quality": (("latitude", "longitude"), [[0, 1]])},
                        coords={"latitude": [0.25], "longitude": [0.25, .75]})
        ds.ssha.attrs.update(units="m", ancillary_variables="quality")
        ds.quality.attrs.update(flag_values=[0, 1], flag_meanings="good bad")
        grid = normalize_grid(ds)
        self.assertTrue(np.isnan(grid.values[0, 1]))

    def test_indicator_header_selection_and_cm_conversion(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            path = Path(temp)/"indicator.txt"
            path.write_text("# 1: decimal year\n# 2: GMSL (cm)\n# 3: smoothed GMSL (cm)\n1993.0 1.2 9.0\n1993.1 1.3 8.0\n", encoding="utf-8")
            series, info = parse_indicator(path, "gmsl")
            self.assertEqual(series.iloc[0], 12)
            self.assertEqual(info["value_column_1based"], 2)
            path.write_text("# unknown columns\n1993.0 1.2 9.0\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_indicator(path, "gmsl")

    def test_map_slope_recovers_known_coefficient(self):
        dates = pd.date_range("2000-01-01", periods=120, freq="MS")
        index = pd.Series(np.random.default_rng(11).normal(size=120), index=dates)
        grid = xr.DataArray((3+7*index.to_numpy())[:, None, None],
                            dims=("time", "latitude", "longitude"),
                            coords={"time": dates, "latitude": [0.5], "longitude": [150.5]})
        result = map_regression(grid, index, 0)
        self.assertAlmostEqual(float(result.coefficient.values[0, 0]), 7)
        self.assertEqual(float(result.n.values[0, 0]), 120)

    def test_overlapping_windows_include_last_possible_window(self):
        dates = pd.date_range("2000-01-01", periods=122, freq="MS")
        raw = pd.Series(np.arange(122)/12*3, index=dates)
        records = window_slopes(raw, raw)
        self.assertEqual(len(records), 3)
        self.assertAlmostEqual(records[-1]["raw"]["trend_mm_yr"], 3)
        self.assertEqual(records[-1]["raw"]["n"], 120)

    def test_el_nino_requires_five_seasons(self):
        oni = pd.Series([.6]*5+[0]+[.6]*4, index=pd.date_range("2000-01-01", periods=10, freq="MS"))
        periods = el_nino_periods(oni)
        self.assertEqual(periods, [(pd.Timestamp("2000-01-01"), pd.Timestamp("2000-06-01"))])

    def test_json_is_strict(self):
        text = json.dumps(clean_json({"value": np.float64(np.nan), "flag": np.bool_(True)}), allow_nan=False)
        self.assertEqual(json.loads(text), {"value": None, "flag": True})

    def test_battery_winter_year_and_complete_month_requirement(self):
        dates = pd.date_range("1999-10-01", "2005-04-01", freq="MS")
        winter_year = dates.year+(dates.month >= 10)
        gauge = pd.Series(np.where(winter_year % 2 == 0, 12., -3.), index=dates)
        gauge.loc["2000-11-01"] = np.nan  # Excludes the winter identified by January 2001.
        oni = pd.Series(np.where(dates.year % 2 == 0, 1., 0.), index=dates)
        with tempfile.TemporaryDirectory(dir=ROOT) as temp, \
             patch("e4_coasts.PROCESSED", Path(temp)), patch("e4_coasts.PERMUTATIONS", 99):
            result = winter_comparison(gauge, oni)
        self.assertEqual(result["n"], 5)
        self.assertEqual(result["el_nino"]["n"], 3)
        self.assertEqual(result["other"]["n"], 2)
        self.assertNotIn(2001, [winter["year"] for winter in result["winters"]])
        self.assertGreater(result["difference_mm"], 0)


class RunnerTests(unittest.TestCase):
    def test_no_nasa_never_imports_nasa_fetcher(self):
        import run_all
        with patch.dict("sys.modules", {"fetch_nasa": None}), \
             patch("fetch_noaa.main", return_value={}), \
             patch("e1_synthetic.main", return_value={}) as e1, \
             patch("e4_coasts.main", return_value={}) as e4, \
             patch("run_all.write_summary") as summary:
            self.assertEqual(run_all.main(["--no-nasa"]), 0)
            e1.assert_called_once_with()
            e4.assert_called_once_with(no_nasa=True)
            summary.assert_called_once()

    def test_noaa_network_failure_stops_before_experiments(self):
        import run_all
        with patch("fetch_noaa.main", side_effect=NetworkUnavailable("offline fixture")), \
             patch("e1_synthetic.main") as e1, patch("run_all.write_summary") as summary:
            self.assertEqual(run_all.main(["--no-nasa"]), 2)
            e1.assert_not_called()
            summary.assert_not_called()


if __name__ == "__main__":
    unittest.main()
