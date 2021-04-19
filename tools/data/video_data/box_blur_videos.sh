#!/bin/bash
#
# DESCRIPTION:
#    Goes through a drectory recursively and blurrs videos using box blur

for fullfile in */*.avi
do
    filename=$(basename -- "$fullfile")
    extension="${filename##*.}"
    filename="${filename%.*}"
    dirloc=$(dirname "${fullfile}")
    
    CMD="ffmpeg -i ${fullfile} -c:v libx264 -crf 0 -vf 'boxblur' ${dirloc}/${filename}_blurred_0to3_sec.avi"
    eval $CMD
done
