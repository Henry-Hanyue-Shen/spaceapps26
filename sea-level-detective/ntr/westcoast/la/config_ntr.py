"""Los Angeles stand-in for ntr/config_ntr.py, so the New York scripts run unchanged on the West Coast target.

Everything is taken from the New York config except the paths (this folder) and the target:
  STATION            9410660, Los Angeles (NOAA CO-OPS)
  SURGE_THRESHOLD_M  the 98th percentile of LA's daily-mean NTR minus its 365-day centred running mean over the train
                     days 1981-2010 (0.120 m, from westcoast/results/wc_results.json), so a "surge day" in the
                     New York scripts is a "high-water day" at Los Angeles.
Put this folder first on sys.path (wc_site_run.py does that).
"""
import importlib.util
import json
from pathlib import Path

_ny_path = Path(__file__).resolve().parents[2] / "config_ntr.py"
_spec = importlib.util.spec_from_file_location("_config_ntr_ny", _ny_path)
_ny = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ny)
for _k in dir(_ny):
    if _k.isupper():
        globals()[_k] = getattr(_ny, _k)

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data_raw"
PROCESSED = ROOT / "data_processed"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
STATION = "9410660"
SURGE_THRESHOLD_M = float(json.loads((ROOT.parent / "results" / "wc_results.json").read_text())
                          ["stations"]["los_angeles"]["p98_resid_m"])
GAUGE_LATLON = (33.72, -118.27)   # Los Angeles 9410660 (NOAA station metadata 33.720, -118.272)


def ensure_dirs():
    for p in (RAW, PROCESSED, RESULTS, FIGURES):
        p.mkdir(parents=True, exist_ok=True)
