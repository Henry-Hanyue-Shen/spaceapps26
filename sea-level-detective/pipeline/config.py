"""Fixed analysis choices. Sea-level inputs to statistics are millimetres."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data_raw"
PROCESSED = ROOT / "data_processed"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))
os.environ.setdefault("MPLBACKEND", "Agg")

# (south, north, west, east), degrees; longitude is normalized to [-180, 180).
BOXES = {
    "global": (-66, 66, -180, 180),
    "west_pacific": (-5, 5, 120, 160),
    "east_pacific": (-5, 5, -150, -90),
    "california_shelf": (32, 38, -124, -117),
    "ny_bight": (39.5, 41, -74.5, -71.5),
    # Gulf Stream strength proxy (NTR study): SSH south of the stream minus SSH in the Slope Sea, 72-68W.
    "gs_south": (36, 37.5, -72, -68),
    "gs_north": (39, 40.5, -72, -68),
}
GAUGES = {
    "8518750": {"name": "The Battery", "box": "ny_bight"},
    "9410230": {"name": "La Jolla", "box": "california_shelf"},
    "9414290": {"name": "San Francisco", "box": "california_shelf"},
}
NASA_COLLECTIONS = {
    "gmsl": "NASA_SSH_GMSL_INDICATOR",
    "enso": "NASA_SSH_ENSO_INDICATOR",
    "pdo": "NASA_SSH_PDO_INDICATOR",
    "grid": "NASA_SSH_REF_SIMPLE_GRID_V1",
}
NOAA_API = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
ENSO_LAG = 0  # Positive lag: sea level responds this many months after the index.
SEED = 20261114
MC_REPLICATES = 1000
MC_LENGTHS = (10, 15, 20, 25, 30, 35)
MC_TRENDS = (0, 1, 2, 3, 4)
ALPHA = 0.05
PERMUTATIONS = 9999
PEAK_WINDOWS = {"1997/98": ("1997-01", "1998-12"),
                "2015/16": ("2015-01", "2016-12")}


def ensure_dirs():
    """Create output directories only beneath this pipeline folder."""
    for path in (RAW / "noaa", RAW / "nasa", PROCESSED, RESULTS, FIGURES):
        path.mkdir(parents=True, exist_ok=True)
