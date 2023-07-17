import smbus
import math
import time

# I2C address of the LSM6DSL accelerometer
ACCELEROMETER_I2C_ADDRESS = 0x6B

# I2C address of the LIS3MDL magnetometer
MAGNETOMETER_I2C_ADDRESS = 0x1E

# Register addresses of the accelerometer
ACCELEROMETER_CTRL_REG1 = 0x10
ACCELEROMETER_CTRL_REG8 = 0x17
ACCELEROMETER_OUTX_L = 0x28
ACCELEROMETER_OUTX_H = 0x29
ACCELEROMETER_OUTY_L = 0x2A
ACCELEROMETER_OUTY_H = 0x2B
ACCELEROMETER_OUTZ_L = 0x2C
ACCELEROMETER_OUTZ_H = 0x2D

# Register addresses of the magnetometer
MAGNETOMETER_CTRL_REG1 = 0x20
MAGNETOMETER_CTRL_REG2 = 0x21
MAGNETOMETER_CTRL_REG3 = 0x22
MAGNETOMETER_CTRL_REG4 = 0x23
MAGNETOMETER_OUTX_L = 0x28
MAGNETOMETER_OUTX_H = 0x29
MAGNETOMETER_OUTY_L = 0x2A
MAGNETOMETER_OUTY_H = 0x2B
MAGNETOMETER_OUTZ_L = 0x2C
MAGNETOMETER_OUTZ_H = 0x2D

# Configure the accelerometer
bus.write_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_CTRL_REG1, 0x50) # Set the accelerometer to 208 Hz, ±2g range
bus.write_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_CTRL_REG8, 0xC0) # Enable high-pass filter to remove gravity offset

# Configure the magnetometer
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG2, 0x04) # Configure the Magnetometer
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG1, 0x80) # Sensor Enabled
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG1, 0x60) # Ultra High Performance Mode Selected for XY Axis
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG4, 0x0C) # Ultra High Performance Mode Selected for Z Axis
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG1, 0x1C) # Output Data Rate of 80 Hz Selected
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG3, 0x00) # Continous Conversion Mode, 4 wire interface Selected
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG2, 0x60) # 16 guass Full Scale

# Initialize the I2C bus
bus = smbus.SMBus(1) #1 for Raspberry Pi 2 and newer

# Constants for gravitational acceleration
GRAVITY = 9.80665  # m/s^2
G_FORCE = GRAVITY / 1000  # g

try:
    while True:
        # Read acceleration data from the accelerometer
        accelerometer_x_l = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTX_L)
        accelerometer_x_h = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTX_H)
        accelerometer_y_l = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTY_L)
        accelerometer_y_h = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTY_H)
        accelerometer_z_l = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTZ_L)
        accelerometer_z_h = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTZ_H)

        # Read acceleration data from the accelerometer
        magnetometer_x_l = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTX_L)
        magnetometer_x_h = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTX_H)
        magnetometer_y_l = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTY_L)
        magnetometer_y_h = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTY_H)
        magnetometer_z_l = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTZ_L)
        magnetometer_z_h = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTZ_H)

        # Convert the raw data to signed 16-bit values
        accelerometer_x = (accelerometer_x_h << 8 | accelerometer_x_l)
        if accelerometer_x > 32767:
            accelerometer_x -= 65536

        accelerometer_y = (accelerometer_y_h << 8 | accelerometer_y_l)
        if accelerometer_y > 32767:
            accelerometer_y -= 65536

        accelerometer_z = (accelerometer_z_h << 8 | accelerometer_z_l)
        if accelerometer_z > 32767:
            accelerometer_z -= 65536

        magnetometer_x = (magnetometer_x_h << 8 | magnetometer_x_l)
        if magnetometer_x > 32767:
            magnetometer_x -= 65536

        magnetometer_y = (magnetometer_y_h << 8 | magnetometer_y_l)
        if magnetometer_y > 32767:
            magnetometer_y -= 65536

        magnetometer_z = (magnetometer_z_h << 8 | magnetometer_z_l)
        if magnetometer_z > 32767:
            magnetometer_z -= 65536

        # Calculate the g-force in each axis
        g_x = accelerometer_x / 16384.0
        g_y = accelerometer_y / 16384.0
        g_z = accelerometer_z / 16384.0

        # Calculate the total g-force
        g_total = math.sqrt(g_x ** 2 + g_y ** 2 + g_z ** 2) - 1.0  # Subtract the 1g offset

        # Display only positive g-force values
        g_total = max(0, g_total)

        # Calculate the direction
        direction = ""
        angle = math.degrees(math.atan2(x, y))
        if angle < 0:
            angle += 360
        if 45 <= angle < 135:
            direction = "East"
        elif 135 <= angle < 225:
            direction = "South"
        elif 225 <= angle < 315:
            direction = "West"
        else:
            direction = "North"

        print("Direction:", direction)

        print(f"X: {g_x:.2f}g, Y: {g_y:.2f}g, Z: {g_z:.2f}g, Total: {g_total:.1f}g")

        # Wait for a moment
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
