#!/bin/sh
cd ~/sea-level-detective
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/w" -w /w/deck_figs yh/sld:20261114 sh -c "python plot_compare.py /w/deck_figs && python plot_hov.py /w/ntr/data_processed/ssh_gibs_monthly.npz /w/deck_figs" 2>&1 | grep -v -i "pytorch\|copyright\|shmem\|nvidia\|docker run\|ulimit\|reserved\|=====\|^ *\$" | tail -6
