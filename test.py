from machine import I2C, Pin
import time
import math

# I2C-Pins des ESP32 definieren
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Standard I2C-Pins (SCL=GPIO22, SDA=GPIO21)

# MPU9265 I2C-Adresse und Register
MPU_ADDRESS = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# MPU9265 aufwecken
i2c.writeto_mem(MPU_ADDRESS, PWR_MGMT_1, b'\x00')  # Schreiben von 0 in das Power-Management-Register


# Funktion zum Lesen von 16-Bit-Werten (2 Bytes) aus einem Register
def read_word(i2c, address, reg):
    high, low = i2c.readfrom_mem(address, reg, 2)
    value = (high << 8) + low
    return value if value < 0x8000 else value - 0x10000


# Funktion zum Abrufen von Beschleunigungs- und Gyroskopdaten
def get_accel_gyro(i2c):
    accel_x = read_word(i2c, MPU_ADDRESS, ACCEL_XOUT_H)
    accel_y = read_word(i2c, MPU_ADDRESS, ACCEL_XOUT_H + 2)
    accel_z = read_word(i2c, MPU_ADDRESS, ACCEL_XOUT_H + 4)
    gyro_x = read_word(i2c, MPU_ADDRESS, GYRO_XOUT_H)
    gyro_y = read_word(i2c, MPU_ADDRESS, GYRO_XOUT_H + 2)
    gyro_z = read_word(i2c, MPU_ADDRESS, GYRO_XOUT_H + 4)
    return (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)


# Hauptschleife
while True:
    accel, gyro = get_accel_gyro(i2c)[:3], get_accel_gyro(i2c)[3:]
    print(f"Accelerometer: {accel}")
    print(f"Gyroscope: {gyro}")
    time.sleep(0.5)

