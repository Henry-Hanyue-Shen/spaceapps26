# NTR study: The Battery (1993-01..2012-12 train, 2013-01.. test)

Sources: {'enso': 'NOAA ONI (fallback)', 'nao': 'NCEP/NCAR reanalysis SLP, station-style NAO (public)', 'wind': 'NCEP/NCAR reanalysis NY Bight wind from NE (public)'}
Target trend removed (train fit): 5.13 mm/yr

## Lag analysis (prewhitened, train)
- enso: r by lag 0:+0.07, 1:+0.01, 2:+0.00, 3:+0.02, 4:+0.02, 5:-0.01, 6:-0.01; significant lags (all) none, (cool season) none; best any 0, best leading 3
- nao: r by lag 0:-0.21, 1:-0.08, 2:-0.10, 3:-0.05, 4:-0.05, 5:-0.02, 6:+0.04; significant lags (all) [0], (cool season) none; best any 0, best leading 2
- wind: r by lag 0:+0.47, 1:+0.11, 2:+0.08, 3:+0.12, 4:+0.09, 5:+0.09, 6:-0.06; significant lags (all) [0], (cool season) [0]; best any 0, best leading 3

## Held-out skill (monthly mean NTR anomaly)
| model | skill vs climatology | RMSE mm | clim RMSE mm | n test |
|---|---:|---:|---:|---:|
| persistence | 0.145 | 60.0 | 64.9 | 166 |
| enso (best lag) | 0.002 | 65.0 | 65.1 | 165 |
| nao (best lag) | 0.087 | 62.0 | 64.9 | 158 |
| wind (best lag) | 0.257 | 55.9 | 64.9 | 158 |
| all concurrent (best lag 0-6) | 0.316 | 53.6 | 64.9 | 158 |
| all leading (lag 1-6, forecast) | -0.016 | 65.5 | 65.0 | 160 |
| all leading + persistence | 0.131 | 60.6 | 65.0 | 160 |

## Cool-season surge days (> 0.3 m)
Deviance skill vs trend-only on test: 0.235 (train mean 1.37 days/month)
- enso_lag0: rate ratio per SD 1.11 [0.93, 1.32], p = 0.244
- nao_lag0: rate ratio per SD 0.77 [0.64, 0.93], p = 0.00611
- wind_lag0: rate ratio per SD 1.16 [0.97, 1.39], p = 0.114

## Season forecast: August ENSO -> Oct-Apr surge days (quasi-Poisson, trend term)
Train 29 seasons (1980-2011), test 14 (2012-2025); dispersion 2.49
Rate ratio per SD of August ENSO: 1.44 [1.13, 1.82], p = 0.00259
Test deviance skill vs trend-only: 0.248
Mean surge days per season: train 10.2, test 10.6
All 43 seasons: RR 1.38 [1.18, 1.63], p = 8.5e-05; leave-one-out RR 1.35-1.46, max p 0.00061
Strong El Nino seasons (Aug ENSO >= 1.2 SD): {1982: 19.0, 1987: 10.0, 2015: 16.0, 2023: 20.0}
Outlook 2026-10..2027-04: August ENSO = +2.77 SD -> expected 29.9 surge days [11.3, 79.2] vs trend-only 9.2
