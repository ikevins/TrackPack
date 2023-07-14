import smbus
import time

bus = smbus.SMBus(1)
address = 0x6B

while True:
    # Read accelerometer data
    accel_x = bus.read_word_data(address, 0x28)
    accel_y = bus.read_word_data(address, 0x2A)
    accel_z = bus.read_word_data(address, 0x2C)

    # Convert the raw data to acceleration values
    accel_x = accel_x / 16384.0
    accel_y = accel_y / 16384.0
    accel_z = accel_z / 16384.0

    # Convert acceleration values to force in "g"
    gravity = 9.8  # Acceleration due to gravity in m/s^2
    force_x = accel_x / gravity
    force_y = accel_y / gravity
    force_z = accel_z / gravity

    # Print the force values
    print("Force (g): X = {:.2f}, Y = {:.2f}, Z = {:.2f}".format(force_x, force_y, force_z))

    time.sleep(0.1)  # Wait for a while before reading again
