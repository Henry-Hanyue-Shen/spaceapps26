#!/bin/sh
echo host:; which ffmpeg ffprobe
echo docker:; docker run --rm yh/sld:20261114 sh -c "which ffmpeg; python -c \"import imageio_ffmpeg as m; print(m.get_ffmpeg_exe())\"" 2>&1 | tail -2
mkdir -p ~/sea-level-detective/video
