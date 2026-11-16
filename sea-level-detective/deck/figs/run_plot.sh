#!/bin/sh
cd ~/sea-level-detective
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/w" -w /w/deck_figs yh/sld:20261114 python plot_clue_maps.py /w/deck_figs 2>&1 | tail -1
