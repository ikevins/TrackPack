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

    # Print the acceleration values
    print("Acceleration (g): X = {:.2f}, Y = {:.2f}, Z = {:.2f}".format(accel_x, accel_y, accel_z))

    time.sleep(0.1)  # Wait for a while before reading again
