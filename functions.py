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
def calculate_angles(self):
    current_time = time.ticks_ms()
    dt = (current_time - self.last_time) / 1000.0  # Zeitdifferenz in Sekunden
    self.last_time = current_time

    gyro_data = self.get_gyro()
    self.gyro_angle_x += gyro_data['x'] * dt
    self.gyro_angle_y += gyro_data['y'] * dt
    accel_roll, accel_pitch = self.get_accel_angle()

    # Gyro & Accelerometer kombinieren (Complementary Filter)
    #         alpha = 0.96  # Gewichtung des Gyroskops (zwischen 0 und 1)
    roll = alpha * (self.gyro_angle_x) + (1 - alpha) * accel_roll
    pitch = alpha * (self.gyro_angle_y) + (1 - alpha) * accel_pitch

    return roll, pitch
# Funktion zur Geschwindigkeitsrücksetzung um drift zu verhindern

def complementary_filter(gyro, accel, alpha=0.98, dt=0.01):
    """
    Kombiniert Gyroskop- und Accelerometer-Daten für einen stabileren Winkel.
    :param gyro: Gyro-Daten als Dictionary {"x":, "y":, "z":}
    :param accel: Accelerometer-Daten als Dictionary {"x":, "y":, "z":}
    :param alpha: Gewichtung (0.98 bedeutet 98% Gyro, 2% Accel)
    :param dt: Zeitschritt in Sekunden (z.B. 0.01 für 10ms)
    :return: Stabiler Roll-Winkel in Grad
    """
    roll_accel = math.degrees(math.atan2(accel["y"], accel["z"]))  # Absoluter Winkel aus Accelerometer
    roll_gyro = gyro["x"] * dt  # Winkeländerung aus Gyroskop

    # Complementary Filter: Kombiniere beide Werte
    roll = alpha * (roll_gyro) + (1 - alpha) * roll_accel
    return roll

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