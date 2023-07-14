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
    mag_x = bus.read_word_data(address, 0x28)
    mag_y = bus.read_word_data(address, 0x2A)
    mag_z = bus.read_word_data(address, 0x2C)

    # Convert the raw data to magnetic field values
    mag_x = mag_x * 0.00014  # sensitivity: 0.14 µT/LSB
    mag_y = mag_y * 0.00014
    mag_z = mag_z * 0.00014

    # Calculate the heading angle
    heading = math.atan2(mag_y, mag_x)
    if heading < 0:
        heading += 2 * math.pi

    # Convert the heading angle to degrees
    heading_degrees = math.degrees(heading)

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
