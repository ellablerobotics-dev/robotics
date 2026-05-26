#this sample requires two library files from vendors
# imu.py
# vector3d.py

from imu import MPU6050
from time import sleep
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
WIDTH =128 
HEIGHT= 64

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
imu = MPU6050(i2c)

i2c2=I2C(1,scl=Pin(15),sda=Pin(14),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c2)

while True:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",tem,"        ",end="\r")
    sleep(0.2)
    
    oled.fill(0)
    oled.text("DIY PROJECTS LAB", 0, 0)
    oled.text("Tutorial", 20, 40)
    oled.show()

