"""Run one New York ntr/ script unchanged, but on the Los Angeles target (westcoast/la/config_ntr.py shadows the
New York config). Usage: python wc_site_run.py prepare|build_ntr|explore_analyze|explore_maps|explore_predictions|
explore_signal_winters|explore_surge_dates|explore_ssh_gibs|model

prepare     fills westcoast/la/data_processed: LA hourly NTR (from wc_fetch.py) and copies of the New York predictor
            tables (same 29 signals, ONI, CPC NAO, public predictors); links the GISTEMP file and the GIBS tile cache.
explore_maps  same script with its BATTERY location moved to the Los Angeles gauge (distances, globe marker).
"""
import os
import runpy
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LA, NTR = HERE / "la", HERE.parent
sys.path[:0] = [str(LA), str(NTR)]
os.chdir(LA)
import config_ntr as C  # noqa: E402  (the LA shim)

assert Path(C.__file__).parent == LA, C.__file__


def prepare():
    C.ensure_dirs()
    import pandas as pd
    h = pd.read_csv(HERE / "data_processed" / f"{C.STATION}_hourly.csv")
    h.to_csv(C.PROCESSED / "ntr_hourly.csv", index=False)          # columns time, ntr_m (what the scripts read)
    for f in ("explore_monthly.csv", "explore_sources.json", "oni.csv", "cpc_nao.csv", "public_predictors.csv"):
        shutil.copy2(NTR / "data_processed" / f, C.PROCESSED / f)
    for name in ("explore", "gibs_ssh"):
        link = C.RAW / name
        if not link.exists():
            os.symlink(f"../../../data_raw/{name}", link)
    print(f"prepare: {len(h)} hourly rows for {C.STATION}; threshold {C.SURGE_THRESHOLD_M:.4f} m", flush=True)


def main(step):
    if step == "prepare":
        return prepare()
    if step == "explore_maps":
        import explore_maps
        explore_maps.BATTERY = C.GAUGE_LATLON
        return explore_maps.main()
    runpy.run_path(str(NTR / f"{step}.py"), run_name="__main__")


if __name__ == "__main__":
    main(sys.argv[1])
