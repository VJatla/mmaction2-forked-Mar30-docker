# Custom data set preparation
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Custom data set preparation](#custom-data-set-preparation)
    - [0. Start docker container](#0-start-docker-container)
    - [1. Data](#1-data)
    - [2. Custom dataset scripts](#2-custom-dataset-scripts)
    - [3. Extracting RGB + Optical flow images](#3-extracting-rgb--optical-flow-images)
    - [4. Creating training video list](#4-creating-training-video-list)
    - [4. Training using videos](#4-training-using-videos)

<!-- markdown-toc end -->
## 0. Start docker container
```bash
sudo docker run --name mmaction2 --gpus 1 --shm-size 64G -it -v <mma2 home>:/home venkatesh369/mmaction2_mar30_2021:light2
```
In my case `<mma2 home>` is `/home/vj/DockerHome/mmaction2_mar30_2021`
## 1. Data
1. Download data by [clicking this link](https://www.dropbox.com/s/j8a9bj7jmnorgzj/ucf101_3_classes.tar.gz?dl=0),
2. Extract it
3. Copy it to `<mma2 home>/mma2/mmaction2/data`(if there is no `data` directory create it.)
On doing this properly, we can see `ucf101_3_classes` at `/home/mma2/mmaction2/data/` in docker container. It
contians the following directories,
- `videos/`			: This directory has subdirectories with class name containing videos.
- `annotations/`	: Contains `ClassInd.txt`, a text file containing class indexes
## 2. Custom dataset scripts
To process custom dataset, please clone the following git repo to mma2 user home
```bash
git clone https://github.com/VJatla/mmaction2-forked-Mar30-docker.git ~/mmaction2-forked-Mar30-docker
```
## 3. Creating video list for training
```bash
cd
```
## 4. Training
```bash

```
