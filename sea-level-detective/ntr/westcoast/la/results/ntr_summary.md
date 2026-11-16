# NTR study: The Battery (1993-01..2012-12 train, 2013-01.. test)

Sources: {'enso': 'NOAA ONI (fallback)', 'nao': 'NCEP/NCAR reanalysis SLP, station-style NAO (public)', 'wind': 'NCEP/NCAR reanalysis NY Bight wind from NE (public)'}
Target trend removed (train fit): -0.35 mm/yr

## Lag analysis (prewhitened, train)
- enso: r by lag 0:+0.23, 1:+0.27, 2:+0.11, 3:+0.06, 4:-0.08, 5:-0.07, 6:-0.12; significant lags (all) [0, 1], (cool season) [1]; best any 1, best leading 1
- nao: r by lag 0:-0.14, 1:-0.05, 2:-0.14, 3:-0.05, 4:-0.09, 5:+0.03, 6:-0.01; significant lags (all) none, (cool season) none; best any 2, best leading 2
- wind: r by lag 0:+0.13, 1:+0.17, 2:+0.12, 3:+0.10, 4:-0.00, 5:-0.08, 6:-0.10; significant lags (all) [1], (cool season) [1]; best any 1, best leading 1

## Held-out skill (monthly mean NTR anomaly)
| model | skill vs climatology | RMSE mm | clim RMSE mm | n test |
|---|---:|---:|---:|---:|
| persistence | 0.762 | 38.0 | 77.8 | 166 |
| enso (best lag) | 0.335 | 58.8 | 72.1 | 165 |
| nao (best lag) | -0.023 | 69.1 | 68.3 | 160 |
| wind (best lag) | 0.004 | 67.5 | 67.6 | 159 |
| all concurrent (best lag 0-6) | 0.284 | 57.2 | 67.6 | 159 |
| all leading (lag 1-6, forecast) | 0.284 | 57.2 | 67.6 | 159 |
| all leading + persistence | 0.694 | 37.4 | 67.6 | 159 |

## Cool-season surge days (> 0.12035250684931507 m)
Deviance skill vs trend-only on test: 0.024 (train mean 0.72 days/month)
- enso_lag1: rate ratio per SD 2.23 [1.59, 3.12], p = 2.98e-06
- nao_lag2: rate ratio per SD 1.16 [0.77, 1.76], p = 0.472
- wind_lag1: rate ratio per SD 1.20 [0.87, 1.65], p = 0.271

## Season forecast: August ENSO -> Oct-Apr surge days (quasi-Poisson, trend term)
Train 32 seasons (1980-2011), test 14 (2012-2025); dispersion 6.04
Rate ratio per SD of August ENSO: 2.30 [1.60, 3.31], p = 7.61e-06
Test deviance skill vs trend-only: 0.462
Mean surge days per season: train 5.8, test 4.0
All 46 seasons: RR 2.28 [1.73, 3.00], p = 5.8e-09; leave-one-out RR 2.22-2.54, max p 2.4e-07
Strong El Nino seasons (Aug ENSO >= 1.2 SD): {1982: 25.0, 1987: 2.0, 1997: 23.0, 2015: 18.0, 2023: 10.0}
Outlook 2026-10..2027-04: August ENSO = +2.77 SD -> expected 36.2 surge days [7.1, 186.2] vs trend-only 3.4
