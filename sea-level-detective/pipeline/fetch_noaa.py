"""Download public NOAA monthly gauge records and ONI; no authentication."""
import io
import json
from datetime import date
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import GAUGES, NOAA_API, ONI_URL, RAW, PROCESSED, ensure_dirs
from common import save_json, metadata


class NetworkUnavailable(RuntimeError):
    """The public NOAA endpoint could not be reached."""


def session():
    client = requests.Session()
    client.headers["User-Agent"] = "SeaLevelDetective/1.0"
    retries = Retry(total=2, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    client.mount("https://", HTTPAdapter(max_retries=retries))
    return client


def get(client, url, **kwargs):
    try:
        response = client.get(url, timeout=(15, 60), **kwargs)
        response.raise_for_status()
        return response
    except requests.RequestException as exc:
        raise NetworkUnavailable(f"NOAA request failed at {url}: {exc}") from exc


def windows(first_year=1800, today=None):
    """Inclusive windows <=10 calendar years, through the last complete month.

    1800 predates all three stations' records, so initial empty windows are
    expected. No assumed station start date can truncate the downloaded record.
    """
    today = today or date.today()
    end = pd.Timestamp(today).replace(day=1) - pd.Timedelta(days=1)
    for year in range(first_year, end.year+1, 10):
        start = pd.Timestamp(year, 1, 1)
        stop = min(pd.Timestamp(year+9, 12, 31), end)
        yield start, stop


def parse_gauge(payload):
    """CO-OPS monthly MSL (metres) -> mm; retain provider QA fields in raw JSON."""
    if "error" in payload:
        message = str(payload["error"].get("message", payload["error"]))
        if "no data" in message.lower():
            return pd.Series(dtype=float, index=pd.DatetimeIndex([], name="date"), name="level_mm")
        raise ValueError(f"NOAA API error: {message}")
    rows = payload.get("data")
    if rows is None:
        raise ValueError("NOAA monthly response is missing its data array")
    dates, values = [], []
    for row in rows:
        lower = {key.lower(): value for key, value in row.items()}
        if not {"year", "month", "msl"} <= lower.keys():
            raise ValueError(f"Unexpected NOAA monthly fields: {list(row)}")
        dates.append(pd.Timestamp(int(lower["year"]), int(lower["month"]), 1))
        value = pd.to_numeric(lower["msl"], errors="coerce")
        values.append(float(value)*1000 if pd.notna(value) and abs(float(value)) < 99 else float("nan"))
    return pd.Series(values, index=pd.DatetimeIndex(dates, name="date"), name="level_mm")


def parse_oni(text):
    """Map each three-month ONI season to its central month; values are degrees C."""
    frame = pd.read_csv(io.StringIO(text), sep=r"\s+")
    required = {"SEAS", "YR", "ANOM"}
    if not required <= set(frame.columns):
        raise ValueError(f"Unrecognized ONI header: {list(frame.columns)}")
    seasons = "DJF JFM FMA MAM AMJ MJJ JJA JAS ASO SON OND NDJ".split()
    months = frame.SEAS.map({name: i+1 for i, name in enumerate(seasons)})
    if months.isna().any():
        raise ValueError("Unrecognized ONI season")
    dates = pd.to_datetime(dict(year=frame.YR, month=months, day=1))
    values = pd.to_numeric(frame.ANOM, errors="coerce").where(lambda x: x.abs() < 90)
    return pd.Series(values.to_numpy(), index=pd.DatetimeIndex(dates, name="date"), name="oni_c").sort_index()


def main():
    ensure_dirs()
    client, report = session(), {"datum": "MSL", "units": "mm", "gauges": {}}
    for station, info in GAUGES.items():
        parts = []
        print(f"NOAA: {info['name']} ({station}), full monthly record", flush=True)
        for start, end in windows():
            path = RAW / "noaa" / f"{station}_{start:%Y%m%d}_{end:%Y%m%d}.json"
            # Historical windows are immutable caches; refresh the current partial decade.
            cached = path.exists() and end.month == 12 and end.year < date.today().year
            if cached:
                payload = json.loads(path.read_text(encoding="utf-8"))
            else:
                params = dict(product="monthly_mean", application="SeaLevelDetective",
                              station=station, begin_date=start.strftime("%Y%m%d"),
                              end_date=end.strftime("%Y%m%d"), datum="MSL", units="metric",
                              time_zone="gmt", format="json")
                payload = get(client, NOAA_API, params=params).json()
                parse_gauge(payload)  # Do not cache an API error other than an empty record.
                path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            part = parse_gauge(payload)
            parts.append(part)
            print(f"  {start:%Y}-{end:%Y}: {part.count()} months{' (cached)' if cached else ''}", flush=True)
        series = pd.concat(parts).sort_index()
        if series.index.has_duplicates:
            raise ValueError(f"Overlapping NOAA observations for {station}")
        series = series.loc[series.first_valid_index():series.last_valid_index()]
        if not series.count():
            raise ValueError(f"No monthly observations returned for {station}")
        series.resample("MS").mean().to_csv(PROCESSED / f"gauge_{station}.csv")
        report["gauges"][station] = {"name": info["name"], **metadata(series),
                                      "source": NOAA_API, "missing_months": int(series.resample("MS").mean().isna().sum())}
    print("NOAA: fetching ONI", flush=True)
    text = get(client, ONI_URL).text
    oni = parse_oni(text)
    (RAW / "noaa" / "oni.ascii.txt").write_text(text, encoding="utf-8")
    oni.to_csv(PROCESSED / "oni.csv")
    report["oni"] = {**metadata(oni), "source": ONI_URL, "units": "degree C",
                     "time_assignment": "central month; DJF is January of the stated year"}
    return save_json("noaa_manifest.json", report)


if __name__ == "__main__":
    main()
