import smbus
import math
import time

# I2C address of the LSM6DSL accelerometer
I2C_ADDRESS = 0x6B

# Register addresses of the accelerometer
CTRL1_XL = 0x10
CTRL8_XL = 0x17
OUTX_L_XL = 0x28
OUTX_H_XL = 0x29
OUTY_L_XL = 0x2A
OUTY_H_XL = 0x2B
OUTZ_L_XL = 0x2C
OUTZ_H_XL = 0x2D

# Constants for gravitational acceleration
GRAVITY = 9.80665  # m/s^2
G_FORCE = GRAVITY / 1000  # g

# Initialize the I2C bus
bus = smbus.SMBus(1)  # 1 for Raspberry Pi 2 and newer

# Configure the accelerometer
bus.write_byte_data(I2C_ADDRESS, CTRL1_XL, 0x50)  # Set the accelerometer to 208 Hz, ±2g range
bus.write_byte_data(I2C_ADDRESS, CTRL8_XL, 0xC0)  # Enable high-pass filter to remove gravity offset

try:
    while True:
        # Read acceleration data from the accelerometer
        x_l = bus.read_byte_data(I2C_ADDRESS, OUTX_L_XL)
        x_h = bus.read_byte_data(I2C_ADDRESS, OUTX_H_XL)
        y_l = bus.read_byte_data(I2C_ADDRESS, OUTY_L_XL)
        y_h = bus.read_byte_data(I2C_ADDRESS, OUTY_H_XL)
        z_l = bus.read_byte_data(I2C_ADDRESS, OUTZ_L_XL)
        z_h = bus.read_byte_data(I2C_ADDRESS, OUTZ_H_XL)

        # Convert the raw data to signed 16-bit values
        x = (x_h << 8 | x_l)
        if x > 32767:
            x -= 65536

        y = (y_h << 8 | y_l)
        if y > 32767:
            y -= 65536

        z = (z_h << 8 | z_l)
        if z > 32767:
            z -= 65536

        # Calculate the g-force in each axis
        g_x = x / 16384.0
        g_y = y / 16384.0
        g_z = z / 16384.0

        # Calculate the total g-force
        g_total = math.sqrt(g_x ** 2 + g_y ** 2 + g_z ** 2) - 1.0  # Subtract the 1g offset

        # Display only positive g-force values
        g_total = max(0, g_total)

        # Print the g-force values
        print(f"X: {g_x:.2f}g, Y: {g_y:.2f}g, Z: {g_z:.2f}g, Total: {g_total:.1f}g")

        # Wait for a moment
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
