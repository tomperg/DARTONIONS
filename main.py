from machine import Pin, I2C
import time
import math
from functions import *
import socket 
import os 

# MPU6050-Klasse importieren
from MPU6050 import MPU6050

# I²C initialisieren
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Zwei MPU6050-Sensoren initialisieren
mpu1 = MPU6050(i2c, addr=0x69) #AD0 auf vcc für andere Adresse
mpu2 = MPU6050(i2c, addr=0x68)

def web_page():

    f = open('webserver.html')
    html = f.read()
    f.close()
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# Globale Variablen
last_relative_roll = None
prev_time = None  # Für Delta-T
velocity_reset = False  # Geschwindigkeit zurücksetzen

# Interrupt-Handler
def touch_interrupt_handler(pin):
    global last_relative_roll, prev_time, velocity_reset

    reset_velocity() # Geschwindigkeit zurücksetzen

    print("Kontakt erkannt! Schleife gestartet.")
    
    # Initiale Zeit festlegen
    prev_time = time.ticks_ms() / 1000.0

    while not pin.value():  # Prüfen, ob der Schalter geschlossen ist
        current_time = time.ticks_ms() / 1000.0
        dt = current_time - prev_time
        prev_time = current_time

        # Beschleunigung und Gyro-Daten lesen
        accel1 = mpu1.get_accel()
        gyro1 = mpu1.get_gyro()

        # Schwerkraft vom Handgelenk IMU entfernen
        accel1_no_gravity = remove_gravity_with_gyro(accel1, gyro1, dt)

        # Geschwindigkeit berechnen
        update_velocity(accel1_no_gravity, dt)

        # Winkel berechnen
        roll1, _ = calculate_angles(accel1)
        accel2 = mpu2.get_accel()
        roll2, _ = calculate_angles(accel2)
        last_relative_roll = roll1 - roll2

        time.sleep(0.1)  # Schleifenintervall

    # Wenn der Schalter geöffnet wird
    print("Schalter geöffnet. Schleife beendet.")
    if last_relative_roll is not None:
        print("Letzter relativer Roll: {:.2f}°".format(last_relative_roll))
    print("Geschwindigkeit: x={:.2f} m/s, y={:.2f} m/s, z={:.2f} m/s".format(
        velocity['x'], velocity['y'], velocity['z']))

    # Geschwindigkeit zurücksetzen
    velocity_reset = True
    time.sleep(0.2)  # Entprellzeit

# GPIO für Schalter konfigurieren
touch_pin = Pin(15, Pin.IN, Pin.PULL_UP)  # GPIO 15 mit internem Pull-Up-Widerstand
touch_pin.irq(trigger=Pin.IRQ_FALLING, handler=touch_interrupt_handler)

# Hauptschleife
try:
    while True:
        time.sleep(1)  # Programm bleibt aktiv
except KeyboardInterrupt:
    print("Programm beendet.")