"""Hourly NTR -> monthly targets.

ntr_monthly.csv columns (index = month start):
  ntr_mean_mm   monthly mean NTR (mm); months with < 80% of hours are NaN
  surge_days    number of days whose daily-mean surge exceeds the threshold (0.30 m), following Sweet & Zervas (2011):
                daily-mean NTR minus its 365-day centred running mean (removes sea-level rise and seasonal level
                changes, and tide-phase spikes that daily maxima would count)
  hours         hours with a valid NTR value
"""
import pandas as pd
from config_ntr import PROCESSED, SURGE_THRESHOLD_M, MIN_HOURS_FRACTION, ensure_dirs


def main():
    ensure_dirs()
    h = pd.read_csv(PROCESSED / "ntr_hourly.csv", parse_dates=["time"]).set_index("time")["ntr_m"]
    hours = h.resample("MS").count()
    expected = h.resample("MS").size().index.days_in_month * 24
    mean = h.resample("MS").mean() * 1000
    mean[hours < MIN_HOURS_FRACTION * expected] = float("nan")
    daily_ok = h.resample("D").count() >= 20
    daily_mean = h.resample("D").mean().where(daily_ok)
    background = daily_mean.rolling(365, center=True, min_periods=300).mean()
    surge = ((daily_mean - background) > SURGE_THRESHOLD_M) & daily_ok
    surge_days = surge.resample("MS").sum().astype(float)
    surge_days[hours < MIN_HOURS_FRACTION * expected] = float("nan")
    out = pd.DataFrame({"ntr_mean_mm": mean, "surge_days": surge_days, "hours": hours})
    out.to_csv(PROCESSED / "ntr_monthly.csv", index_label="date")
    print(f"build_ntr: {out['ntr_mean_mm'].count()} valid months, "
          f"{int(out['surge_days'].sum())} surge days > {SURGE_THRESHOLD_M} m", flush=True)
    return out


if __name__ == "__main__":
    main()
