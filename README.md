# Kigurumi-Camera
Make a Kigurumi Camera to record ur life with a RaspberryPi 
用一片 RaspberryPi 制作 Kigurumi 摄像头（行娃记录仪） 
 
### Before Start | 开始之前 
确保您插入了兼容的CSI摄像头，并在RaspberryPi上安装了Raspberry Pi OS，主用户为`kigcam`，本程序兼容 Debian 11 和 Raspberry Pi OS Lite 镜像，最好为64位 
将状态LED插入`GPIO#27`并将按钮插入`GPIO#17`（默认情况下） 
运行
```bash
sudo apt-get install python3-picamera python3-rpi.gpio
```
并且运行
```bash
sudo raspi-config
```
确认其中的 `Legacy Camera` 为关闭状态 
 
### Install | 安装
下载 `kigcam.py` 到 `/usr/bin/kigcam.py` 
按需求可适当修改`kigcam.py` 
下载 kigcamera.service 到 `/etc/systemd/system/kigcamera.service` 
运行
```bash
sudo systemctl daemon-reload
sudo systemctl enable kigcamera.service
sudo systemctl start kigcamera.service
```
恭喜你制作成功了自己的行娃记录仪 
 
### Use | 使用
在设备正常开机的情况下，按下按钮，LED灯亮起，开始录制，再次按下，录制结束，文件可在 `kigcam.py` 中配置的路径下找到，默认为`/media/kigcam/kigcam` 。 
 
 
本程序采用GNU GPLv3开源协议，请遵循该协议。
(Copyright) xiaoniaoawa 2022-2025
