import smbus
import math
import time

# Create an instance of the SMBus class and define the I2C address
bus = smbus.SMBus(1)
address = 0x1E

# Configure the sensor for continuous conversion mode
bus.write_byte_data(address, 0x20, 0x00)  # Set configuration register to continuous conversion mode

# Calibration values (adjust as needed)
offset_x = 0.0
offset_y = 0.0

while True:
    # Read magnetometer data
    mag_x = bus.read_word_data(address, 0x28)
    mag_y = bus.read_word_data(address, 0x2A)
    mag_z = bus.read_word_data(address, 0x2C)

    # Apply offset and convert the raw data to magnetic field values
    mag_x = (mag_x * 0.00014) - offset_x  # sensitivity: 0.14 µT/LSB
    mag_y = (mag_y * 0.00014) - offset_y
    mag_z = mag_z * 0.00014

    # Calculate the heading or direction
    heading = math.atan2(mag_y, mag_x)
    if heading < 0:
        heading += 2 * math.pi

    # Convert heading to degrees
    heading_degrees = math.degrees(heading)

    # Print the heading in degrees
    print("Heading: {:.2f} degrees".format(heading_degrees))

    time.sleep(0.1)  # Wait for a while before reading again
