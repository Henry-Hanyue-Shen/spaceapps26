# NTR exploration: The Battery. Train 1981-01..2010-12, test 2011-01.., 29 predictors, FDR 10%

## Monthly: mean NTR, all months
348 predictor x lead tests; 9 discoveries on train; persistence skill 0.156
Same-month (lag 0, reference): msl_sandy_hook +0.98, msl_atlantic_city +0.93, msl_montauk +0.93, msl_kings_point +0.92, msl_sewells_point +0.87, msl_boston +0.83
- CONFIRMED msl_portland leads by 1 mo: r_train -0.20, r_test -0.13 (p 0.032), skill alone 0.119, gain over persistence +0.001
- discovered on train but NOT confirmed on test: wind_ne_power@3, storminess_power@11, msl_bermuda@1, msl_portland@2, msl_montauk@3, msl_sandy_hook@3, msl_atlantic_city@3, msl_sewells_point@3

## Monthly: mean NTR, cool months
348 predictor x lead tests; 19 discoveries on train; persistence skill 0.119
Same-month (lag 0, reference): msl_sandy_hook +0.98, msl_atlantic_city +0.94, msl_montauk +0.93, msl_kings_point +0.93, msl_sewells_point +0.89, msl_boston +0.83
- discovered on train but NOT confirmed on test: polar_slp_power@8, wind_ne_power@2, wind_ne_power@3, ao_cpc@8, msl_portland@2, msl_boston@2, msl_boston@3, msl_montauk@2, msl_montauk@3, msl_montauk@5, msl_sandy_hook@2, msl_sandy_hook@3, msl_sandy_hook@5, msl_atlantic_city@2, msl_atlantic_city@3, msl_atlantic_city@5, msl_sewells_point@2, msl_sewells_point@3, nao_power@8

## Monthly: surge days, cool months
348 predictor x lead tests; 0 discoveries on train; persistence skill 0.004
Same-month (lag 0, reference): msl_sandy_hook +0.51, msl_montauk +0.50, msl_atlantic_city +0.45, msl_boston +0.44, msl_kings_point +0.41, msl_portland +0.41

