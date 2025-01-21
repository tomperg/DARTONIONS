from machine import Pin, I2C
import time
import mpu9250

# I2C initialisieren
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)  # SCL auf GPIO22, SDA auf GPIO21

# MPU9250 initialisieren
imu = mpu9250.MPU9250(i2c)

# Warten, bis der Sensor stabil ist
time.sleep(1)

while True:
    # Auslesen der Beschleunigungs- und Gyroskopdaten
    accel = imu.accel
    gyro = imu.gyro
    mag = imu.mag

    # Ausgabe der Sensordaten
    print("Accelerometer:", accel)
    print("Gyroscope:", gyro)
    print("Magnetometer:", mag)
    
    # Kurze Pause
    time.sleep(1)
