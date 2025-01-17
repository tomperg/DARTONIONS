import math

def calculate_yaw(x, y):
    yaw = math.atan2(y, x)
    return math.degrees(yaw)