## Season-ahead: Jul-Sep predictor -> Oct-Apr surge days (quasi-Poisson + trend)
| predictor | RR/SD train | p train | FDR | test skill | LOO skill | RR/SD all | p all |
|---|---:|---:|:-:|---:|---:|---:|---:|
| oni | 1.46 | 0.005 | yes | +0.208 | +0.243 | 1.40 | 0.0001 |
| nino34_giss | 1.39 | 0.012 | yes | +0.349 | +0.223 | 1.39 | 0.0001 |
| pdo_ncei | 1.44 | 0.003 | yes | -0.762 | +0.065 | 1.19 | 0.0273 |
| msl_atlantic_city | 1.81 | 0.046 |  | -0.548 | +0.024 | 1.37 | 0.1104 |
| msl_portland | 1.88 | 0.006 | yes | -2.542 | +0.013 | 1.29 | 0.1038 |
| msl_charleston | 1.23 | 0.207 |  | -0.099 | +0.007 | 1.17 | 0.2250 |
| nao_power | 1.07 | 0.774 |  | -0.124 | -0.004 | 0.81 | 0.1864 |
| msl_boston | 1.42 | 0.171 |  | +0.192 | -0.007 | 1.33 | 0.1509 |
| polar_slp_power | 1.14 | 0.547 |  | +0.069 | -0.018 | 1.21 | 0.2403 |
| msl_montauk | 1.45 | 0.174 |  | -0.132 | -0.019 | 1.24 | 0.2877 |
| msl_key_west | 1.06 | 0.690 |  | +0.007 | -0.022 | 1.07 | 0.5608 |
| nao_cpc | 1.14 | 0.514 |  | -0.309 | -0.028 | 0.90 | 0.3602 |
| msl_sewells_point | 1.22 | 0.370 |  | -0.072 | -0.028 | 1.13 | 0.4653 |
| battery_ntr_summer | 1.20 | 0.088 |  | -0.447 | -0.029 | 1.08 | 0.3147 |
| qbo_cpc | 1.10 | 0.328 |  | -0.023 | -0.029 | 1.06 | 0.4170 |
| pna_cpc | 1.27 | 0.203 |  | -0.112 | -0.030 | 1.15 | 0.3207 |
| wind_ne_power | 1.32 | 0.307 |  | -0.044 | -0.031 | 1.21 | 0.3143 |
| previous_season_surge | 1.04 | 0.743 |  | -0.120 | -0.032 | 0.92 | 0.3130 |
| slp_nybight_power | 1.29 | 0.498 |  | -0.359 | -0.034 | 0.87 | 0.4934 |
| seaice_arctic | 0.97 | 0.725 |  | +0.021 | -0.037 | 0.96 | 0.5133 |
| natl_giss | 0.83 | 0.193 |  | -0.207 | -0.040 | 0.91 | 0.4129 |
| hudson_flow | 1.02 | 0.946 |  | -0.008 | -0.042 | 0.92 | 0.6124 |
| ao_cpc | 1.00 | 0.995 |  | -0.001 | -0.043 | 0.81 | 0.4686 |
| trop_natl_giss | 0.96 | 0.799 |  | -0.025 | -0.045 | 0.99 | 0.9545 |
| msl_sandy_hook | 1.54 | 0.109 |  | -0.405 | -0.046 | 1.19 | 0.3957 |
| nwatl_shelf_giss | 0.97 | 0.879 |  | +0.020 | -0.047 | 0.90 | 0.5028 |
| subpolar_giss | 0.87 | 0.151 |  | -0.839 | -0.054 | 0.99 | 0.8259 |
| npi_power | 1.00 | 0.996 |  | +0.000 | -0.058 | 0.93 | 0.8272 |
| storminess_power | 0.92 | 0.763 |  | -0.014 | -0.072 | 0.95 | 0.8223 |
| msl_bermuda | 0.79 | 0.210 |  | -0.315 | -0.075 | 0.97 | 0.8651 |

Added to ENSO (LOO gain, test gain): pna_cpc +0.050/+0.138; msl_portland +0.045/-2.119; msl_charleston +0.021/-0.471; msl_boston +0.009/-0.043; msl_atlantic_city +0.008/-0.618; slp_nybight_power -0.010/-0.144; msl_montauk -0.014/-0.353; msl_key_west -0.014/-0.077

