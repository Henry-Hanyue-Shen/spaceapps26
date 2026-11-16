# NTR exploration: The Battery. Train 1981-01..2010-12, test 2011-01.., 29 predictors, FDR 10%

## Monthly: mean NTR, all months
348 predictor x lead tests; 13 discoveries on train; persistence skill 0.719
Same-month (lag 0, reference): oni +0.22, wind_ne_power +0.20, pdo_ncei +0.17, npi_power -0.17, nino34_giss +0.17, msl_montauk +0.16
- CONFIRMED wind_ne_power leads by 1 mo: r_train +0.18, r_test +0.17 (p 0.009), skill alone 0.020, gain over persistence +0.000
- CONFIRMED oni leads by 1 mo: r_train +0.23, r_test +0.23 (p 0.001), skill alone 0.498, gain over persistence +0.012
- CONFIRMED msl_kings_point leads by 11 mo: r_train -0.25, r_test -0.33 (p 0.000), skill alone 0.090, gain over persistence +0.035
- discovered on train but NOT confirmed on test: wind_ne_power@3, nino34_giss@2, msl_montauk@1, msl_kings_point@8, msl_sandy_hook@1, msl_sandy_hook@3, msl_atlantic_city@1, msl_atlantic_city@3, msl_sewells_point@1, msl_sewells_point@3

## Monthly: mean NTR, cool months
348 predictor x lead tests; 16 discoveries on train; persistence skill 0.727
Same-month (lag 0, reference): npi_power -0.26, wind_ne_power +0.25, pna_cpc +0.25, oni +0.22, storminess_power +0.20, msl_montauk +0.19
- CONFIRMED slp_nybight_power leads by 9 mo: r_train +0.22, r_test +0.21 (p 0.019), skill alone 0.086, gain over persistence +0.018
- CONFIRMED natl_giss leads by 9 mo: r_train -0.23, r_test -0.31 (p 0.001), skill alone 0.358, gain over persistence +0.033
- discovered on train but NOT confirmed on test: wind_ne_power@1, wind_ne_power@2, nino34_giss@2, natl_giss@3, natl_giss@5, subpolar_giss@9, oni@1, ao_cpc@9, msl_montauk@1, msl_sandy_hook@1, msl_atlantic_city@1, msl_atlantic_city@3, msl_sewells_point@1, msl_key_west@8

## Monthly: surge days, cool months
348 predictor x lead tests; 0 discoveries on train; persistence skill 0.097
Same-month (lag 0, reference): wind_ne_power +0.23, msl_kings_point +0.21, msl_charleston +0.19, slp_nybight_power -0.18, hudson_flow -0.16, oni +0.15

