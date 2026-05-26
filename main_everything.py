from machine import Pin, I2C
import ssd1306
from imu import MPU6050
from time import sleep
import math
from pca9685 import PCA9685

WIDTH =128 
HEIGHT= 64
# Initialize I2C perhipheral
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
i2cMPU = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
i2cServo = I2C(0, scl=Pin(9), sda=Pin(8))  # GP1 = SCL, GP0 = SDA
imu = MPU6050(i2cMPU)

# Initialise OLED display
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2cMPU, addr=0x3c)

#servo
# Setup PCA9685
pwm = PCA9685(i2cServo)
servo1 = 0  # servo 1
servo2 = 1  # servo 2

#mpu pitch
def get_pitch(ax, ay, az):
    pitch = math.degrees(math.atan2(ax, math.sqrt(ay**2 + az**2)))
    return pitch


while True:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    #print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",tem,"        ",end="\r")
    pitch = get_pitch(ax, ay, az)
    angle = max(0, min(180, 90 + int(pitch)))  # Map -90 to +90 pitch to 0-180
    print("Pitch:", pitch, "Angle:", angle)

    pitch2 = get_pitch(ay, ax, az)
    angle2 = max(0, min(180, 90 + int(pitch2)))  # Map -90 to +90 pitch to 0-180
    print("Pitch2:", pitch2, "Angle:", angle2)
    
    angle=abs(180-angle)
    if(angle<70):
        angle=70
    if(angle>120):
        angle=120
    if(angle2<70):
        angle2=70
    if(angle2>120):
        angle2=120
    pwm.set_servo_angle2(servo1, angle)
    pwm.set_servo_angle2(servo2, angle2)
    sleep(0.2)
    
    oled.fill(0)
    outputStr = "Servo #1: "+str(angle)
    outputStr2 ="Servo #2: "+str(angle2)
    oled.text(outputStr, 0, 0)
    oled.text(outputStr2, 0, 10)
    oled.text(str(tem), 0, 40)
    oled.show()

