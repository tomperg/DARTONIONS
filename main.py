from machine import I2C, Pin
from adxl345 import ADXL345_I2C
from functions import calculate_angles
import math

#I2C initialisieren
i2c = I2C(0,sda=Pin(21), scl=Pin(22))
imu = ADXL345_I2C(i2c)

while True:
    # Beschleunigungswerte abrufen
    x, y, z = imu.acceleration
    
    # Winkel berechnen
    pitch, roll = calculate_angles(x, y, z)
    
    # Ausgabe
    print(f"Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")