"""Checks for the data standard: raw NASA-SSH layout in, standard format out."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd
import xarray as xr

import preprocess
from build_series import normalize_grid


def raw_nasa_like_grid():
    """Tiny grid in the documented raw layout (NASA-SSH V1 User Guide, Table 2)."""
    lat = np.array([-0.25, 0.25])
    lon = np.array([0.25, 179.75, 180.25, 359.75])          # degrees east, 0..360
    seconds = (pd.Timestamp("2000-01-03") - pd.Timestamp("1990-01-01")).total_seconds()
    ssha = np.full((1, 2, 4), 0.10)                           # metres
    basin = np.array([[1, 1, 5, 1], [1, 0, 1, 1]])            # 5 = lake, 0 = land
    counts = np.array([[500, 0, 500, 500], [500, 500, 500, 500]])
    ds = xr.Dataset(
        {"ssha": (("time", "latitude", "longitude"), ssha, {"units": "m"}),
         "basin_flag": (("latitude", "longitude"), basin),
         "counts": (("latitude", "longitude"), counts),
         "basin_names_table": (("basin",), np.array(["1: Pacific Ocean", "5: Lake Superior"]))},
        coords={"time": ("time", [seconds], {"units": "seconds since 1990-01-01 00:00:00"}),
                "latitude": lat, "longitude": lon})
    return xr.decode_cf(ds)


class TestGridStandard(unittest.TestCase):
    def test_raw_grid_conversions(self):
        preprocess.GRID_LOG.clear()   # filled once per process; other tests may have filled it
        ds = raw_nasa_like_grid()
        self.assertEqual(pd.Timestamp(ds.time.values[0]), pd.Timestamp("2000-01-03"))  # seconds since 1990 decoded
        out = normalize_grid(ds)
        self.assertTrue(float(out.longitude.min()) >= -180 and float(out.longitude.max()) < 180)
        self.assertTrue(np.all(np.diff(out.longitude.values) > 0))
        valid = out.values[np.isfinite(out.values)]
        np.testing.assert_allclose(valid, 100.0)                  # 0.10 m -> 100 mm
        # cells removed: lake (id 5), land (id 0), counts == 0  -> 3 of 8 cells NaN
        self.assertEqual(int(np.isnan(out.values).sum()), 3)
        self.assertIn(5, preprocess.GRID_LOG["basins_excluded"])

    def test_basin_names_char_array(self):
        table = xr.DataArray(np.array([list("1: Arctic Ocean    "), list("7: Caspian Sea     ")], dtype="S1"))
        names = preprocess.parse_basin_names(table)
        self.assertEqual(names[1], "Arctic Ocean")
        self.assertEqual(names[7], "Caspian Sea")


class TestSeriesStandard(unittest.TestCase):
    def series(self):
        idx = pd.date_range("1990-01-01", "2020-12-01", freq="MS")
        t = np.arange(len(idx)) / 12
        return pd.Series(3.0 * t + 20 * np.sin(2 * np.pi * idx.month / 12) + 500, index=idx, name="x")

    def test_rebaseline_and_deseason(self):
        std, mean0, n = preprocess.rebaseline(self.series())
        self.assertAlmostEqual(float(std["1993":"2012"].mean()), 0.0, places=9)
        self.assertEqual(n, 240)
        des = preprocess.deseason(std)
        # seasonal cycle removed: month-of-year means over the baseline are ~0
        base = des["1993":"2012"]
        self.assertLess(base.groupby(base.index.month).mean().abs().max(), 1e-9)

    def test_main_writes_standard_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            s = self.series()
            pd.DataFrame({"level_mm": s.values}, index=pd.Index(s.index, name="date")).to_csv(tmp / "gauge_8518750.csv")
            pd.DataFrame({"oni_c": np.sin(np.arange(len(s)))}, index=pd.Index(s.index, name="date")).to_csv(tmp / "oni.csv")
            with mock.patch.object(preprocess, "PROCESSED", tmp), \
                 mock.patch.object(preprocess, "GAUGES", {"8518750": {"name": "The Battery"}}):
                result = preprocess.main()
            monthly = pd.read_csv(tmp / "series_monthly.csv")
            self.assertEqual(set(monthly.columns), {"date", "region", "variable", "value", "unit", "source", "n_obs"})
            self.assertTrue(monthly["date"].str.fullmatch(r"\d{4}-\d{2}").all())
            self.assertEqual(set(monthly["unit"]), {"mm"})
            sl = monthly[(monthly.region == "gauge_the_battery") & (monthly.variable == "sea_level")]
            self.assertAlmostEqual(sl[sl.date.between("1993-01", "2012-12")]["value"].mean(), 0.0, places=6)
            idx = pd.read_csv(tmp / "indices_monthly.csv")
            self.assertIn("noaa_oni_z", idx.columns)
            self.assertTrue((tmp / "PROVENANCE.md").exists())
            self.assertIn("skipped", result["gmsl_check"])


if __name__ == "__main__":
    unittest.main()
