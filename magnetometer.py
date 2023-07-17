import smbus
import math
import time

# Define I2C address
DEVICE_ADDRESS = 0x1E

# Register addresses
OUT_X_L = 0x03
OUT_X_H = 0x04
OUT_Y_L = 0x05
OUT_Y_H = 0x06

# Magnetometer calibration values (update with your own)
CALIBRATION_X_MIN = -300
CALIBRATION_X_MAX = 300
CALIBRATION_Y_MIN = -300
CALIBRATION_Y_MAX = 300

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
    # Perform magnetometer calibration
    print("Performing magnetometer calibration...")
    x_min = y_min = float('inf')
    x_max = y_max = float('-inf')
    calibration_samples = 200

    for _ in range(calibration_samples):
        x = read_data(OUT_X_L)
        y = read_data(OUT_Y_L)

        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)

        time.sleep(0.01)

    # Apply calibration values
    CALIBRATION_X_MIN = x_min
    CALIBRATION_X_MAX = x_max
    CALIBRATION_Y_MIN = y_min
    CALIBRATION_Y_MAX = y_max

    print("Calibration complete.")
    print("X min:", CALIBRATION_X_MIN)
    print("X max:", CALIBRATION_X_MAX)
    print("Y min:", CALIBRATION_Y_MIN)
    print("Y max:", CALIBRATION_Y_MAX)
    print("")

    while True:
        # Read magnetometer data
        x = read_data(OUT_X_L)
        y = read_data(OUT_Y_L)

        # Apply calibration offsets
        x -= (CALIBRATION_X_MAX + CALIBRATION_X_MIN) / 2
        y -= (CALIBRATION_Y_MAX + CALIBRATION_Y_MIN) / 2

        # Get direction
        direction = get_direction(x, y)

        # Print the direction
        print("Direction:", direction)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated by user")
