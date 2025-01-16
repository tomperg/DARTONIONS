import math

def calculate_yaw(x, y, z):
    yaw = math.atan2(y, x)
    return math.degrees(yaw)