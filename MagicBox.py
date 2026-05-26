from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from imu import MPU6050
from time import sleep
import math

#OLED Display
WIDTH =128 
HEIGHT= 64
i2c=I2C(1,scl=Pin(15),sda=Pin(14),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

#MPU Gyroscope
i2cMPU = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
imu = MPU6050(i2cMPU)

# Complementary filter parameters
dt = 0.02         # 20ms loop time
alpha = 0.98      # filter coefficient
pitch = 0.0       # initial pitch angle

# winning counter
winner=0
winCount=200

def get_pitch():
    global pitch

    # Calculate pitch from accelerometer
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    
    accel_pitch = math.degrees(math.atan2(ax, math.sqrt(ay**2 + az**2)))

    # Gyroscope angular rate
    #gyro_rate = gyro_data['y']  # rotation around Y-axis
    gyro_rate=ay
    
    # Complementary filter 
    pitch = alpha * (pitch + gyro_rate * dt) + (1 - alpha) * accel_pitch
    return pitch

def drawface(yPosition):
    global winner
    oled.pixel(30, yPosition, 60)  #x, y, color
    oled.pixel(30, yPosition+1, 60)  #x, y, color
    oled.pixel(31, yPosition, 60)  #x, y, color
    oled.pixel(31, yPosition+1, 60)  #x, y, color 
    winner=winner+1
    
def gameover():
    oled.fill(0)
    oled.text("Game Over!", 32, 32)
    oled.show()
    sleep(3)
    
def wingame():
    oled.fill(0)
    oled.text("You Win!", 32, 32)
    oled.show()
    sleep(3)
    
    
myY=0  #Y Position


while True:
    angle = get_pitch()
    print(f"Pitch Angle: {angle:.2f}°")
    
    oled.fill(0)
    pAngle="angle: "+str(angle)
    #oled.text("Robot LAB", 0, 0)
    oled.text(pAngle, 0, 0)
    oled.text("win: "+str(winner),0,10)
    if angle>2:
        print("angle greater 2")
        #move dot to the top, meaning y is decreasing
        myY=myY-1
        drawface(myY)
        
        if(myY<0):
            gameover()
            winner=0 #reset winning count to 0
            myY=64        
    else:
        #move dot to the bottom, meaning y is increasing
        print("angle less than 2")
        myY=myY+1
        drawface(myY)
        
        if(myY>64):
            gameover()
            winner=0  #reset winning count to 0
            myY=0
            
    if winner>winCount:
        wingame()
        winner=0 #reset winning count to 0
    oled.show()

