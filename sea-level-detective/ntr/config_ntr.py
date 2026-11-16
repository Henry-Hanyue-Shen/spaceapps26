"""Fixed choices for the NY Harbor non-tidal residual (NTR) study. Set before looking at results."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data_raw"
PROCESSED = ROOT / "data_processed"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PIPELINE_PROCESSED = ROOT.parent / "pipeline" / "data_processed"   # NASA box series (incl. Gulf Stream boxes)

STATION = "8518750"                 # The Battery, NY
FIRST_YEAR, LAST_YEAR = 1980, 2026
SURGE_THRESHOLD_M = 0.30            # daily max NTR above this = a "surge day"
MIN_HOURS_FRACTION = 0.80           # a month needs >= 80% of its hours to count
TRAIN = ("1993-01", "2012-12")      # fit period (common NASA coverage starts 1993)
TEST = ("2013-01", "2026-12")       # held-out evaluation
MAX_LAG = 6                         # months; predictor leads NTR by 0..MAX_LAG
COOL_MONTHS = (10, 11, 12, 1, 2, 3, 4)

NOAA_API = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
CPC_NAO_URL = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii"

# MERRA-2 (NASA GMAO) monthly single-level diagnostics, read with an Earthdata login.
MERRA2 = "M2TMNXSLV"
NAO_POINTS = {"iceland": (65.08, -22.73), "azores": (37.74, -25.68)}   # Stykkisholmur, Ponta Delgada
NY_BIGHT_BOX = (39.5, 41.0, -74.5, -71.5)   # (south, north, west, east)
# Wind "from the northeast" pushes water toward the harbor; positive = wind blowing toward 225 deg (SW).
WIND_FROM_NE = (-0.70710678, -0.70710678)   # unit vector toward the SW, applied to (u, v)


def ensure_dirs():
    for p in (RAW, PROCESSED, RESULTS, FIGURES):
        p.mkdir(parents=True, exist_ok=True)
