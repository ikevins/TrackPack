import smbus2
import time
import math

# Create an instance of the SMBus class
bus = smbus2.SMBus(1)

# Define the I2C address
address = 0x1E

# Configure the sensor for continuous conversion mode
bus.write_byte_data(address, 0x20, 0x00)  # Set configuration register to continuous conversion mode

while True:
    # Read magnetometer data
    mag_x_low = bus.read_byte_data(address, 0x28)
    mag_x_high = bus.read_byte_data(address, 0x29)
    mag_y_low = bus.read_byte_data(address, 0x2A)
    mag_y_high = bus.read_byte_data(address, 0x2B)
    mag_z_low = bus.read_byte_data(address, 0x2C)
    mag_z_high = bus.read_byte_data(address, 0x2D)

    # Convert the raw data to signed integers
    mag_x = (mag_x_high << 8) | mag_x_low
    mag_y = (mag_y_high << 8) | mag_y_low
    mag_z = (mag_z_high << 8) | mag_z_low
    mag_x = mag_x if mag_x < 32768 else mag_x - 65536
    mag_y = mag_y if mag_y < 32768 else mag_y - 65536
    mag_z = mag_z if mag_z < 32768 else mag_z - 65536

    # Convert the magnetometer data to magnetic field values
    mag_x = mag_x * 0.00014  # sensitivity: 0.14 Gauss/LSB
    mag_y = mag_y * 0.00014
    mag_z = mag_z * 0.00014

    # Calculate the heading angle
    heading = math.atan2(mag_y, mag_x)
    if heading < 0:
        heading += 2 * math.pi

    # Convert the heading angle to degrees
    heading_degrees = math.degrees(heading)

    # Adjust the heading degrees to be in the range of 0-360
    if heading_degrees < 0:
        heading_degrees += 360

    # Determine the cardinal direction
    if 45 <= heading_degrees < 135:
        direction = "East"
    elif 135 <= heading_degrees < 225:
        direction = "South"
    elif 225 <= heading_degrees < 315:
        direction = "West"
    else:
        direction = "North"

    # Print the heading and direction
    print("Heading: {:.2f} degrees".format(heading_degrees))
    print("Direction: {}".format(direction))

    time.sleep(0.1)  # Wait for a while before reading again