## Season-ahead: Jul-Sep predictor -> Oct-Apr surge days (quasi-Poisson + trend)
| predictor | RR/SD train | p train | FDR | test skill | LOO skill | RR/SD all | p all |
|---|---:|---:|:-:|---:|---:|---:|---:|
| oni | 2.54 | 0.000 | yes | +0.367 | +0.412 | 2.40 | 0.0000 |
| nino34_giss | 2.61 | 0.000 | yes | +0.498 | +0.409 | 2.45 | 0.0000 |
| natl_giss | 0.37 | 0.008 | yes | -0.205 | +0.161 | 0.44 | 0.0043 |
| trop_natl_giss | 0.48 | 0.030 |  | -0.250 | +0.061 | 0.60 | 0.0326 |
| nwatl_shelf_giss | 0.37 | 0.038 |  | -0.175 | +0.058 | 0.49 | 0.0419 |
| subpolar_giss | 0.70 | 0.143 |  | -0.623 | +0.030 | 0.76 | 0.0745 |
| pdo_ncei | 1.28 | 0.390 |  | +0.263 | +0.030 | 1.43 | 0.0578 |
| msl_sandy_hook | 0.32 | 0.055 |  | +0.021 | +0.028 | 0.37 | 0.0322 |
| msl_montauk | 0.37 | 0.116 |  | +0.067 | +0.024 | 0.43 | 0.0928 |
| msl_boston | 0.34 | 0.154 |  | -0.452 | -0.005 | 0.54 | 0.2817 |
| msl_portland | 0.78 | 0.732 |  | +0.126 | -0.019 | 0.65 | 0.2839 |
| seaice_arctic | 1.14 | 0.578 |  | +0.040 | -0.021 | 1.15 | 0.4377 |
| previous_season_surge | 0.69 | 0.310 |  | -0.026 | -0.024 | 0.75 | 0.2988 |
| msl_sewells_point | 0.84 | 0.740 |  | -0.018 | -0.026 | 0.95 | 0.9057 |
| msl_atlantic_city | 1.05 | 0.939 |  | -0.006 | -0.027 | 1.04 | 0.9404 |
| battery_ntr_summer | 1.22 | 0.409 |  | +0.104 | -0.031 | 1.34 | 0.0796 |
| wind_ne_power | 1.01 | 0.993 |  | +0.001 | -0.044 | 1.13 | 0.7887 |
| nao_power | 1.71 | 0.380 |  | -0.473 | -0.044 | 0.94 | 0.8867 |
| msl_charleston | 1.32 | 0.440 |  | -0.029 | -0.045 | 1.29 | 0.3695 |
| qbo_cpc | 1.14 | 0.587 |  | +0.020 | -0.045 | 1.13 | 0.5167 |
| slp_nybight_power | 1.86 | 0.492 |  | -0.287 | -0.047 | 1.14 | 0.7991 |
| pna_cpc | 1.45 | 0.372 |  | +0.008 | -0.052 | 1.35 | 0.3649 |
| ao_cpc | 1.89 | 0.511 |  | -0.279 | -0.054 | 0.80 | 0.7582 |
| npi_power | 0.18 | 0.039 |  | -0.454 | -0.054 | 0.40 | 0.2163 |
| nao_cpc | 2.80 | 0.031 |  | -2.025 | -0.059 | 1.22 | 0.4940 |
| msl_key_west | 1.29 | 0.479 |  | +0.051 | -0.061 | 1.38 | 0.2820 |
| hudson_flow | 1.19 | 0.823 |  | -0.028 | -0.061 | 0.96 | 0.9302 |
| polar_slp_power | 0.60 | 0.274 |  | -0.282 | -0.070 | 0.88 | 0.7578 |
| msl_bermuda | 0.89 | 0.802 |  | +0.003 | -0.075 | 0.88 | 0.7133 |
| storminess_power | 1.55 | 0.526 |  | +0.017 | -0.090 | 1.49 | 0.4705 |

Added to ENSO (LOO gain, test gain): msl_sandy_hook +0.063/+0.010; msl_montauk +0.050/+0.201; msl_boston +0.034/-0.391; natl_giss +0.034/-0.243; pna_cpc +0.019/+0.170; slp_nybight_power +0.007/-3.606; npi_power +0.001/+0.011; trop_natl_giss +0.000/-0.197

