import smbus

# Define LSM6DSL registers
CTRL1_XL = 0x10  # Control register for accelerometer
OUTX_L_XL = 0x28  # Output register for accelerometer data (X-axis)

# Initialize I2C bus (replace 1 with the appropriate bus number)
bus = smbus.SMBus(1)

# Set the device address (6B in your case)
address = 0x6B

# Configure LSM6DSL
bus.write_byte_data(address, CTRL1_XL, 0x80)  # Enable accelerometer

# Read accelerometer data
data_x_l = bus.read_byte_data(address, OUTX_L_XL)
data_x_h = bus.read_byte_data(address, OUTX_L_XL + 1)
acceleration = (data_x_h << 8) | data_x_l

print(f"Acceleration: {acceleration}")
