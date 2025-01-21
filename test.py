import smbus2
import time
import math

# I2C-Adresse des MPU9265
MPU_ADDRESS = 0x68

# Register-Adressen
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# I2C-Schnittstelle initialisieren
bus = smbus2.SMBus(1)

# MPU9265 aufwecken
bus.write_byte_data(MPU_ADDRESS, PWR_MGMT_1, 0)

def read_word(bus, address, reg):
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg + 1)
    value = (high << 8) + low
    return value if value < 0x8000 else value - 0x10000

def get_accel_gyro(bus):
    accel_x = read_word(bus, MPU_ADDRESS, ACCEL_XOUT_H)
    accel_y = read_word(bus, MPU_ADDRESS, ACCEL_XOUT_H + 2)
    accel_z = read_word(bus, MPU_ADDRESS, ACCEL_XOUT_H + 4)
    gyro_x = read_word(bus, MPU_ADDRESS, GYRO_XOUT_H)
    gyro_y = read_word(bus, MPU_ADDRESS, GYRO_XOUT_H + 2)
    gyro_z = read_word(bus, MPU_ADDRESS, GYRO_XOUT_H + 4)
    return (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)

while True:
    accel, gyro = get_accel_gyro(bus)[:3], get_accel_gyro(bus)[3:]
    print(f"Accelerometer: {accel}")
    print(f"Gyroscope: {gyro}")
    time.sleep(0.5)
