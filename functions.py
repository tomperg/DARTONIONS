import math 
import time 
#Globale Valiablen

gyro_angle = {'pitch': 0.0, 'roll': 0.0}  # Orientierung basierend auf Gyro
alpha = 0.98  # Komplementärfilter-Konstante
velocity = {'x': 0.0, 'y': 0.0, 'z': 0.0}
velocity_reset = False

def update_velocity(accel_no_gravity, dt):
    global velocity, velocity_reset

    # Geschwindigkeit aktualisieren
    velocity['x'] += accel_no_gravity['x'] * dt
    velocity['y'] += accel_no_gravity['y'] * dt
    velocity['z'] += accel_no_gravity['z'] * dt

# Funktion zur Winkelberechnung
def calculate_angles(accel):
    x, y, z = accel['x'], accel['y'], accel['z']
    pitch = math.degrees(math.atan2(x, math.sqrt(y**2 + z**2)))
    roll = math.degrees(math.atan2(y, math.sqrt(x**2 + z**2)))
    return roll, pitch

# Funktion zur Geschwindigkeitsrücksetzung um drift zu verhindern

def calculate_velocity_from_gyro(gyro_x, gyro_y, gyro_z, radius=0.25):
    """
    Berechnet die lineare Geschwindigkeit basierend auf der Winkelgeschwindigkeit um alle Achsen.
    
    :param gyro_x: Winkelgeschwindigkeit um die x-Achse in Grad/Sekunde
    :param gyro_y: Winkelgeschwindigkeit um die y-Achse in Grad/Sekunde
    :param gyro_z: Winkelgeschwindigkeit um die z-Achse in Grad/Sekunde
    :param radius: Radius in Metern (Standard: 0.25 m)
    :return: Lineare Geschwindigkeit in m/s
    """
    # Winkelgeschwindigkeit in Grad/s in Radiant/s umrechnen
    omega_rad = math.radians((gyro_x**2 + gyro_y**2 + gyro_z**2)**0.5)  # ω = √(ωx² + ωy² + ωz²) * π/180
    
    # Lineare Geschwindigkeit berechnen
    velocity = omega_rad * radius  # v = ω * r
    return velocity