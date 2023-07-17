#Setting Up smbus libraries
import smbus
import time
import math
bus = smbus.SMBus(1)

LIS3MDL_M_ADDRESS = 0x1E

LIS3MDL_CTRL_REG1_M = 0x20
LIS3MDL_CTRL_REG2_M = 0x21
LIS3MDL_CTRL_REG3_M = 0x22
LIS3MDL_CTRL_REG4_M = 0x23
LIS3MDL_OUT_X_L_M = 0x28
LIS3MDL_OUT_X_H_M = 0x29
LIS3MDL_OUT_Y_L_M = 0x2A
LIS3MDL_OUT_Y_H_M = 0x2B
LIS3MDL_OUT_Z_L_M = 0x2C
LIS3MDL_OUT_Z_H_M = 0x2D
LIS3MDL_REG_CTL_1_TEMP_EN = 0x80
LIS3MDL_REG_CTL_2_RESET = 0x04

# Configure the Magnetometer
bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG2_M, LIS3MDL_REG_CTL_2_RESET)
# Sensor Enabled
bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG1_M, LIS3MDL_REG_CTL_1_TEMP_EN )
#Ultra High Performance Mode Selected for XY Axis
bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG1_M, 0x60)
#Ultra High Performance Mode Selected for Z Axis
bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG4_M, 0x0C)
#Output Data Rate of 80 Hz Selected
bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG1_M, 0x1C)
#Continous Conversion Mode, 4 wire interface Selected
bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG3_M, 0x00)
# 16 guass Full Scale
bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG2_M, 0x60)

try:
    while True:

        x_l = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_X_L_M)
        x_h = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_X_H_M)
        y_l = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_Y_L_M)
        y_h = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_Y_H_M)
        z_l = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_Z_L_M)
        z_h = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_Z_H_M)

        # Convert the raw data to signed 16-bit values
        x = (x_h << 8 | x_l)
        if x > 32767:
            x -= 65536

        y = (y_h << 8 | y_l)
        if y > 32767:
            y -= 65536

        z = (z_h << 8 | z_l)
        if z > 32767:
            z -= 65536

        direction = ""
        # Calculate the direction
        angle = math.degrees(math.atan2(x, y))
        if angle < 0:
            angle += 360
        if 45 <= angle < 135:
            direction = "East"
        elif 135 <= angle < 225:
            direction = "South"
        elif 225 <= angle < 315:
            direction = "West"
        else:
            direction = "North"

        print("Direction:", direction)

        # Wait for a moment
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
