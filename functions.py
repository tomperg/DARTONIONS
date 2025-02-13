import math 
import time 

#Filter welcher roll aus Gyro und Accelermeter berechnet um Winkel weniger von beschleunigung der Hand zu beeinflussen
def complementary_filter(gyro, accel, alpha=0.98, dt=0.01):
    roll_accel = math.degrees(math.atan2(accel["y"], accel["z"]))  # Absoluter Winkel aus Accelerometer
    roll_gyro = gyro["x"] * dt  # Winkeländerung aus Gyroskop

    # Complementary Filter: Kombiniere beide Werte
    roll = alpha * (roll_gyro) + (1 - alpha) * roll_accel
    return roll

def calculate_velocity_from_gyro(gyro_x, gyro_y, gyro_z, radius=0.25):
    # Winkelgeschwindigkeit in Grad/s in Radiant/s umrechnen
    omega_rad = math.radians((gyro_x**2 + gyro_y**2 + gyro_z**2)**0.5)  # ω = √(ωx² + ωy² + ωz²) * π/180
    
    # Lineare Geschwindigkeit berechnen
    velocity = omega_rad * radius  # v = ω * r
    return velocity