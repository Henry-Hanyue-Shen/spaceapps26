#!/bin/bash
# Build the West (Los Angeles) site data on the DGX: New York scripts rerun unchanged on the LA target, then export.
# Usage: bash ntr/westcoast/run_site_dgx.sh [steps...]   (default: all)
cd ~/sea-level-detective
STEPS=${*:-"prepare build_ntr explore_analyze explore_maps explore_predictions explore_signal_winters explore_surge_dates explore_ssh_gibs model gauges export"}
docker run --rm --cpus 4 --memory 8g -v "$PWD":/work -w /work/ntr/westcoast -e MPLCONFIGDIR=/tmp -e PYTHONWARNINGS=ignore \
  yh/sld:20261114 bash -c "
  set -e; trap 'chown -R $(id -u):$(id -g) /work/ntr/westcoast' EXIT
  for s in $STEPS; do
    echo \"### \$s\"
    case \$s in
      gauges) python wc_site_gauges.py ;;
      export) python wc_site_export.py ;;
      *) python wc_site_run.py \$s ;;
    esac
  done
" > ntr/westcoast/site_build.log 2>&1
echo "exit=$?"
grep -v -E '^(=+|== PyTorch|NVIDIA Release|PyTorch Version|Container image|Copyright|All rights|Various files|GOVERNING|\(found at|and the Product|WARNING: The NVIDIA|   Use the NVIDIA|   https://docs|NOTE: The SHMEM|   docker run|   insufficient|$)' ntr/westcoast/site_build.log
