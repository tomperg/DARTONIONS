import math 
import time 
#Globale Valiablen

gyro_angle = {'pitch': 0.0, 'roll': 0.0}  # Orientierung basierend auf Gyro
alpha = 0.98  # Komplementärfilter-Konstante
velocity = {'x': 0.0, 'y': 0.0, 'z': 0.0}
velocity_reset = False
#functions we need in our main.py file
def update_orientation_with_gyro(gyro, dt):
    global gyro_angle
    gyro_angle['pitch'] += gyro['x'] * dt
    gyro_angle['roll'] += gyro['y'] * dt

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

def update_velocity(accel_no_gravity, dt):
    global velocity, velocity_reset

    # Geschwindigkeit aktualisieren
    velocity['x'] += accel_no_gravity['x'] * dt
    velocity['y'] += accel_no_gravity['y'] * dt
    velocity['z'] += accel_no_gravity['z'] * dt

    # Bei Bedarf Geschwindigkeit zurücksetzen
    if velocity_reset:
        velocity = {'x': 0.0, 'y': 0.0, 'z': 0.0}           #überprüfen ob das auch in der main.py funktioniert!!!!!!!!
        velocity_reset = False

# Funktion zur Winkelberechnung
def calculate_angles(accel):
    x, y, z = accel['x'], accel['y'], accel['z']
    pitch = math.degrees(math.atan2(x, math.sqrt(y**2 + z**2)))
    roll = math.degrees(math.atan2(y, math.sqrt(x**2 + z**2)))
    return roll, pitch