## ENSO lead-time curve (all seasons): month -> RR/SD [CI], p, LOO skill
- oni month  1 (+9 mo before Oct): RR 1.01 [0.89, 1.15], p 0.9054, LOO -0.064
- oni month  2 (+8 mo before Oct): RR 1.02 [0.88, 1.19], p 0.7484, LOO -0.062
- oni month  3 (+7 mo before Oct): RR 1.07 [0.89, 1.28], p 0.4750, LOO -0.045
- oni month  4 (+6 mo before Oct): RR 1.19 [0.96, 1.48], p 0.1131, LOO +0.014
- oni month  5 (+5 mo before Oct): RR 1.43 [1.14, 1.81], p 0.0025, LOO +0.165
- oni month  6 (+4 mo before Oct): RR 1.59 [1.27, 1.98], p 0.0000, LOO +0.266
- oni month  7 (+3 mo before Oct): RR 1.53 [1.26, 1.85], p 0.0000, LOO +0.271
- oni month  8 (+2 mo before Oct): RR 1.40 [1.18, 1.66], p 0.0001, LOO +0.232
- oni month  9 (+1 mo before Oct): RR 1.31 [1.13, 1.51], p 0.0003, LOO +0.217
- oni month 10 (+0 mo before Oct): RR 1.25 [1.10, 1.41], p 0.0005, LOO +0.203
- oni month 11 (-1 mo before Oct): RR 1.22 [1.09, 1.36], p 0.0006, LOO +0.199
- oni month 12 (-2 mo before Oct): RR 1.21 [1.09, 1.34], p 0.0004, LOO +0.207
- nino34_giss month  1 (+9 mo before Oct): RR 1.02 [0.89, 1.17], p 0.7520, LOO -0.056
- nino34_giss month  2 (+8 mo before Oct): RR 1.05 [0.88, 1.24], p 0.6068, LOO -0.048
- nino34_giss month  3 (+7 mo before Oct): RR 1.10 [0.90, 1.35], p 0.3593, LOO -0.029
- nino34_giss month  4 (+6 mo before Oct): RR 1.27 [1.00, 1.62], p 0.0481, LOO +0.057
- nino34_giss month  5 (+5 mo before Oct): RR 1.49 [1.18, 1.88], p 0.0007, LOO +0.202
- nino34_giss month  6 (+4 mo before Oct): RR 1.64 [1.31, 2.04], p 0.0000, LOO +0.303
- nino34_giss month  7 (+3 mo before Oct): RR 1.50 [1.23, 1.82], p 0.0001, LOO +0.250
- nino34_giss month  8 (+2 mo before Oct): RR 1.37 [1.16, 1.61], p 0.0002, LOO +0.211
- nino34_giss month  9 (+1 mo before Oct): RR 1.30 [1.12, 1.52], p 0.0006, LOO +0.193
- nino34_giss month 10 (+0 mo before Oct): RR 1.26 [1.10, 1.43], p 0.0005, LOO +0.198
- nino34_giss month 11 (-1 mo before Oct): RR 1.22 [1.09, 1.37], p 0.0005, LOO +0.197
- nino34_giss month 12 (-2 mo before Oct): RR 1.23 [1.10, 1.37], p 0.0002, LOO +0.228

## Outlook 2026-27 by lead month (expected Oct-Apr surge days [95% CI of the mean]; * = beyond the observed range)
- oni month 5: +1.62 SD (max seen +1.55)* -> 14.9 [10.2, 21.8] vs trend-only 10.2
- oni month 6: +2.15 SD (max seen +1.73)* -> 21.2 [13.8, 32.6] vs trend-only 10.2
- oni month 7: +2.64 SD (max seen +2.03)* -> 24.5 [15.5, 38.9] vs trend-only 10.2
- oni month 8: +3.06 SD (max seen +2.37)* -> 24.0 [14.7, 39.2] vs trend-only 10.2
- oni month 9: +3.43 SD (max seen +2.72)* -> 22.3 [13.7, 36.4] vs trend-only 10.2
- nino34_giss month 5: +1.23 SD (max seen +1.38) -> 14.5 [10.2, 20.6] vs trend-only 10.2
- nino34_giss month 6: +1.85 SD (max seen +1.45)* -> 21.0 [13.9, 31.8] vs trend-only 10.2
- nino34_giss month 7: +2.15 SD (max seen +1.76)* -> 21.2 [13.6, 32.8] vs trend-only 10.2
- nino34_giss month 8: +2.60 SD (max seen +2.16)* -> 21.8 [13.5, 35.2] vs trend-only 10.2
- nino34_giss month 9: +2.87 SD (max seen +2.39)* -> 21.4 [13.1, 35.1] vs trend-only 10.2

## Response by calendar month (August ONI -> surge days in that month)
- month 10: RR 1.28 [0.87, 1.88], p 0.208, mean 1.3 days
- month 11: RR 1.42 [0.88, 2.29], p 0.151, mean 0.9 days
- month 12: RR 1.19 [0.84, 1.69], p 0.325, mean 1.6 days
- month  1: RR 1.24 [0.89, 1.73], p 0.200, mean 1.7 days
- month  2: RR 1.45 [1.07, 1.98], p 0.018, mean 1.7 days
- month  3: RR 1.33 [0.84, 2.11], p 0.223, mean 1.7 days
- month  4: RR 1.31 [0.87, 1.97], p 0.204, mean 1.1 days

## Other gauges (August ONI -> Oct-Apr surge days)
- the_battery: RR 1.40 [1.18, 1.66], p 0.0001, LOO +0.232, test +0.230, mean 10.3 days, n 43
