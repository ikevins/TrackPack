import smbus
import time

# Create an instance of the SMBus class and define the I2C address
bus = smbus.SMBus(1)
address = 0x6B

# Enable the gyroscope
bus.write_byte_data(address, 0x10, 0x80)

while True:
    # Read gyroscope data
    gyro_x = bus.read_word_data(address, 0x22)
    gyro_y = bus.read_word_data(address, 0x24)
    gyro_z = bus.read_word_data(address, 0x26)

    # Convert the raw data to angular rate values
    gyro_x = gyro_x * 0.070  # sensitivity: 70 mdps/LSB
    gyro_y = gyro_y * 0.070
    gyro_z = gyro_z * 0.070

    # Print the gyroscope values
    print("Angular Rate (dps): X = {:.2f}, Y = {:.2f}, Z = {:.2f}".format(gyro_x, gyro_y, gyro_z))

    time.sleep(0.1)  # Wait for a while before reading again
