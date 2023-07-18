from picamera import PiCamera
import time
import os
camera = PiCamera()
time.sleep(2)
camera.resolution = (1280, 720)
camera.rotation = 270
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.start_recording("/home/ikevins/TrackPack/Videos/testvideo.h264")
camera.wait_recording(5)
camera.stop_recording()

os.system("MP4Box -add /home/ikevins/TrackPack/Videos/testvideo.h264 /home/ikevins/TrackPack/Videos/convertedVideo.mp4")
