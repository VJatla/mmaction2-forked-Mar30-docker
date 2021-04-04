# Easy way of installing mmaction2
## 0. Prerequisite
1. Docker
2. nvidia-docker
## 1. Pull docker image
```bash
docker pull venkatesh369/mmaction2_mar30_2021
```
## 2. Download home directory
Download compressed home directory by [Clicking here](https://www.dropbox.com/s/hw858g9hw9taxd1/home.tar.gz?dl=0).
```bash
# Create a directory for docker home
mkdir ~/DockerHome

# Uncompress the home direcotry to ~/DockerHome
tar -pxvzf <location of home.tar.gz> ~/DockerHome/
```
## 3. Start docker container
```bash
sudo docker run --name mmaction2_mar30_2021 --gpus all --shm-size 8G -it -v /home/vj/DockerHome/mmaction2_mar30_2021:/home venkatesh369/mmaction2_mar30_2021:light
```
1. `shm-size` can be more than 8GB
2. Make sure that you mount appropriate directories using `-v` flag.
