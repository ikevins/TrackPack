import smbus

bus = smbus.SMBus(1)  # Use 0 for older Raspberry Pi boards

# LSM6DSL I2C address
address = 0x6A

# Accelerometer and gyroscope registers
acc_reg = 0x28
gyro_reg = 0x22

# Read accelerometer data
acc_data = bus.read_i2c_block_data(address, acc_reg, 6)

# Read gyroscope data
gyro_data = bus.read_i2c_block_data(address, gyro_reg, 6)

# Process and print the data
print("Accelerometer: ", acc_data)
print("Gyroscope: ", gyro_data)
