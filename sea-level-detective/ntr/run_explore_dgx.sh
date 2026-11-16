#!/bin/bash
# Run one exploration step on the DGX in the yh/sld image. Usage: bash run_explore_dgx.sh fetch|analyze
set -e
STEP=${1:-analyze}
cd ~/sea-level-detective
docker run --rm --cpus 6 --memory 16g -v "$PWD":/work -w /work/ntr -e MPLCONFIGDIR=/tmp -e PYTHONWARNINGS=ignore \
  yh/sld:20261114 python explore_${STEP}.py > ntr/explore_${STEP}.log 2>&1
echo "exit=$?"
grep -v -E '^(=+|== PyTorch|NVIDIA Release|PyTorch Version|Container image|Copyright|All rights|Various files|GOVERNING|\(found at|and the Product|WARNING: The NVIDIA|   Use the NVIDIA|   https://docs|NOTE: The SHMEM|   docker run|   insufficient|$)' ntr/explore_${STEP}.log | tail -${2:-80}
