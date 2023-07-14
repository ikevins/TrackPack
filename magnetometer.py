import smbus
import time
import math

# Create an instance of the SMBus class and define the I2C address
bus = smbus.SMBus(1)
address = 0x1E

# Configure the sensor for continuous conversion mode
bus.write_byte_data(address, 0x20, 0x00)  # Set configuration register to continuous conversion mode

while True:
    # Read magnetometer data
    mag_x = bus.read_word_data(address, 0x28) | (bus.read_byte_data(address, 0x29) << 8)
    mag_y = bus.read_word_data(address, 0x2A) | (bus.read_byte_data(address, 0x2B) << 8)
    mag_z = bus.read_word_data(address, 0x2C) | (bus.read_byte_data(address, 0x2D) << 8)

    # Convert the raw data to signed integers
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
