import smbus
import math
import time

# I2C addresses of the LSM6DSL accelerometer and LIS3MDL magnetometer
ACCEL_ADDRESS = 0x6B
MAG_ADDRESS = 0x1E

# Register addresses of the accelerometer
CTRL1_XL = 0x10
CTRL8_XL = 0x17
OUTX_L_XL = 0x28
OUTX_H_XL = 0x29
OUTY_L_XL = 0x2A
OUTY_H_XL = 0x2B
OUTZ_L_XL = 0x2C
OUTZ_H_XL = 0x2D

# Register addresses of the magnetometer
CTRL_REG1_M = 0x20
CTRL_REG2_M = 0x21
CTRL_REG3_M = 0x22
OUT_X_L_M = 0x28
OUT_X_H_M = 0x29
OUT_Y_L_M = 0x2A
OUT_Y_H_M = 0x2B
OUT_Z_L_M = 0x2C
OUT_Z_H_M = 0x2D

# Constants for gravitational acceleration
GRAVITY = 9.80665  # m/s^2
G_FORCE = GRAVITY / 1000  # g

# Initialize the I2C bus
bus = smbus.SMBus(1)  # 1 for Raspberry Pi 2 and newer

# Configure the accelerometer
bus.write_byte_data(ACCEL_ADDRESS, CTRL1_XL, 0x50)  # Set the accelerometer to 208 Hz, ±2g range
bus.write_byte_data(ACCEL_ADDRESS, CTRL8_XL, 0xC0)  # Enable high-pass filter to remove gravity offset

# Configure the magnetometer
bus.write_byte_data(MAG_ADDRESS, CTRL_REG1_M, 0x80)  # Set the magnetometer to continuous mode
bus.write_byte_data(MAG_ADDRESS, CTRL_REG2_M, 0x00)  # Set the magnetometer scale to ±4 gauss

def read_acceleration():
    # Read acceleration data from the accelerometer
    x_l = bus.read_byte_data(ACCEL_ADDRESS, OUTX_L_XL)
    x_h = bus.read_byte_data(ACCEL_ADDRESS, OUTX_H_XL)
    y_l = bus.read_byte_data(ACCEL_ADDRESS, OUTY_L_XL)
    y_h = bus.read_byte_data(ACCEL_ADDRESS, OUTY_H_XL)
    z_l = bus.read_byte_data(ACCEL_ADDRESS, OUTZ_L_XL)
    z_h = bus.read_byte_data(ACCEL_ADDRESS, OUTZ_H_XL)

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

    return g_x, g_y, g_z

def read_magnetic_field():
    # Read magnetic field data from the magnetometer
    x_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
    x_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
    y_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
    y_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
    z_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
    z_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)

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

    return x, y, z

try:
    while True:
        # Read acceleration data
        g_x, g_y, g_z = read_acceleration()

        # Calculate the total g-force
        g_total = math.sqrt(g_x ** 2 + g_y ** 2 + g_z ** 2) - 1.0  # Subtract the 1g offset

        # Read magnetic field data
        mag_x, mag_y, mag_z = read_magnetic_field()

        # Calculate the heading or direction using the magnetometer data
        heading = math.atan2(mag_y, mag_x)
        if heading < 0:
            heading += 2 * math.pi

        # Convert heading to degrees
        heading_deg = math.degrees(heading)

        # Display the acceleration, total g-force, and heading
        print(f"Acceleration: X: {g_x:.2f}g, Y: {g_y:.2f}g, Z: {g_z:.2f}g")
        print(f"Total g-force: {g_total:.2f}g")
        print(f"Heading: {heading_deg:.2f} degrees")

        # Wait for a moment
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
