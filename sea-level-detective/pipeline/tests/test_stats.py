"""Deterministic recovery, calibration and independent-reference checks."""
import unittest
import numpy as np
import pandas as pd
import pymannkendall as mk
from stats import (deseasonalize, sen_slope, mk_hamed_rao, seasonal_kendall,
                   ols_ar1, fit_with_index, naive_ols)
from e1_synthetic import ar1_noise, batch_pvalues, wilson, crossing


class StatsTests(unittest.TestCase):
    def setUp(self):
        self.dates = pd.date_range("1993-01-01", periods=360, freq="MS")
        self.time = np.arange(360)/12

    def test_recovers_known_trend(self):
        rng = np.random.default_rng(24)
        series = pd.Series(20+2.5*self.time+rng.normal(0, 1, 360), index=self.dates)
        for function in (sen_slope, ols_ar1):
            result = function(series)
            self.assertAlmostEqual(result["trend_mm_yr"], 2.5, delta=.04)
            self.assertLess(result["ci95_mm_yr"][0], 2.5)
            self.assertGreater(result["ci95_mm_yr"][1], 2.5)

    def test_calendar_gaps_do_not_accelerate_trend(self):
        series = pd.Series(4*self.time, index=self.dates).drop(self.dates[70:170])
        self.assertAlmostEqual(sen_slope(series)["trend_mm_yr"], 4, places=9)
        self.assertAlmostEqual(ols_ar1(series)["trend_mm_yr"], 4, places=9)

    def test_climatology_removed(self):
        series = pd.Series(np.sin(2*np.pi*self.time)*30+self.time, index=self.dates)
        residual = deseasonalize(series)
        np.testing.assert_allclose(residual.groupby(residual.index.month).mean(), 0, atol=1e-12)

    def test_joint_fit_preserves_every_non_index_component(self):
        rng = np.random.default_rng(42)
        index = pd.Series(.12*self.time+ar1_noise(rng, 1, 360, 1, .6)[0], index=self.dates)
        base = 10+3*self.time+9*np.sin(2*np.pi*self.time)+4*np.cos(4*np.pi*self.time)
        signal = pd.Series(base, index=self.dates)+7*index.shift(2)
        result = fit_with_index(signal, index, 2)
        self.assertAlmostEqual(result["trend_mm_yr"], 3, places=9)
        self.assertAlmostEqual(result["index_coefficient"], 7, places=9)
        np.testing.assert_allclose(result["index_removed"], base[2:], atol=1e-10)
        self.assertGreater(result["r2_with_index"], result["r2_without_index"])
        self.assertEqual(result["n"], 358)

    def test_index_lag_is_calendar_time(self):
        index = pd.Series(np.cos(self.time), index=self.dates).drop(self.dates[10])
        signal = pd.Series(2*self.time, index=self.dates)+5*index.reindex(self.dates).shift(1)
        result = fit_with_index(signal, index, 1)
        self.assertNotIn(self.dates[11], result["index_removed"].index)
        self.assertAlmostEqual(result["index_coefficient"], 5, places=9)

    def test_seasonal_kendall_preserves_missing_months(self):
        series = pd.Series(3*self.time+40*np.sin(2*np.pi*self.time), index=self.dates)
        series.iloc[50:53] = np.nan
        self.assertAlmostEqual(seasonal_kendall(series)["trend_mm_yr"], 3, places=8)

    def test_batched_tests_match_pymannkendall(self):
        noise = ar1_noise(np.random.default_rng(57), 4, 120, 30, .6)
        for trend, values in batch_pvalues(noise, (0, 3)).items():
            for i in range(len(noise)):
                y = noise[i]+trend*np.arange(120)/12
                references = {"plain_mk": mk.original_test(y).p,
                              "hamed_rao_mk": mk.hamed_rao_modification_test(y).p,
                              "seasonal_kendall": mk.seasonal_test(y, period=12).p}
                series = pd.Series(y, index=self.dates[:120])
                references.update(naive_ols=naive_ols(series)["p"], ar1_ols=ols_ar1(series)["p"])
                for method, expected in references.items():
                    self.assertAlmostEqual(values[method][i], expected, places=9, msg=method)

    def test_false_positive_sanity(self):
        noise = ar1_noise(np.random.default_rng(1004), 1000, 120, 30, 0)
        pvalues = batch_pvalues(noise, (0,))[0]
        for method in ("naive_ols", "plain_mk", "seasonal_kendall", "ar1_ols"):
            rate = np.mean(pvalues[method] < .05)
            self.assertGreater(rate, .015, method)
            self.assertLess(rate, .09, method)

    def test_ar1_adjustment_reduces_inflated_false_positives(self):
        noise = ar1_noise(np.random.default_rng(1998), 1000, 120, 30, .6)
        values = batch_pvalues(noise, (0,))[0]
        naive = np.mean(values["naive_ols"] < .05)
        adjusted = np.mean(values["ar1_ols"] < .05)
        self.assertGreater(naive, .15)
        self.assertLess(adjusted, naive)
        self.assertLess(adjusted, .13)

    def test_noise_sd_is_marginal(self):
        noise = ar1_noise(np.random.default_rng(9), 2000, 120, 30, .8)
        self.assertAlmostEqual(noise.std(), 30, delta=1)
        self.assertAlmostEqual(noise[:, 0].std(), 30, delta=2)

    def test_binomial_interval_and_crossing_boundaries(self):
        low, high = wilson(50, 1000)
        self.assertLess(low, .05)
        self.assertGreater(high, .05)
        self.assertAlmostEqual(crossing([10, 15], [.8, 1])["years"], 12.5)
        self.assertIsNone(crossing([10, 15], [.1, .2])["years"])
        self.assertIsNone(crossing([10, 15], [.95, .99])["years"])

    def test_constant_series_mk(self):
        result = mk_hamed_rao(pd.Series(10., index=self.dates))
        self.assertEqual(result["p"], 1)
        self.assertEqual(result["trend_mm_yr"], 0)


if __name__ == "__main__":
    unittest.main()
