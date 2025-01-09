import math

def calculate_angles(x, y, z):
    # Berechne Pitch und Roll
    pitch = math.degrees(math.atan2(x, math.sqrt(y**2 + z**2)))
    roll = math.degrees(math.atan2(y, math.sqrt(x**2 + z**2)))
    return pitch, roll