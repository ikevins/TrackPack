import smbus

# I2C address of the LSM6DSL
DEVICE_ADDRESS = 0x6B

# LSM6DSL registers
WHO_AM_I_REG = 0x0F
CTRL1_XL_REG = 0x10
CTRL2_G_REG = 0x11
OUTX_L_XL_REG = 0x28
OUTY_L_XL_REG = 0x2A
OUTZ_L_XL_REG = 0x2C
OUTX_L_G_REG = 0x22
OUTY_L_G_REG = 0x24
OUTZ_L_G_REG = 0x26

# Initialize the I2C bus
bus = smbus.SMBus(1)

def read_byte(reg):
    return bus.read_byte_data(DEVICE_ADDRESS, reg)

def read_word(reg):
    high_byte = bus.read_byte_data(DEVICE_ADDRESS, reg)
    low_byte = bus.read_byte_data(DEVICE_ADDRESS, reg + 1)
    value = (high_byte << 8) | low_byte
    return value

def read_acceleration():
    x = read_word(OUTX_L_XL_REG)
    y = read_word(OUTY_L_XL_REG)
    z = read_word(OUTZ_L_XL_REG)
    return (x, y, z)

def read_gyroscope():
    x = read_word(OUTX_L_G_REG)
    y = read_word(OUTY_L_G_REG)
    z = read_word(OUTZ_L_G_REG)
    return (x, y, z)

# Check the device ID
who_am_i = read_byte(WHO_AM_I_REG)
if who_am_i != 0x6A:
    raise ValueError("LSM6DSL not found at address 0x6B.")

# Configure the accelerometer and gyroscope
bus.write_byte_data(DEVICE_ADDRESS, CTRL1_XL_REG, 0x60)  # Accelerometer: 208 Hz, ±2 g
bus.write_byte_data(DEVICE_ADDRESS, CTRL2_G_REG, 0x60)   # Gyroscope: 208 Hz, ±2000 dps

# Read and print sensor data
acceleration = read_acceleration()
gyroscope = read_gyroscope()
print("Acceleration (mg): X = {}, Y = {}, Z = {}".format(*acceleration))
print("Gyroscope (dps): X = {}, Y = {}, Z = {}".format(*gyroscope))
