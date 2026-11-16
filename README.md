# Space Apps 2026: Sea Level Detective

NASA Space Apps Challenge 2026 entry by Team **Poseidon SAR**: Maxim Zyskin, Hanyue Shen, Ningzi Chen.
Challenge: *Be an Earth System Trend Detective*.

**Does the ocean know before the sea rises in New York Harbor?**
Two routes to one warning:

- **Seasonal outlook:** El Niño, read in June, forecasts the October–April storm-surge season in New York Harbor and Los Angeles.
- **14-day forecast:** an equatorial shallow-water model forecasts the Pacific's next two weeks (physics by M. Zyskin).

## Links
- Website: https://ivyreia3-boop.github.io/wbsite/sea-level-detective/
- Slides: https://ivyreia3-boop.github.io/wbsite/sea-level-detective/slides.html
- 30-second video: https://ivyreia3-boop.github.io/wbsite/sea-level-detective/video30.html
- 1-minute video: https://ivyreia3-boop.github.io/wbsite/sea-level-detective/video.html

## Headline results
- New York: June Niño-3.4 raises storm-surge days ×1.64 per standard deviation (p < 0.0001). Strong El Niño winters bring 16 days against 10 in an average winter. Leave-one-winter-out error is 3.8 days per winter, against 4.6 for a trend-only model.
- Los Angeles: ×3.5 high-water days per standard deviation.
- 2026–27 outlook for New York: about 21 storm-surge days (likely 14–32), about twice normal.
- 14-day Pacific forecast: 12.3% lower sea-height error than persistence (95% CI 10.3–14.3%), with 168 of 182 forecasts better than persistence. Surface currents improve by 9.4%.

## What is here (`sea-level-detective/`)
| Folder | Contents |
|---|---|
| `site/` | The interactive website: 3D globe, East/West coast switch, charts; slides and video pages. Static files, so any web server works. |
| `deck/` | Slides (PDF, PPTX, slide PNGs), the figure scripts (`figs/`) and the print source (`print/`). |
| `ntr/` | Storm-surge study: NOAA tide-gauge records, 29 NASA/NOAA predictors, the false-discovery-rate screen, quasi-Poisson count models, and the East and West Coast results. |
| `pipeline/` | Sea-level trend explorer: least squares with Fourier terms, AR(1)-corrected error bars, tests, and the site export. |
| `handoff/` | Data handoff workbook with a CSV copy of every sheet. |
| `summary/` | Project summary and the list of verified facts. |
| `argument_tree/`, `narrative/`, `experiment_plan/` | Claim tree, story map and experiment plan (LaTeX + PDF). |

## Data used
| Dataset | Link |
|---|---|
| NASA MEaSUREs Gridded Sea Surface Height Anomalies | https://podaac.jpl.nasa.gov/dataset/SEA_SURFACE_HEIGHT_ALT_GRIDS_L4_2SATS_5DAY_6THDEG_V_JPL1812 |
| NASA-SSH Sea Surface Height Anomalies | https://doi.org/10.5067/NSREF-SG0V1 |
| NASA GISTEMP v4 | https://data.giss.nasa.gov/gistemp/ |
| NASA POWER (MERRA-2) | https://power.larc.nasa.gov/ |
| NASA GEOS-FP winds | https://gmao.gsfc.nasa.gov/GMAO_products/NRT_products.php |
| OSCAR V2 surface currents | https://podaac.jpl.nasa.gov/dataset/OSCAR_L4_OC_FINAL_V2.0 |
| NASA GIBS imagery | https://gibs.earthdata.nasa.gov/wmts/epsg3857/best |
| GHRSST MUR 0.25° SST | https://podaac.jpl.nasa.gov/dataset/MUR25-JPL-L4-GLOB-v04.2 |
| VIIRS SNPP true colour | https://worldview.earthdata.nasa.gov/?l=VIIRS_SNPP_CorrectedReflectance_TrueColor |
| NOAA CO-OPS: The Battery (8518750) | https://tidesandcurrents.noaa.gov/stationhome.html?id=8518750 |
| NOAA CO-OPS: Los Angeles (9410660) | https://tidesandcurrents.noaa.gov/stationhome.html?id=9410660 |
| NOAA CPC Oceanic Niño Index | https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php |
| NOAA CPC teleconnection indices | https://www.cpc.ncep.noaa.gov/data/teledoc/telecontents.shtml |
| NOAA NCEI PDO | https://www.ncei.noaa.gov/access/monitoring/pdo/ |
| NSIDC Sea Ice Index v4 | https://nsidc.org/data/g02135 |
| USGS 01358000 Hudson River | https://waterdata.usgs.gov/monitoring-location/USGS-01358000/ |

## Running it
- Website: serve `sea-level-detective/site/` with any static server (for example `python -m http.server`), then open `index.html`.
- Pipeline: see `sea-level-detective/README.md`. NASA downloads need a free Earthdata token; keep it in an environment variable only.
