#!/bin/bash
# Run the NTR study on the DGX inside the yh/sld image. Usage: bash run_ntr_dgx.sh [noaa|nasa]
#   noaa : NOAA data only (no login): NTR, ONI, CPC NAO
#   nasa : also MERRA-2 predictors (needs ~/.earthdata_token, mounted read-only; never printed)
set -e
MODE=${1:-noaa}
cd ~/sea-level-detective
SECRET=""
if [ "$MODE" = "nasa" ]; then
  test -f ~/.earthdata_token || { echo "no ~/.earthdata_token"; exit 2; }
  SECRET="-v $HOME/.earthdata_token:/secrets/earthdata_token:ro"
fi
docker run --rm --cpus 4 --memory 16g $SECRET -v "$PWD":/work -w /work/ntr -e MPLCONFIGDIR=/tmp yh/sld:20261114 bash -c "
  set -e
  python fetch_noaa_ntr.py
  python build_ntr.py
  python fetch_public_predictors.py
  if [ '$MODE' = 'nasa' ]; then python fetch_nasa_predictors.py; fi
  python model.py
" 2>&1 | grep -v -E '^(=+|== PyTorch|NVIDIA Release|PyTorch Version|Container image|Copyright|All rights|Various files|GOVERNING|\(found at|and the Product|WARNING: The NVIDIA|   Use the NVIDIA|NOTE: The SHMEM|   docker run|   insufficient)' | sed '/^$/N;/^\n$/D'
