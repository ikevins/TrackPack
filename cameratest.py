from picamera import PiCamera
import time
import os
camera = PiCamera()
time.sleep(2)
camera.resolution = (1280, 720)
camera.rotation = 270
camera.start_recording("/home/ikevins/Desktop/testvideo.h264")
camera.wait_recording(5)
camera.stop_recording()

os.system("MP4Box -add testvideo.h264 convertedVideo.mp4")
