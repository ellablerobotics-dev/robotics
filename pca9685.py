# pca9685.py
from machine import I2C
import time

MODE1 = 0x00
PRESCALE = 0xFE

class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.reset()
        self.set_pwm_freq(50)

    def reset(self):
        self.i2c.writeto_mem(self.address, MODE1, b'\x00')
        time.sleep_ms(10)

    def set_pwm_freq(self, freq_hz):
        prescale_val = int((25000000.0 / (4096 * freq_hz)) - 1)
        old_mode = self.i2c.readfrom_mem(self.address, MODE1, 1)[0]
        new_mode = (old_mode & 0x7F) | 0x10
        self.i2c.writeto_mem(self.address, MODE1, bytes([new_mode]))
        self.i2c.writeto_mem(self.address, PRESCALE, bytes([prescale_val]))
        self.i2c.writeto_mem(self.address, MODE1, bytes([old_mode]))
        time.sleep_ms(5)
        self.i2c.writeto_mem(self.address, MODE1, bytes([old_mode | 0xA1]))

    def set_pwm(self, channel, on, off):
        data = bytearray([
            on & 0xFF, on >> 8,
            off & 0xFF, off >> 8
        ])
        self.i2c.writeto_mem(self.address, 0x06 + 4 * channel, data)

    def set_servo_angle(self, channel, angle):
        angle = max(0, min(180, angle))
        pulse = int((angle * (500/45)) + 1500)  # Convert to microseconds
        pwm_val = int(pulse * 4096 / 20000)     # Convert to 12-bit (20ms frame)
        self.set_pwm(channel, 0, pwm_val)
        
    def set_servo_angle2(self, channel, angle):
        angle = max(0, min(180, angle))  # Clamp angle
        min_us = 500
        max_us = 2500
        us = min_us + (angle / 180) * (max_us - min_us)
        pwm_val = int(us * 4096 / 20000)  # Convert microseconds to 12-bit PWM step
        self.set_pwm(channel, 0, pwm_val)

