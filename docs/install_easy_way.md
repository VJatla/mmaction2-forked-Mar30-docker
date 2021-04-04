# Easy way of installing mmaction2
## 0. Prerequisite
1. Docker
2. nvidia-docker
## 1. Pull docker image
```bash
docker pull venkatesh369/mmaction2_mar30_2021:light2
```
## 2. Download home directory
```bash
# Create a directory for docker home
mkdir <docker home directory>
```
Download compressed home directory by [Clicking here](https://www.dropbox.com/s/hw858g9hw9taxd1/home.tar.gz?dl=0)
to `<docker home directory>` and uncompress.
```bash
cd <docker home directory>
tar -xvzf <location of home.tar.gz>
```
## 3. Start docker container
1. `shm-size` can be more than 8GB
2. Make sure that you mount appropriate directories using `-v` flag.
3. Please set your time zone correctly
```bash
sudo docker run --name mmaction2_mar30_2021 --gpus all --shm-size 8G -it -v <docker home directory>/mmacton2_mar30_2021:/home venkatesh369/mmaction2_mar30_2021:light2
```
## 4. Set time zone in container (optional, recommended)
```bash
dpkg-reconfigure tzdata
```

```bash
su mma2
cd ~/mmaction2
```
## 4. Test script
```bash
# From /home/mma2/mmaction2 folder, run
python demo/demo.py configs/recognition/tsn/tsn_r50_video_inference_1x1x3_100e_kinetics400_rgb.py https://download.openmmlab.com/mmaction/recognition/tsn/tsn_r50_1x1x3_100e_kinetics400_rgb/tsn_r50_1x1x3_100e_kinetics400_rgb_20200614-e508be42.pth demo/demo.mp4 demo/label_map_k400.txt --out-filename demo/demo_out.mp4
```
You should be able to see a arm wrestling video called demo_out.mp4 at `/home/mma2/mmaction2/demo/demo_out.mp4`.
This can be played by going to the same location in host system.
