import smbus
import time

bus = smbus.SMBus(1)
address = 0x1E

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

    # Print the magnetic field values
    print("Magnetic Field (µT): X = {:.2f}, Y = {:.2f}, Z = {:.2f}".format(mag_x, mag_y, mag_z))

    time.sleep(0.1)  # Wait for a while before reading again
