from machine import I2C, Pin
import socket
from ADXL345 import ADXL345_I2C
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
    velocity = acceleration*delta_time
    return velocity

'''def web_page():
    f = open('index.html')
    html = f.read()
    f.close()
    return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)'''

def calculate_angles(x, y, z):
    # Berechne Pitch und Roll
    pitch = math.degrees(math.atan2(x, math.sqrt(y**2 + z**2)))
    roll = math.degrees(math.atan2(y, math.sqrt(x**2 + z**2)))
    return pitch, roll

def calculate_velocity(acceleration, delta_time):
    # Numerische Integration zur Geschwindigkeitsberechnung
    return acceleration * delta_time

def high_pass_filter(value, prev_value, alpha=0.8):
    # High-Pass-Filter zur Reduktion von Schwerkraftanteilen
    return alpha * (prev_value + value)

# Initialisierte Werte für den Filter
prev_x_corrected, prev_y_corrected, prev_z_corrected = 0, 0, 0

while True:
    # Beschleunigungswerte auslesen
    x, y, z = imu.xValue*0.039, imu.yValue*0.039, imu.zValue*0.039
    print(f"X: {x}, Y: {y}, Z: {z}")

    #Berechnung der Beschleunigung der einzelnen Achsen 


    imu_ges = math.sqrt(x**2 + y**2 + z**2)

    current_time = time.ticks_ms()
    delta_time = time.ticks_diff(current_time, prev_time) / 1000.0
    prev_time = current_time

    pitch, roll = calculate_angles(x, y, z)

    # Schwerkraftkompensation
    gravity_x = 9.81 * math.sin(math.radians(pitch))
    gravity_y = -9.81 * math.sin(math.radians(roll))
    gravity_z = 9.81 * math.cos(math.radians(pitch)) * math.cos(math.radians(roll))

    x_corrected = x - gravity_x
    y_corrected = y - gravity_y
    z_corrected = z - gravity_z

    gravity_ges = math.sqrt(gravity_x**2 + gravity_y**2 + gravity_z**2)

    print(f"X: {gravity_x}, Y: {gravity_y}, Z: {gravity_z}")
    print(f"Gravity: {gravity_ges:.2f} m/s^2")
    # High-Pass-Filter anwenden
    x_filtered = high_pass_filter(x_corrected, prev_x_corrected)
    y_filtered = high_pass_filter(y_corrected, prev_y_corrected)
    z_filtered = high_pass_filter(z_corrected, prev_z_corrected)

    prev_x_corrected, prev_y_corrected, prev_z_corrected = x_filtered, y_filtered, z_filtered

    # Geschwindigkeit berechnen
    velocity_x += calculate_velocity(x_filtered, delta_time)
    velocity_y += calculate_velocity(y_filtered, delta_time)
    velocity_z += calculate_velocity(z_filtered, delta_time)

    velocity_ges = math.sqrt(velocity_x**2 + velocity_y**2 + velocity_z**2)

    #print(f"Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")
    #print(f"Velocity: X: {velocity_x:.2f} m/s, Y: {velocity_y:.2f} m/s, Z: {velocity_z:.2f} m/s")
    #print(f"Gesamtgeschwindigkeit: {velocity_ges:.2f} m/s")

    time.sleep(0.1)
