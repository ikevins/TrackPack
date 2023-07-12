from picamera import PiCamera
import time
camera = PiCamera()
time.sleep(2)
camera.resolution = (1280, 720)
camera.vflip = False
camera.contrast = 10
camera.start_recording(/home/ikevins/Desktop/testvideo.h264)
#camera.wait_recording(5)
camera.stop_recording()

# Define the command we want to execute.
command = "MP4Box -add testvideo.h264 convertedVideo.mp4"
# Execute our command
call([command], shell=True)
