from machine import Pin, I2C
import time
import math
from math import atan2, degrees, sqrt
from MPU6050 import MPU6050

# I²C-Konfiguration für den ESP32
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Passen Sie die GPIOs an, falls nötig

# MPU6050-Klasse (falls nicht vorhanden, verwenden Sie eine Bibliothek oder erweitern Sie diese)

# Zwei MPU6050-Module initialisieren
mpu1 = MPU6050(i2c, addr=0x68)  # Modul mit Adresse 0x68
mpu2 = MPU6050(i2c, addr=0x69)  # Modul mit Adresse 0x69

def calculate_angles(accel_data):
    ax = accel_data['x']
    ay = accel_data['y']
    az = accel_data['z']

    roll = degrees(atan2(ay, sqrt(ax ** 2 + az ** 2)))
    pitch = degrees(atan2(-ax, sqrt(ay ** 2 + az ** 2)))
    return roll, pitch

# Hauptprogramm
try:
    while True:
        accell1 = mpu1.get_accel()
        gyro1 = mpu1.get_gyro()
        roll1, pitch1 = calculate_angles(accell1)

        accell2 = mpu2.get_accel()
        gyro2 = mpu2.get_gyro()
        roll2, pitch2 = calculate_angles(accell2)

        relativeroll = roll1 - roll2
        relativepitch = pitch1 - pitch2

        print("Relativer Roll: {:.2f}°".format(relativeroll))
        

        time.sleep(0.1)  # 100 ms Verzögerung
except KeyboardInterrupt:
    print("Messung beendet")