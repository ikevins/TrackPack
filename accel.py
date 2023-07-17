import smbus
import time

bus = smbus.SMBus(1)
address = 0x6B

# Calibration values (obtained through calibration process)
x_offset = -4
y_offset = -1
z_offset = -0.2

while True:
    # Read accelerometer data
    accel_x = bus.read_word_data(address, 0x28)
    accel_y = bus.read_word_data(address, 0x2A)
    accel_z = bus.read_word_data(address, 0x2C)

    # Apply calibration offsets
    accel_x = (accel_x / 16384.0) - x_offset
    accel_y = (accel_y / 16384.0) - y_offset
    accel_z = (accel_z / 16384.0) - z_offset

    # Calculate the total acceleration
    acceleration = (accel_x ** 2 + accel_y ** 2 + accel_z ** 2) ** 0.5

    # Convert acceleration to g-forces
    gravity = 9.8  # Acceleration due to gravity in m/s^2
    g_forces = acceleration / gravity

    # Print the g-forces during acceleration
    print("G-Forces during acceleration: {:.2f} g".format(g_forces))

    time.sleep(0.1)  # Wait for a while before reading again
