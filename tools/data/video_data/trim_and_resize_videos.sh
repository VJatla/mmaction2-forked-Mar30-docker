#!/bin/bash
#
# DESCRIPTION:
#     The following script goes throgh all avi video(10 sec min duration)
#     files recursively, and trims them into 3 3 second segments and also
#     resize them to 240 pixels along height.

for fullfile in */*.avi
do
    filename=$(basename -- "$fullfile")
    extension="${filename##*.}"
    filename="${filename%.*}"
    dirloc=$(dirname "${fullfile}")
    
    CMD1="ffmpeg -ss 0 -i ${fullfile} -to 3 -c:a copy -c:v libx264 -crf 0 -vf 'scale=-1:240' ${dirloc}/${filename}_0to3_sec.avi"
    CMD2="ffmpeg -ss 3 -i ${fullfile} -to 3 -c:a copy -c:v libx264 -crf 0 -vf 'scale=-1:240' ${dirloc}/${filename}_3to6_sec.avi"
    CMD3="ffmpeg -ss 6 -i ${fullfile} -to 3 -c:a copy -c:v libx264 -crf 0 -vf 'scale=-1:240' ${dirloc}/${filename}_6to9_sec.avi"
    
    eval $CMD1
    eval $CMD2
    eval $CMD3
done




for fullfile in */*.mp4
do
    filename=$(basename -- "$fullfile")
    extension="${filename##*.}"
    filename="${filename%.*}"
    dirloc=$(dirname "${fullfile}")
    
    CMD1="ffmpeg -i ${fullfile} -c:a copy -c:v libx264  ${dirloc}/${filename}.wmv"
    eval $CMD1
done
