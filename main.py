from machine import I2C, Pin, TouchPad
import socket
from ADXL345 import ADXL345_I2C
import math
import time

# I2C initialisieren
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
imu = ADXL345_I2C(i2c)

#TouchPin initialisieren
touch1 = 15

#starten
starten = TouchPad(Pin(touch1))
TOUCH_THRESHHOLD = 500

# Anfangsgeschwindigkeit
velocity_x = 0.0
velocity_y = 0.0
velocity_z = 0.0

# Zeitvariable für Integration
prev_time = time.ticks_ms()
acceleration_history = []

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

# Initialisierte Werte für den Filter
prev_x_corrected, prev_y_corrected, prev_z_corrected = 0, 0, 0

try:
    while True:
        if starten.read() < TOUCH_THRESHHOLD:
            # Beschleunigungswerte auslesen
            x, y, z = imu.xValue*0.039, imu.yValue*0.039+0.7 , imu.zValue*0.039 -1.5 #offset
            print(f"X: {x}")

                #Berechnung der Beschleunigung der einzelnen Achsen 


            imu_ges = math.sqrt(x**2 + y**2 + z**2)

            current_time = time.ticks_ms()
            delta_time = time.ticks_diff(current_time, prev_time) / 1000.0
            print(f"Delta Time: {delta_time:.2f}")
            prev_time = current_time

            pitch, roll = calculate_angles(x, y, z)

                # Schwerkraftkompensation
            gravity_x = 9.81 * math.sin(math.radians(pitch))
            gravity_y = 9.81 * math.sin(math.radians(roll))
            gravity_z = 9.81 * math.cos(math.radians(pitch)) * math.cos(math.radians(roll))
                #print(gravity_z)                                           
            x_corrected = x - gravity_x
            y_corrected = y - gravity_y
            if z < 0:
                z_corrected = z + gravity_z
            else: 
                z_corrected = z - gravity_z
                #print(z_corrected)

            gravity_ges = math.sqrt(gravity_x**2 + gravity_y**2 + gravity_z**2)

            accelaration_ges = math.sqrt(x_corrected**2 + y_corrected**2 + z_corrected**2)
                    # Beschleunigungswerte speichern
            acceleration_history.append((x_corrected, y_corrected, z_corrected, delta_time))
            if len(acceleration_history) > 20:
                acceleration_history.pop(0)

                # Geschwindigkeit über die letzten 20 Werte berechnen
            velocity_x = 0.0
            velocity_y = 0.0
            velocity_z = 0.0
            for ax, ay, az, dt in acceleration_history:
                velocity_x += calculate_velocity(ax, dt)
                velocity_y += calculate_velocity(ay, dt)
                velocity_z += calculate_velocity(az, dt)

                # Gesamtgeschwindigkeit als Vektor
            velocity_ges = math.sqrt(velocity_x**2 + velocity_y**2 + velocity_z**2) #offset

                #print(f"Velocity: {velocity_ges:.2f} m/s")

            time.sleep(0.01)
except KeyboardInterrupt: 
    print ("Programm beendet")