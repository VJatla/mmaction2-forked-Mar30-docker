# Custom data set preparation
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Custom data set preparation](#custom-data-set-preparation)
    - [0. Start docker container](#0-start-docker-container)
    - [1. Download](#1-download)
        - [1. custom data](#1-custom-data)
        - [2. configs and scripts](#2-configs-and-scripts)
    - [2. Creating video list for training](#2-creating-video-list-for-training)
    - [3. Training (single GPU)](#3-training-single-gpu)

<!-- markdown-toc end -->
## 0. Start docker container
```bash
sudo docker run --name mmaction2 --gpus 1 --shm-size 64G -it -v <mma2 home>:/home venkatesh369/mmaction2_mar30_2021:light2
```
In my case `<mma2 home>` is `/home/vj/DockerHome/mmaction2_mar30_2021`
## 1. Download 
### 1. custom data
1. Download data by [clicking this link](https://www.dropbox.com/s/5pdkkdpd4j3gnag/ucf101_3_classes.tar.gz?dl=0),
2. Extract it
3. Copy it to `<mma2 home>/mma2/mmaction2/data`(if there is no `data` directory create it.)
On doing this properly, we can see `ucf101_3_classes` at `/home/mma2/mmaction2/data/` in docker container. It
contians the following directories,
- `videos/`			: This directory has subdirectories with class name containing videos.
- `annotations/`	: Contains `ClassInd.txt`, a text file containing class indexes
### 2. configs and scripts
To process custom dataset, please clone the following git repo to mma2 user home
```bash
# From your docker terminal
su mma2
cd ~
git clone https://github.com/VJatla/mmaction2-forked-Mar30-docker.git ~/mmaction2-forked-Mar30-docker
```
## 2. Creating video list for training
This creates a `train.txt` file having class labels and relative video path.
```bash
cd ~/mmaction2-forked-Mar30-docker/custom_data/tools/data
python generate_videos_filelist.py ~/mmaction2/data/ucf101_3_classes avi ~/mmaction2/data/ucf101_3_classes/train.txt
```
## 3. Training (single GPU)
```bash
cd ~/mmaction2
python tools/train.py /home/mma2/mmaction2-forked-Mar30-docker/custom_data/configs/recognition/i3d/i3d_r50_video_32x2x1_100e_kinetics400_rgb.py --work-dir work_dirs/i3d_r50_32x2x1_100e_kinetics400_rgb --validate --seed 0 --deterministic
```
