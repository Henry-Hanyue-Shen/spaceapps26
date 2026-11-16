# Sea Level Detective — NASA Space Apps 2026

Challenge: **Be An Earth System Trend Detective!** Pick a place, and the tool tells you how fast sea level is really
changing there, whether the trend is statistically significant, and how much of the change is El Niño.

## Folders
| Folder | What |
|---|---|
| `argument_tree/` | Literature-grounded claim tree (PDF, 23 verified references + our own numbers) |
| `narrative/` | One-page story map (PDF) |
| `experiment_plan/` | Experiments E0–E8 and the NASA dataset table (PDF) |
| `pipeline/` | Python pipeline: download, data standard (`DATA_STANDARD.md`), statistics, experiments, site export |
| `site/` | Static website (open `site/index.html` through any web server; GitHub Pages ready) |
| `docs_nasa/` | NASA-SSH user guides (public PDFs) |
| `archive_planned_v1/` | First, plan-only version of the tree and narrative |

## Run
```
cd pipeline
..\.venv\Scripts\python.exe -m unittest            # 29 tests
..\.venv\Scripts\python.exe run_all.py --no-nasa   # NOAA gauges + ONI, E1, E4 gauges, standard files, site data
```
With NASA data (needs a free Earthdata login: https://urs.earthdata.nasa.gov → Generate Token):
```
$env:EARTHDATA_TOKEN = "<your token>"   # set in the shell only; never write it into a file
..\.venv\Scripts\python.exe run_all.py            # downloads ~1,700 NASA-SSH weekly grids (~2 GB) + indicators
```
Then check `node site/tests/check_stats.mjs` (browser statistics = Python statistics).

## NY Harbor NTR study (`ntr/`, runs on the DGX)
```
bash ntr/run_ntr_dgx.sh noaa    # NOAA only: Battery NTR, ONI, CPC NAO
bash ntr/run_ntr_dgx.sh nasa    # + MERRA-2 NAO and wind (needs ~/.earthdata_token on the DGX)
```
Results are in `ntr/results/ntr_summary.md`. The headline: August El Niño predicts October–April surge days at the
Battery, +38% per SD [+18%, +63%] over 43 winters, with +25% held-out skill over the trend alone.

## Status (2026-11-14 19:40 UTC)
- Done:
  - pipeline and data standard;
  - E1: only AR(1)-adjusted OLS keeps false alarms near 5%;
  - E4 gauges: about 4 cm per °C of ONI in California; New York not significant;
  - the website explorer working on the 3 tide gauges.
- Waiting for an Earthdata token: E0, E2, E3 and the satellite part of E4. Once the token is set, the NASA regions
  appear in the site's "Place" menu automatically.
