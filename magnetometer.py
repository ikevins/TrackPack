import smbus
import time
import math

bus = smbus.SMBus(1)

# Magnetometer registers and constants
# ...

# Magnetic sensitivity and scale
# ...

def initialise():
    # Initialize the magnetometer
    # ...

def readMagx():
    # Read magnetometer X-axis value
    # ...

def readMagy():
    # Read magnetometer Y-axis value
    # ...

def readMagz():
    # Read magnetometer Z-axis value
    # ...

def MagDataTotal():
    # Calculate total magnetic field strength
    # ...

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

# Initialize the device
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

    print("****************************")
    time.sleep(0.5)
