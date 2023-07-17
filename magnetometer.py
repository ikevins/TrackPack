import smbus
import math

# Define I2C address
DEVICE_ADDRESS = 0x1E

# Register addresses
OUT_X_L = 0x03
OUT_X_H = 0x04
OUT_Y_L = 0x05
OUT_Y_H = 0x06

# Initialize I2C bus
bus = smbus.SMBus(1)

def read_data(register):
    # Read 16-bit little-endian data from the specified register
    low_byte = bus.read_byte_data(DEVICE_ADDRESS, register)
    high_byte = bus.read_byte_data(DEVICE_ADDRESS, register + 1)
    value = (high_byte << 8) | low_byte

    # Convert to signed value
    if value & 0x8000:
        value = -(value & 0x7FFF)

    return value

def get_direction(x, y):
    # Calculate the direction based on x and y values
    angle = math.atan2(y, x)
    angle = math.degrees(angle)

    if angle < 0:
        angle += 360

    if angle >= 45 and angle < 135:
        return "E"
    elif angle >= 135 and angle < 225:
        return "S"
    elif angle >= 225 and angle < 315:
        return "W"
    else:
        return "N"

try:
    while True:
        # Read magnetometer data
        x = read_data(OUT_X_L)
        y = read_data(OUT_Y_L)

        # Get direction
        direction = get_direction(x, y)

        # Print the direction
        print("Direction:", direction)

except KeyboardInterrupt:
    print("Program terminated by user")
