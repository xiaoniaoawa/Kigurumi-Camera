import RPi.GPIO as GPIO
from picamera2 import Picamera2
import datetime
import os
import time
from picamera2.encoders import H264Encoder

# 硬件设置
BUTTON_PIN = 17    # 按钮GPIO编号（BCM模式）
LED_PIN = 27       # LED GPIO编号（BCM模式）
SAVE_PATH = "/media/kigcam/kigcam/"
CHECK_INTERVAL = 5  # 路径检测间隔（秒）
VIDENCODER = H264Encoder(10000000)

# 初始化GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

# 初始化摄像头
camera = Picamera2()
camera.resolution = (1200, 960)
camera.framerate = 15
is_recording = False

def wait_for_path():
    """等待存储路径就绪"""
    while not os.path.isdir(SAVE_PATH):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 等待存储路径：{SAVE_PATH}")
        print("请检查存储设备是否已正确挂载...")
        time.sleep(CHECK_INTERVAL)

def get_timestamp_filename():
    """生成带时间戳的文件名"""
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".h264"

def button_callback(channel):
    global is_recording
    time.sleep(0.05)
    
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        if not is_recording:
            # 开始录制前再次确认路径
            if not os.path.isdir(SAVE_PATH):
                print("错误：存储路径已丢失！")
                return
                
            filename = get_timestamp_filename()
            file_path = os.path.join(SAVE_PATH, filename)
            print('recording with '+file_path)
            camera.start_recording(output=file_path, encoder=VIDENCODER)
            GPIO.output(LED_PIN, GPIO.HIGH)
            is_recording = True
            print(f"开始录制: {file_path}")
        else:
            camera.stop_recording()
            GPIO.output(LED_PIN, GPIO.LOW)
            is_recording = False
            print("录制已停止")

try:
    # 启动时等待存储路径就绪
    print("正在初始化...")
    wait_for_path()
    
    # 设置按钮中断检测
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, 
                         callback=button_callback, 
                         bouncetime=300)
    
    print("准备就绪，按下按钮开始录制...")
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    if is_recording:
        camera.stop_recording()
    GPIO.cleanup()
    camera.close()
    print("\n程序已安全退出")
except Exception as e:
    print(f"发生错误：{str(e)}")
    GPIO.cleanup()
    camera.close()
