#Setting Up smbus libraries
import smbus
import time
import math
bus = smbus.SMBus(1)


##############
# LIS3MDL Mag Registers #
##############
LIS3MDL_M_ADDRESS       = 0x1E
LIS3MDL_WHO_AM_I_M      = 0x0F
LIS3MDL_CTRL_REG1_M     = 0x20
LIS3MDL_CTRL_REG2_M     = 0x21
LIS3MDL_CTRL_REG3_M     = 0x22
LIS3MDL_CTRL_REG4_M     = 0x23
LIS3MDL_STATUS_REG_M        = 0x27
LIS3MDL_OUT_X_L_M       = 0x28
LIS3MDL_OUT_X_H_M       = 0x29
LIS3MDL_OUT_Y_L_M       = 0x2A
LIS3MDL_OUT_Y_H_M       = 0x2B
LIS3MDL_OUT_Z_L_M       = 0x2C
LIS3MDL_OUT_Z_H_M       = 0x2D
LIS3MDL_TEMP_OUT_L_M        = 0x2E
LIS3MDL_TEMP_OUT_H_M        = 0x2F
LIS3MDL_INT_CFG_M       = 0x30
LIS3MDL_INT_SRC_M       = 0x31
LIS3MDL_INT_THS_L_M     = 0x32
LIS3MDL_INT_THS_H_M     = 0x33

LIS3MDL_REG_CTL_1_TEMP_EN   = 0x80
LIS3MDL_REG_CTL_2_RESET     = 0x04


# mag_scale defines all possible FSR's of the magnetometer:
    
LIS3MDL_M_SCALE_4GS         = 0x20 # 00:  4Gs
LIS3MDL_M_SCALE_8GS     = 0x40 # 01:  8Gs
LIS3MDL_M_SCALE_12GS        = 0x60 # 10:  12Gs
LIS3MDL_M_SCALE_16GS        = 0x60 # 11:  16Gs
    

# mag_oder defines all possible output data rates of the magnetometer:
    
LIS3MDL_M_ODR_625       = 0x04 # 6.25 Hz 
LIS3MDL_M_ODR_125       = 0x08 # 12.5 Hz 
LIS3MDL_M_ODR_25        = 0x0C # 25 Hz 
LIS3MDL_M_ODR_5         = 0x10 # 50 
LIS3MDL_M_ODR_10        = 0x14 # 10 Hz
LIS3MDL_M_ODR_20        = 0x14 # 20 Hz
LIS3MDL_M_ODR_40        = 0x14 # 40 Hz
LIS3MDL_M_ODR_80        = 0x14 # 80 Hz 


mRes = 4.0 / 32768.0   # 4G
SENSITIVITY_OF_MIN_SCALE = 27368.0 # (4 guass scale) * (6842 LSB/guass at 4 guass scale)
Scale = 16
def initialise():
    
# initMag -- Sets up the magnetometer to begin reading.
    
    #User Register Reset Function
    bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG2_M, LIS3MDL_REG_CTL_2_RESET)
    #Temperature Sensor Enabled
    bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG1_M, LIS3MDL_REG_CTL_1_TEMP_EN )
    #Ultra High Performance Mode Selected for XY Axis
    bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG1_M, 0x60)
    #Ultra High Performance Mode Selected for Z Axis
    bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG4_M, 0x0C)
    #Output Data Rate of 80 Hz Selected
    bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG1_M, 0x1C)
    #Continous Conversion Mode,4 wire interface Selected 
    bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG3_M, 0x00)
    # 16 guass Full Scale 
    bus.write_byte_data(LIS3MDL_M_ADDRESS, LIS3MDL_CTRL_REG2_M, 0x60)
  

#Read the magnetometer output registers.
# This will read all six Magnetometer output registers.

# Reading the  Magnetometer X-Axis Values from the Register
def readMagx():
        Mag_l = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_X_L_M)
        Mag_h = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_X_H_M)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536

# Reading the  Magnetometer Y-Axis Values from the Register
def readMagy():
        Mag_l = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_Y_L_M)
        Mag_h = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_Y_H_M)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536

# Reading the  Magnetometer Z-Axis Values from the Register
def readMagz():
        Mag_l = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_Z_L_M)
        Mag_h = bus.read_byte_data(LIS3MDL_M_ADDRESS,LIS3MDL_OUT_Y_H_M)
        Mag_total = (Mag_l | Mag_h <<8)
        return Mag_total  if Mag_total < 32768 else Mag_total - 65536

def MagDataTotal():
        mtotal = (((readMagx()**2)+(readMagy()**2)+(readMagz()**2))**0.5)
        return mtotal

def getDirection(Magx, Magy, Magz):
    angle = math.degrees(math.atan2(Magy, Magx))
    if angle < 0:
        angle += 360

    if 45 <= angle < 135:
        return 'East'
    elif 135 <= angle < 225:
        return 'South'
    elif 225 <= angle < 315:
        return 'West'
    else:
        return 'North'

#Magnetic Sensitivity
'''
def Mag(SensorInterface):
            
             4 : (0x00, 27368.0)# (4 guass scale) * (6842 LSB/guass at 4 guass scale)
             8 : (0x01, 27368.0)# (8 guass scale) * (3421 LSB/guass at 8 guass scale)
             12: (0x10, 27372.0)# (12 guass scale) * (2281 LSB/guass at 12 guass scale)
             16: (0x11, 27376.0)# (16 guass scale) * (1711 LSB/guass at 16 guass scale)
'''

#Initialising the Device.
initialise()

while True:
    # Read magnetometer values
    Magx = readMagx()
    Magy = readMagy()
    Magz = readMagz()
    Mtotal = MagDataTotal()

    # Convert magnetometer readings to Gauss
    Mtotal = Mtotal * Scale / SENSITIVITY_OF_MIN_SCALE

    # Get the direction
    direction = getDirection(Magx, Magy, Magz)

    # Print the magnetometer readings and direction
    print("\nMagnetometer Readings:")
    print("Mag X-Axis:", Magx, "Mag Y-Axis:", Magy, "Mag Z-Axis:", Magz)
    print("Mag X:", Magx * Scale / SENSITIVITY_OF_MIN_SCALE, "Gauss")
    print("Mag Y:", Magy * Scale / SENSITIVITY_OF_MIN_SCALE, "Gauss")
    print("Mag Z:", Magz * Scale / SENSITIVITY_OF_MIN_SCALE, "Gauss")
    print("Mtotal:", Mtotal, "Gauss")
    print("Direction:", direction)

    time.sleep(0.5)
