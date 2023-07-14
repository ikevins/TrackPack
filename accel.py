import smbus
import time
from math import sqrt

bus = smbus.SMBus(1)
address = 0x6B

# Kalman filter variables
Q = 0.001  # Process noise covariance
R = 0.1  # Measurement noise covariance
x = 0  # Initial state estimate
P = 1  # Initial state covariance

def kalman_filter(z):
    global x, P
    # Prediction
    x_pred = x
    P_pred = P + Q

    # Kalman gain
    K = P_pred / (P_pred + R)

    # Update
    x = x_pred + K * (z - x_pred)
    P = (1 - K) * P_pred

    return x

while True:
    # Read accelerometer data
    accel_z = bus.read_word_data(address, 0x2C)

    # Convert raw data to acceleration value
    accel_z = accel_z / 16384.0

    # Apply Kalman filter
    filtered_accel_z = kalman_filter(accel_z)

    # Calculate the total acceleration
    acceleration = sqrt(filtered_accel_z ** 2)

    # Convert acceleration to g-forces
    gravity = 9.8  # Acceleration due to gravity in m/s^2
    g_forces = acceleration / gravity

    # Print the g-forces during acceleration
    print("G-Forces during acceleration: {:.2f} g".format(g_forces))

    time.sleep(0.1)  # Wait for a while before reading again
