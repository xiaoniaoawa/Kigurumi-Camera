# Kigurumi-Camera <br>
Make a Kigurumi Camera to record ur life with a RaspberryPi <br>
用一片 RaspberryPi 制作 Kigurumi 摄像头（行娃记录仪） <br>
 
#Before Start | 开始之前 <br>
确保您插入了兼容的CSI摄像头，并在RaspberryPi上安装了Raspberry Pi OS，主用户为kigcam，本程序兼容 Debian 11 和 Raspberry Pi OS Lite 镜像，最好为64位 <br>
将状态LED插入GPIO#27并将按钮插入GPIO#17（默认情况下） <br>
运行 <br>
'sudo apt-get install python3-picamera python3-rpi.gpio' <br>
并且运行 <br>
'sudo raspi-config' <br>
确认其中的 Legacy Camera 为关闭状态 <br>
 <br>
格式化一个USB驱动器并命名为kigcam，插入设备，并通电。 <br>
在Raspberry Pi OS 中，将会自动挂载到 '/media/kigcam/kigcam' 下，当然此路径可以通过修改kigcam.py来设定 <br>
 <br>
 <br>
#Install | 安装 <br>
下载 kigcam.py 到 /usr/bin/kigcam.py <br>
按需求可适当修改kigcam.py <br>
下载 kigcamera.service 到 /etc/systemd/system/kigcamera.service <br>
运行 <br>
'sudo systemctl daemon-reload' <br>
'sudo systemctl enable kigcamera.service' <br>
'sudo systemctl start kigcamera.service' <br>
恭喜你制作成功了自己的行娃记录仪 <br>
 <br>
#Use | 使用 <br>
在设备正常开机的情况下，按下按钮，LED灯亮起，开始录制，再次按下，录制结束，文件可在 kigcam.py 中配置的路径下找到。 <br>


本程序采用GNU GPLv3开源协议，请遵循该协议。
(Copyright) xiaoniaoawa 2022-2025
