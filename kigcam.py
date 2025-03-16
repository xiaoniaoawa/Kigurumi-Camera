from picamera2.encoders import H264Encoder
# 可编辑设置_按钮
BUTTON_PIN = 17    # 按钮GPIO编号（BCM模式）
LED_PIN = 27       # LED GPIO编号（BCM模式）

# 可编辑设置_保存
SAVE_PATH = "/mnt/kigcam" #保存路径 
VSIZE_W = 800 #视频宽度
VSIZE_H = 600 #视频高度

# 可编辑设置_高级
CHECK_INTERVAL = 5 #路径存在检测冷却(sec)
VIDENCODER = H264Encoder(10000000) #编码器





#引用模块
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import datetime
import os
import time
#from picamera2.encoders import H264Encoder

#清屏
os.system('clear')

# 初始化GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

# 初始化摄像头
camera = Picamera2()
print(camera.sensor_modes)
video_rec_config = camera.create_video_configuration(
    main={"size": (VSIZE_W, VSIZE_H)}
)
camera.configure(video_rec_config)
#在这里修改录制分辨率
is_recording = False


#到此结束初始化脚本
 
#挂载存储设备
os.system('sudo umount '+SAVE_PATH)
os.system('sudo mkdir '+SAVE_PATH)
os.system('sudo mount /dev/sda1 '+SAVE_PATH)
print('文件将会被储存到 '+SAVE_PATH+' , 挂载设备为sda1')


def wait_for_path():
    """等待存储路径就绪"""
    while not os.path.isdir(SAVE_PATH):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 等待存储路径：{SAVE_PATH}")
        print("请检查存储设备是否已正确挂载...")
        time.sleep(CHECK_INTERVAL)

def get_timestamp_filename():
    """生成带时间戳的文件名"""
    return datetime.datetime.now().strftime("kigcam_%Y%m%d_%H-%M-%S") + ".h264"

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
            for templed in range(4):
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(0.1)
            GPIO.output(LED_PIN, GPIO.HIGH)
            is_recording = True
            print(f"开始录制: {file_path}")
        else:
            camera.stop_recording()
            GPIO.output(LED_PIN, GPIO.LOW)
            
            for templed in range(4):
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(LED_PIN, GPIO.LOW)
                time.sleep(0.1)
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
