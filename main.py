#I2C initialisieren
i2c = I2C(0,sda=Pin(21), scl=Pin(22))
imu = ADXL345_I2C(i2c)


