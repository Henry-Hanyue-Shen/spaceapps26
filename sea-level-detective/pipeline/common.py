"""Small shared IO helpers; JSON never contains nonstandard NaN literals."""
import json
import math
import numpy as np
import pandas as pd
from config import PROCESSED, RESULTS, ensure_dirs


def clean_json(value):
    if isinstance(value, dict):
        return {str(k): clean_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [clean_json(v) for v in value]
    if isinstance(value, np.generic):
        return clean_json(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, (pd.Timestamp, pd.Period)):
        return str(value)
    return value


def save_json(name, value):
    ensure_dirs()
    (RESULTS / name).write_text(json.dumps(clean_json(value), indent=2,
                                         allow_nan=False) + "\n", encoding="utf-8")
    return value


def read_monthly(name):
    """Read a tidy CSV with a date column, retaining missing calendar months."""
    frame = pd.read_csv(PROCESSED / name, parse_dates=["date"]).set_index("date")
    return frame.sort_index().resample("MS").mean(numeric_only=True)


def metadata(series):
    """Observed window and count, excluding missing values."""
    series = series.dropna()
    return {"window": [str(series.index.min().date()), str(series.index.max().date())]
            if len(series) else None, "n": len(series)}
