import smbus
import time

bus = smbus.SMBus(1)
address = 0x6B

calibration_duration = 5  # Duration of calibration process in seconds
sample_delay = 0.1  # Delay between accelerometer samples in seconds

num_samples = calibration_duration / sample_delay

x_sum = 0
y_sum = 0
z_sum = 0

for _ in range(int(num_samples)):
    # Read accelerometer data
    accel_x = bus.read_word_data(address, 0x28)
    accel_y = bus.read_word_data(address, 0x2A)
    accel_z = bus.read_word_data(address, 0x2C)

    # Accumulate the sum of readings
    x_sum += accel_x
    y_sum += accel_y
    z_sum += accel_z

    time.sleep(sample_delay)

# Calculate the average values
x_avg = x_sum / num_samples
y_avg = y_sum / num_samples
z_avg = z_sum / num_samples

# Calculate the offset values
x_offset = -x_avg / 16384.0
y_offset = -y_avg / 16384.0
z_offset = -z_avg / 16384.0

print("Calibration complete.")
print("x_offset: {:.4f}".format(x_offset))
print("y_offset: {:.4f}".format(y_offset))
print("z_offset: {:.4f}".format(z_offset))