## ENSO lead-time curve (all seasons): month -> RR/SD [CI], p, LOO skill
- oni month  1 (+9 mo before Oct): RR 1.03 [0.76, 1.41], p 0.8310, LOO -0.025
- oni month  2 (+8 mo before Oct): RR 1.06 [0.74, 1.51], p 0.7661, LOO -0.022
- oni month  3 (+7 mo before Oct): RR 1.15 [0.75, 1.78], p 0.5253, LOO -0.014
- oni month  4 (+6 mo before Oct): RR 1.48 [0.89, 2.46], p 0.1285, LOO +0.028
- oni month  5 (+5 mo before Oct): RR 2.43 [1.40, 4.21], p 0.0015, LOO +0.183
- oni month  6 (+4 mo before Oct): RR 3.18 [1.97, 5.13], p 0.0000, LOO +0.335
- oni month  7 (+3 mo before Oct): RR 2.82 [2.00, 3.99], p 0.0000, LOO +0.391
- oni month  8 (+2 mo before Oct): RR 2.35 [1.76, 3.14], p 0.0000, LOO +0.388
- oni month  9 (+1 mo before Oct): RR 2.11 [1.64, 2.71], p 0.0000, LOO +0.427
- oni month 10 (+0 mo before Oct): RR 1.97 [1.58, 2.47], p 0.0000, LOO +0.471
- oni month 11 (-1 mo before Oct): RR 1.94 [1.58, 2.37], p 0.0000, LOO +0.525
- oni month 12 (-2 mo before Oct): RR 1.94 [1.61, 2.34], p 0.0000, LOO +0.570
- nino34_giss month  1 (+9 mo before Oct): RR 1.06 [0.77, 1.47], p 0.7132, LOO -0.021
- nino34_giss month  2 (+8 mo before Oct): RR 1.04 [0.70, 1.55], p 0.8400, LOO -0.022
- nino34_giss month  3 (+7 mo before Oct): RR 1.15 [0.71, 1.86], p 0.5804, LOO -0.014
- nino34_giss month  4 (+6 mo before Oct): RR 1.75 [1.00, 3.07], p 0.0487, LOO +0.066
- nino34_giss month  5 (+5 mo before Oct): RR 2.46 [1.45, 4.17], p 0.0008, LOO +0.191
- nino34_giss month  6 (+4 mo before Oct): RR 3.51 [2.12, 5.80], p 0.0000, LOO +0.369
- nino34_giss month  7 (+3 mo before Oct): RR 2.87 [2.04, 4.03], p 0.0000, LOO +0.402
- nino34_giss month  8 (+2 mo before Oct): RR 2.36 [1.77, 3.13], p 0.0000, LOO +0.390
- nino34_giss month  9 (+1 mo before Oct): RR 2.14 [1.63, 2.82], p 0.0000, LOO +0.400
- nino34_giss month 10 (+0 mo before Oct): RR 2.08 [1.65, 2.61], p 0.0000, LOO +0.498
- nino34_giss month 11 (-1 mo before Oct): RR 1.99 [1.62, 2.45], p 0.0000, LOO +0.535
- nino34_giss month 12 (-2 mo before Oct): RR 2.13 [1.74, 2.60], p 0.0000, LOO +0.615

## Outlook 2026-27 by lead month (expected Oct-Apr surge days [95% CI of the mean]; * = beyond the observed range)
- oni month 5: +1.62 SD (max seen +1.55)* -> 8.7 [3.6, 21.4] vs trend-only 3.4
- oni month 6: +2.15 SD (max seen +1.73)* -> 19.6 [8.0, 48.2] vs trend-only 3.4
- oni month 7: +2.64 SD (max seen +2.03)* -> 25.0 [11.0, 56.8] vs trend-only 3.4
- oni month 8: +3.06 SD (max seen +2.37)* -> 24.7 [10.8, 56.3] vs trend-only 3.4
- oni month 9: +3.43 SD (max seen +2.72)* -> 24.3 [10.8, 54.7] vs trend-only 3.4
- nino34_giss month 5: +1.23 SD (max seen +1.38) -> 7.4 [3.2, 17.4] vs trend-only 3.4
- nino34_giss month 6: +1.85 SD (max seen +1.45)* -> 19.7 [8.0, 48.2] vs trend-only 3.4
- nino34_giss month 7: +2.15 SD (max seen +1.84)* -> 19.1 [8.8, 41.6] vs trend-only 3.4
- nino34_giss month 8: +2.60 SD (max seen +2.16)* -> 21.7 [9.7, 48.4] vs trend-only 3.4
- nino34_giss month 9: +2.87 SD (max seen +2.39)* -> 22.6 [9.6, 52.9] vs trend-only 3.4

## Response by calendar month (August ONI -> surge days in that month)
- month 10: RR 3.31 [1.11, 9.88], p 0.032, mean 0.3 days
- month 11: RR 5.23 [2.29, 11.95], p 0.000, mean 0.4 days
- month 12: RR 3.38 [1.80, 6.34], p 0.000, mean 0.8 days
- month  1: RR 2.21 [1.30, 3.75], p 0.003, mean 1.2 days
- month  2: RR 2.05 [1.33, 3.16], p 0.001, mean 1.8 days
- month  3: RR 1.39 [0.63, 3.04], p 0.416, mean 0.7 days
- month  4: RR 2.51 [0.58, 10.88], p 0.219, mean 0.0 days

## Other gauges (August ONI -> Oct-Apr surge days)
- the_battery: RR 2.35 [1.76, 3.14], p 0.0000, LOO +0.388, test +0.380, mean 5.3 days, n 46
