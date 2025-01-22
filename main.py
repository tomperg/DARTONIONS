from machine import Pin, I2C
import time
import math

# MPU6050-Klasse importieren
from MPU6050 import MPU6050

# I²C initialisieren
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Zwei MPU6050-Sensoren initialisieren
mpu1 = MPU6050(i2c, addr=0x69)
mpu2 = MPU6050(i2c, addr=0x68)

# Globale Variablen
gyro_angle = {'pitch': 0.0, 'roll': 0.0}  # Orientierung basierend auf Gyro
alpha = 0.98  # Komplementärfilter-Konstante
last_relative_roll = None
velocity = {'x': 0.0, 'y': 0.0, 'z': 0.0}  # Geschwindigkeit
prev_time = None  # Für Delta-T
velocity_reset = False  # Geschwindigkeit zurücksetzen

# Funktion, um Orientierung mit Gyro-Daten zu berechnen
def update_orientation_with_gyro(gyro, dt):
    global gyro_angle
    gyro_angle['pitch'] += gyro['x'] * dt
    gyro_angle['roll'] += gyro['y'] * dt

# Funktion, um Schwerkraft zu entfernen
def remove_gravity_with_gyro(accel, gyro, dt):
    global gyro_angle

    # Orientierung aktualisieren
    update_orientation_with_gyro(gyro, dt)

    # Orientierung aus Beschleunigung schätzen
    accel_pitch = math.degrees(math.atan2(accel['x'], math.sqrt(accel['y']**2 + accel['z']**2)))
    accel_roll = math.degrees(math.atan2(accel['y'], math.sqrt(accel['x']**2 + accel['z']**2)))

    # Gyro und Beschleunigungsdaten kombinieren
    pitch = alpha * gyro_angle['pitch'] + (1 - alpha) * accel_pitch
    roll = alpha * gyro_angle['roll'] + (1 - alpha) * accel_roll

    # Schwerkraft berechnen
    gravity_x = math.sin(math.radians(pitch))
    gravity_y = -math.sin(math.radians(roll))
    gravity_z = math.cos(math.radians(pitch)) * math.cos(math.radians(roll))

    # Schwerkraft entfernen
    accel_x = accel['x'] - gravity_x
    accel_y = accel['y'] - gravity_y
    accel_z = accel['z'] - gravity_z

    return {'x': accel_x, 'y': accel_y, 'z': accel_z}

# Funktion zur Geschwindigkeitsberechnung
def update_velocity(accel_no_gravity, dt):
    global velocity, velocity_reset

    # Geschwindigkeit aktualisieren
    velocity['x'] += accel_no_gravity['x'] * dt
    velocity['y'] += accel_no_gravity['y'] * dt
    velocity['z'] += accel_no_gravity['z'] * dt

    # Bei Bedarf Geschwindigkeit zurücksetzen
    if velocity_reset:
        velocity = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        velocity_reset = False

# Interrupt-Handler
def touch_interrupt_handler(pin):
    global last_relative_roll, prev_time, velocity_reset

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

        # Schwerkraft entfernen
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

# Funktion zur Winkelberechnung
def calculate_angles(accel):
    x, y, z = accel['x'], accel['y'], accel['z']
    pitch = math.degrees(math.atan2(x, math.sqrt(y**2 + z**2)))
    roll = math.degrees(math.atan2(y, math.sqrt(x**2 + z**2)))
    return roll, pitch

# GPIO für Schalter konfigurieren
touch_pin = Pin(15, Pin.IN, Pin.PULL_UP)  # GPIO 15 mit internem Pull-Up-Widerstand
touch_pin.irq(trigger=Pin.IRQ_FALLING, handler=touch_interrupt_handler)

# Hauptschleife
try:
    while True:
        time.sleep(1)  # Programm bleibt aktiv
except KeyboardInterrupt:
    print("Programm beendet.")