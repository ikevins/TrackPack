from picamera import PiCamera
import time
camera = PiCamera()
time.sleep(2)
camera.resolution = (1280, 720)
camera.vflip = False
camera.contrast = 10
file_name = "/home/ikevins/Desktop/testvideo.h264"
print("Start recording...")
camera.start_recording(file_name)
camera.wait_recording(5)
camera.stop_recording()
print("Done.")
