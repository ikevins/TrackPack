from picamera import PiCamera
import time
import os
camera = PiCamera()
time.sleep(2)
camera.resolution = (1280, 720)
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 270
camera.hflip = False
camera.vflip = False
camera.start_recording("/home/ikevins/Desktop/testvideo.h264")
camera.wait_recording(5)
camera.stop_recording()

os.system("MP4Box -add testvideo.h264 convertedVideo.mp4")
