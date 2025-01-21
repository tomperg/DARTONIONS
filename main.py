from machine import Pin, I2C
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
MPU9265_ADDR = 0x68
ACCEL_XOUT_H = 0x3B

def bytes_to_int(msb, lsb):
    """Konvertiert zwei Bytes in einen signed int16"""
    value = (msb << 8) | lsb
    if value >= 0x8000:
        value -= 0x10000
    return value

try:
    while True:
        # 6 Bytes für acc_x, acc_y, acc_z lesen
        data = i2c.readfrom_mem(MPU9265_ADDR, ACCEL_XOUT_H, 6)
        
        # Rohdaten in g-Werte umrechnen
        acc_scale = 1.0/16384.0  # für ±2g Bereich
        
        ax = bytes_to_int(data[0], data[1]) * acc_scale
        ay = bytes_to_int(data[2], data[3]) * acc_scale
        az = bytes_to_int(data[4], data[5]) * acc_scale
        
        print(f"Acc X: {ax:7.2f}g  Y: {ay:7.2f}g  Z: {az:7.2f}g")
        time.sleep_ms(100)

except KeyboardInterrupt:
    print("Gestoppt")
except Exception as e:
    print("Fehler:", e)