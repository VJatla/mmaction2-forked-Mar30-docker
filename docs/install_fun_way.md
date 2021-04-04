# MMACTION2
## Document log
+ **Created	:** Mar 31st, 2021
+ **Updated	:**
+ **About	:** Installation and usage of MMACTION2.
## System
+ **OS				:** Ubuntu 18.04(docker)
+ **GPU				:** 3 x Nvidia RTX 5000
+ **CPU				:** Intel Xeon
+ **System name		:** *"RTX3"* @ ivPCL 224D
+ **Nvidia driver   :**
+ **CUDA            :** 10.2
+ **CUDNN           :** 7
+ **Fork Link		:** [Fork](https://github.com/VJatla/mmaction2-forked-Mar30)
+ **Fork date		:** March 30th of 2021
+ **Original repo	:** [Original](https://github.com/open-mmlab/mmaction2)
## Installation instructions
**Skip these instrcutions if you are not interested in building from Ubuntu 18.04 base.**
### 1. Create docker image with required packages
1. Dowload ubuntu image
```bash
sudo docker pull nvidia/cuda:10.2-devel-ubuntu18.04
```
2. Start
```bash
sudo docker run --name ubuntu1804 --gpus 3 --shm-size 64G -it nvidia/cuda:10.2-devel-ubuntu18.04
```
3. Install packages necessary
```bash
# Python
apt-get install python3 python3-dev python3-pip python python-pip
ln -sf /usr/bin/pip3 /usr/bin/pip
ln -sf /usr/bin/python3 /usr/bin/python

# Packages
apt-get update
apt-get install -y build-essential python3-dev python3-setuptools make cmake libavcodec-dev libavfilter-dev libavformat-dev libavutil-dev software-properties-common git wget dh-autoreconf pkg-config libssl-dev

# FFMPEG
add-apt-repository ppa:jonathonf/ffmpeg-4
apt-get install ffmpeg
```
4. Commit changes to continer
```bash
sudo docker commit 5b4736f5f525 venkatesh369/mmaction2_mar30_2021:with_packages
```
### 2. Installing `mmcv` and `mmaction2` to user account
1. Start contianer by mounting a directory at `/home`
```bash
sudo docker run --name mmaction2_mar30_2021 --gpus 3 --shm-size 64G -it -v /home/vj/DockerHome/mmaction2_mar30_2021:/home venkatesh369/mmaction2_mar30_2021:with_packages
```
2. Create user(mma2)
```bash
useradd -s /bin/bash -d /home/mma2/ -m -G sudo mma2
passwd mma2 # To set user password
su mma2
cd ~
```
3. Decord
Before compiling from source we need to make sure that libnvcuvid is present. For
cuda versions > 9.2 it is not provided. To handle this, download
[NVIDIA VIDEO CODEC SDK ](https://developer.nvidia.com/nvidia-video-codec-sdk)
and copy the header files to your cuda path (/usr/local/cuda-10.0/include/ for example)
```bash
unzip Video_Codec_SDK_11.0.10.zip
cp Video_Codec_SDK_11.0.10/Interface/nvcuvid.h /usr/local/cuda-10.2/include/
cp Video_Codec_SDK_11.0.10/Interface/cuviddec.h /usr/local/cuda-10.2/include/
cp Video_Codec_SDK_11.0.10/Lib/linux/stubs/x86_64/libnvcuvid.so /usr/local/cuda-10.2/lib64/libnvcuvid.so.1
cp Video_Codec_SDK_11.0.10/Lib/linux/stubs/x86_64/libnvcuvid.so /usr/local/cuda-10.2/lib64/libnvcuvid.so

git clone --recursive https://github.com/dmlc/decord
cd decord
mkdir build && cd build
cmake .. -DUSE_CUDA=0 -DCMAKE_BUILD_TYPE=Release

cd ../python
pwd=$PWD
echo "PYTHONPATH=$PYTHONPATH:$pwd" >> ~/.bashrc
source ~/.bashrc
source activate open-mmlab
python3 setup.py install --user
```

4. Dense flow
Here are [Official instructions](https://github.com/open-mmlab/denseflow/blob/master/INSTALL.md).
My notes are as follows, keep the following lines in `~/.bashrc` and source it.
```bash
export ZZROOT=$HOME/app
export PATH=$ZZROOT/bin:$PATH
export LD_LIBRARY_PATH=$ZZROOT/lib:$ZZROOT/lib64:$LD_LIBRARY_PATH
```
Download the scripts to `setup` directory
```bash
source ~/.bashrc
git clone https://github.com/innerlee/setup.git
cd setup

./zznasm.sh
./zzyasm.sh
./zzlibx264.sh
./zzlibx265.sh
./zzlibvpx.sh

./zzffmpeg.sh

./zzopencv.sh
```
Add this to `~/.bashrc` after installing opencv
```bash
export OpenCV_DIR=$ZZROOT
source ~/.bashrc
```
Install boost and `export BOOST_ROOT=$ZZROOT` to `~/.bashrc` and source it.
```bash
./zzboost.sh
# Add export BOOST_ROOT=$ZZROOT to ~/.bashrc
source ~/.bashrc
```
HDF5
```bash
./zzhdf5.sh
```
Cmake
```bash
./zzcmake.sh
apt-get remove cmake # Removing system cmake
```
Densefow
```bash
./zzdenseflow.sh
```
5. moviepy
```bash
apt-get install imagemagick --fix-missing
pip install moviepy --user
```
As noted in the official installation guide we have to change the policy.
```bash
# Comment the following line in /etc/ImageMagick-6/policy.xml
<policy domain="path" rights="none" pattern="@*" />
# to
<!-- <policy domain="path" rights="none" pattern="@*" /> -->

```

6. Python packages
```bash
# Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
bash Anaconda3-2020.11-Linux-x86_64.sh
rm Anaconda3-2020.11-Linux-x86_64.sh
source ~/.bashrc

# Create environment
conda create -n open-mmlab python=3.7 -y
conda activate open-mmlab

# Pytorch
conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.2 -c pytorch

# pyav
conda install av -c conda-forge -y
pip install PyTurboJPEG --user

# SIMD-Pillow
conda uninstall -y --force pillow pil jpeg libtiff libjpeg-turbo
pip   uninstall -y         pillow pil jpeg libtiff libjpeg-turbo
conda install -yc conda-forge libjpeg-turbo
CFLAGS="${CFLAGS} -mavx2" pip install --upgrade --no-cache-dir --force-reinstall --no-binary :all: --compile pillow-simd
conda install -y jpeg libtiff

# mmcv
pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/102/torch1.6.0/index.html
```
7. MMACTION2
```bash
cd ~
git clone https://github.com/vjatla/mmaction2-forked-Mar30.git ~/mmaction2
cd mmaction2
pip install -r requirements/build.txt
 pip install -v -e .
```
8. MMDETECTION
For spatio temporal recognition we need to use mmdetection.
*"This is new. I did not see this step 1 year back. -vj(Apr 03, 2021)"*
```bash
cd ~
git clone https://github.com/vjatla/mmdetection-apr3-2021.git mmdetection
cd mmdetection
pip install -r requirements/build.txt
pip install -v -e .
```
### 3. Verification
Run he following code
```bash
# from /home/mma2/mmaction2
python demo/demo.py configs/recognition/tsn/tsn_r50_video_inference_1x1x3_100e_kinetics400_rgb.py https://download.openmmlab.com/mmaction/recognition/tsn/tsn_r50_1x1x3_100e_kinetics400_rgb/tsn_r50_1x1x3_100e_kinetics400_rgb_20200614-e508be42.pth demo/demo.mp4 demo/label_map_k400.txt --out-filename demo/demo_out.mp4
```
