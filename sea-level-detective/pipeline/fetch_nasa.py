"""Download the four specified NASA collections. Never store credentials."""
import os
import json
from pathlib import Path
from urllib.parse import urlparse, unquote
from config import NASA_COLLECTIONS, RAW, ensure_dirs


def main():
    if not os.environ.get("EARTHDATA_TOKEN"):
        raise SystemExit("EARTHDATA_TOKEN is not set. Use run_all.py --no-nasa; NASA download skipped.")
    import earthaccess
    ensure_dirs()
    auth = earthaccess.login(strategy="environment")
    if not auth.authenticated:
        raise SystemExit("Earthdata environment authentication failed; check EARTHDATA_TOKEN.")
    manifest = {}
    for key, collection in NASA_COLLECTIONS.items():
        print(f"NASA: discovering every granule of {collection}", flush=True)
        granules = earthaccess.search_data(short_name=collection, count=-1)
        if not granules:
            raise RuntimeError(f"No granules found for {collection}")
        destination = RAW / "nasa" / key
        destination.mkdir(exist_ok=True)
        names = []
        for granule in granules:
            suffixes = (".nc", ".nc4") if key == "grid" else (".txt",)
            links = [url for url in granule.data_links(access="external")
                     if urlparse(url).path.lower().endswith(suffixes)]
            if not links:
                raise RuntimeError(f"Granule in {collection} has no expected data link")
            names.extend(links)
        names = list(dict.fromkeys(names))
        basenames = [Path(unquote(urlparse(url).path)).name for url in names]
        if len(set(basenames)) != len(basenames):
            raise RuntimeError(f"Duplicate granule filenames in {collection}")
        pending = [url for url, name in zip(names, basenames)
                   if not (destination / name).is_file() or (destination / name).stat().st_size == 0]
        print(f"NASA: {len(names)} files, {len(pending)} to download", flush=True)
        if pending:
            # earthaccess itself manages up to eight concurrent downloads.
            earthaccess.download(pending, local_path=destination, threads=8)
        missing = [name for name in basenames if not (destination / name).is_file()
                   or (destination / name).stat().st_size == 0]
        if missing:
            raise RuntimeError(f"NASA download incomplete: {len(missing)} missing files in {collection}")
        manifest[key] = {"collection": collection, "files": basenames}
    (RAW / "nasa" / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
