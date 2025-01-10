from machine import I2C, Pin
import socket
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

def web_page():
    f = open('index.html')
    html = f.read()
    f.close()
    return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

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


    conn, addr = s.accept()

    request = conn.recv(1024)
    request = str(request)

    start_index = request.find("MSGBGN")
    end_index = request.find("MSGEND")
    value = request[start_index+len("MSGBGN"):end_index]

    try:
        led_value = int(value)
    
    except Exception as e:
        print("Invalid value received, Ignored")

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

    time.sleep(0.01)
