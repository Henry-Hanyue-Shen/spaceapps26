# Project summary rewrite: original text and verified facts

## Original summary (the user's draft)

In this research, we study how ocean data can be used to predict water levels in advance and provide useful warning for important coastal regions, exemplified by New York Harbor and the Los Angeles area. We combine two complementary approaches.

First, using NASA and NOAA observations, tide-gauge records, climate indices, winds, pressure and satellite sea-surface-height data, we show that information from remote parts of the ocean can improve regression-based prediction beyond using only the local water-level record. After removing tides and modelling trends and seasonal cycles with least squares and Fourier terms, we screen candidate predictors and test them on unseen winters. In particular, tropical-Pacific El Niño conditions measured months earlier provide useful information about subsequent winter high-water risk on both U.S. coasts.

Second, we use ocean physics for finer-scale, short-range prediction. NASA altimetry, GEOS-FP winds and OSCAR surface currents are incorporated into a nonlinear shallow-water dynamical model. On an extended 2023–2026 dataset, chronologically validated 14-day forecasts reduce sea-surface-height error by about 12% relative to persistence, with 92% of forecasts outperforming it.

Together, the project links global Earth observations, statistical learning and physical ocean modelling to provide both seasonal early warning and 14-day dynamical prediction.

## Addition requested by the user
Mention the interactive webpage hosted on GitHub (https://ivyreia3-boop.github.io/wbsite/sea-level-detective/).
What is true: it is an interactive site (3D globe with an East/West coast switch, "Test a winter" replay, charts). It loads NASA GIBS satellite imagery live in the browser. The statistical results and forecasts on it are precomputed from records through October 2026 (data generated 2026-11-15); it is not a live forecasting service. Do NOT call the data "real-time"; "live NASA satellite imagery" is accurate.

## Verified facts (use these numbers exactly; do not invent others)

Seasonal (statistics, our part):
- New York: storm-surge days at the Battery tide gauge (NOAA 8518750) = daily mean water level, tide removed, more than 0.30 m above its 365-day running mean; counted per October–April winter, 1980–2025.
- Los Angeles (NOAA 9410660): high-water days = top 2% of days (0.12 m above the running yearly mean).
- 29 NASA and NOAA clues (30 candidate predictors with last winter's own count) — sea height, temperature, winds, pressure, sea ice, river flow — each read in every month.
- Evidence selection: Benjamini–Hochberg false-discovery rate 10% on 1981–2010; 4 passed; 2 also predicted 2011–2025 and every left-out winter; both are El Niño (NOAA ONI and NASA GISTEMP Niño-3.4). Last winter's own count (the local record) did not help.
- Model: quasi-Poisson count model, winter days ~ time trend + clue read in month m.
- June Niño-3.4: ×1.64 storm-surge days per standard deviation in New York (p < 0.0001); ×3.5 high-water days per SD in Los Angeles. Read four months before the season.
- New York: strong El Niño winters bring 16 storm-surge days; an average winter brings 10. Average error per winter 3.8 days vs 4.6 for a trend-only model (leave-one-winter-out).
- NASA altimetry: June sea height in the Niño-3.4 box correlates with New York's winter at r = 0.43 (1993–2018).
- 2026–27 outlook for New York: about 21 storm-surge days (likely 14–32), about twice normal.
- Least squares with Fourier features (annual + semiannual harmonics) and AR(1)-corrected uncertainty are used for the sea-level trend analysis on the site; in simulation, plain least squares flags a false trend in 41% of 10-year records, the corrected test in 7%.
- Month to month, local winds and the North Atlantic pressure pattern explain 32% of New York Harbor's mean water level; remote clues add nothing one month ahead. The remote ocean's value is at the seasonal horizon.
- The baseline El Niño beats is a trend-only model (not "the local water-level record" in general).
- West Coast beyond LA: San Francisco shows the El Niño link only in mean winter sea level; Seattle has no useful skill. "Both coasts" = New York and Southern California (Los Angeles).

Physics (M. Zyskin's part, from his slides):
- Equatorial shallow-water model; NASA sea height shows Kelvin-like eastward propagation at +1.50–1.62 m/s (2015–16 El Niño) and Rossby-like westward propagation at −0.68–0.78 m/s (2026 check).
- Residual nonlinear shallow-water forecast: only the dynamical correction to the observed background is forecast, so persistence is the exact reference.
- Data: NASA SSH V1.1 + OSCAR V2 surface currents; 201 weekly states 2023–2026; 182 rolling, chronologically validated 14-day forecasts; domain 170°W–100°W, 10°S–10°N. The headline test uses NO future wind forcing (GEOS-FP winds appear in the observations and in the earlier parameter search via a wind-coupling depth).
- Results: hybrid 14-day forecast has 12.3% lower sea-height RMSE than persistence (95% block-bootstrap CI +10.3% to +14.3%); 168 of 182 forecasts (92%) beat persistence; 14-day surface-current skill +9.4%.

Team: Poseidon SAR (Maxim Zyskin, Hanyue Shen, Ningzi Chen), NASA Space Apps 2026.
