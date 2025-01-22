from machine import I2C

class MPU6050:
    # MPU6050 I2C addresses and registers
    MPU6050_ADDR = 0x68  # Default I2C address for MPU6050
    PWR_MGMT_1 = 0x6B  # Power management register
    ACCEL_XOUT_H = 0x3B  # Starting register for accelerometer data
    GYRO_XOUT_H = 0x43  # Starting register for gyroscope data
    TEMP_OUT_H = 0x41  # Starting register for temperature data

    def __init__(self, i2c, addr=MPU6050_ADDR):
        """
        Initialize the MPU6050 sensor.

        :param i2c: Initialized I2C object
        :param addr: I2C address of the MPU6050
        """
        self.i2c = i2c
        self.addr = addr

        # Wake up the sensor (clear sleep mode)
        self.i2c.writeto_mem(self.addr, self.PWR_MGMT_1, b'\x00')

    def read_raw_data(self, register):
        """
        Read raw 16-bit data from the given register.

        :param register: Register address to read from
        :return: Signed 16-bit integer value
        """
        high = self.i2c.readfrom_mem(self.addr, register, 1)[0]
        low = self.i2c.readfrom_mem(self.addr, register + 1, 1)[0]
        value = (high << 8) | low

        # Convert to signed 16-bit integer
        if value > 32767:
            value -= 65536
        return value

    def get_accel(self):
        """
        Get the accelerometer readings for X, Y, Z axes.

        :return: Dictionary with accelerometer readings in 'g'
        """
        accel_scale = 16384.0  # Sensitivity scale factor (default ±2g)
        return {
            'x': self.read_raw_data(self.ACCEL_XOUT_H) / accel_scale,
            'y': self.read_raw_data(self.ACCEL_XOUT_H + 2) / accel_scale,
            'z': self.read_raw_data(self.ACCEL_XOUT_H + 4) / accel_scale
        }

    def get_gyro(self):
        """
        Get the gyroscope readings for X, Y, Z axes.

        :return: Dictionary with gyroscope readings in degrees/second
        """
        gyro_scale = 131.0  # Sensitivity scale factor (default ±250°/s)
        return {
            'x': self.read_raw_data(self.GYRO_XOUT_H) / gyro_scale,
            'y': self.read_raw_data(self.GYRO_XOUT_H + 2) / gyro_scale,
            'z': self.read_raw_data(self.GYRO_XOUT_H + 4) / gyro_scale
        }

    def get_temperature(self):
        """
        Get the temperature reading from the MPU6050.

        :return: Temperature in degrees Celsius
        """
        raw_temp = self.read_raw_data(self.TEMP_OUT_H)
        return raw_temp / 340.0 + 36.53  # Temperature formula from the datasheet
    

    
