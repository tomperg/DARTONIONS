from machine import I2C, Pin
from ADXL345 import ADXL345_I2C
from functions import calculate_angles
import math
import time

# I2C initialisieren
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
imu = ADXL345_I2C(i2c)

# Anfangsgeschwindigkeit
velocity_x = 0.0
velocity_y = 0.0
velocity_z = 0.0

# Zeitvariable für Integration
prev_time = time.ticks_ms()

def calculate_velocity(acceleration, delta_time):
    return acceleration * delta_time

while True:
    # Beschleunigungswerte auslesen
    x = imu.xValue
    y = imu.yValue
    z = imu.zValue

    # Zeit seit der letzten Messung
    current_time = time.ticks_ms()
    delta_time = time.ticks_diff(current_time, prev_time) / 1000.0  # Umrechnung in Sekunden
    prev_time = current_time

    # Geschwindigkeit berechnen
    velocity_x += calculate_velocity(x, delta_time)
    velocity_y += calculate_velocity(y, delta_time)
    velocity_z += calculate_velocity(z, delta_time)

    # Winkel berechnen
    pitch, roll = calculate_angles(x, y, z)

    # Ausgabe
    print(f"Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")
    print(f"Velocity: X: {velocity_x:.2f} m/s, Y: {velocity_y:.2f} m/s, Z: {velocity_z:.2f} m/s")

    time.sleep(0.01)
