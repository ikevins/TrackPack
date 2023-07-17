import smbus
import time

bus = smbus.SMBus(1)
address = 0x6B

# Calibration offsets
offset_x = 0.0
offset_y = 0.0
offset_z = 0.0

while True:
    # Read accelerometer data
    accel_x = bus.read_word_data(address, 0x28)
    accel_y = bus.read_word_data(address, 0x2A)
    accel_z = bus.read_word_data(address, 0x2C)

    # Apply calibration offsets
    accel_x -= offset_x
    accel_y -= offset_y
    accel_z -= offset_z

    # Convert the raw data to acceleration values
    accel_x = accel_x / 16384.0
    accel_y = accel_y / 16384.0
    accel_z = accel_z / 16384.0

    # Calculate the total acceleration
    acceleration = (accel_x ** 2 + accel_y ** 2 + accel_z ** 2) ** 0.5

    # Convert acceleration to g-forces
    gravity = 9.8  # Acceleration due to gravity in m/s^2
    g_forces = acceleration / gravity

    # Print the g-forces during acceleration
    print("G-Forces during acceleration: {:.2f} g".format(g_forces))

    time.sleep(0.1)  # Wait for a while before reading again
