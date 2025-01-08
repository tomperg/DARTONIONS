import math
def calculate_angles(x, y, z):
    # Berechne Pitch und Roll
    pitch = degrees(atan2(x, sqrt(y**2 + z**2)))
    roll = degrees(atan2(y, sqrt(x**2 + z**2)))
    return pitch, roll