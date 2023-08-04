#import obd
import random
import smbus
import math
import time
import os
import vlc
from tkinter import *
from tkinter import font as tkFont
from datetime import datetime
from picamera import PiCamera

mainWindow = Tk()

mainWindow.geometry("800x480")
#mainWindow.attributes('-fullscreen',True)
mainWindow.title("TrackPack")
mainWindow.configure(bg = "#FFFFFF")

camera = PiCamera()
camera.resolution = (1280, 720)
camera.vflip = False
camera.contrast = 10
camera.rotation = 270

# I2C address of the LSM6DSL accelerometer
ACCELEROMETER_I2C_ADDRESS = 0x6B

# I2C address of the LIS3MDL magnetometer
MAGNETOMETER_I2C_ADDRESS = 0x1E

# Register addresses of the accelerometer
ACCELEROMETER_CTRL_REG1 = 0x10
ACCELEROMETER_CTRL_REG8 = 0x17
ACCELEROMETER_OUTX_L = 0x28
ACCELEROMETER_OUTX_H = 0x29
ACCELEROMETER_OUTY_L = 0x2A
ACCELEROMETER_OUTY_H = 0x2B
ACCELEROMETER_OUTZ_L = 0x2C
ACCELEROMETER_OUTZ_H = 0x2D

# Register addresses of the magnetometer
MAGNETOMETER_CTRL_REG1 = 0x20
MAGNETOMETER_CTRL_REG2 = 0x21
MAGNETOMETER_CTRL_REG3 = 0x22
MAGNETOMETER_CTRL_REG4 = 0x23
MAGNETOMETER_OUTX_L = 0x28
MAGNETOMETER_OUTX_H = 0x29
MAGNETOMETER_OUTY_L = 0x2A
MAGNETOMETER_OUTY_H = 0x2B
MAGNETOMETER_OUTZ_L = 0x2C
MAGNETOMETER_OUTZ_H = 0x2D

# Initialize the I2C bus
bus = smbus.SMBus(1) #1 for Raspberry Pi 2 and newer

# Configure the accelerometer
bus.write_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_CTRL_REG1, 0x50) # Set the accelerometer to 208 Hz, ±2g range
bus.write_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_CTRL_REG8, 0xC0) # Enable high-pass filter to remove gravity offset

# Configure the magnetometer
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG2, 0x04) # Configure the Magnetometer
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG1, 0x80) # Sensor Enabled
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG1, 0x60) # Ultra High Performance Mode Selected for XY Axis
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG4, 0x0C) # Ultra High Performance Mode Selected for Z Axis
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG1, 0x1C) # Output Data Rate of 80 Hz Selected
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG3, 0x00) # Continous Conversion Mode, 4 wire interface Selected
bus.write_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_CTRL_REG2, 0x60) # 16 guass Full Scale

def exit(e):
    mainWindow.destroy()

def openBeginLoggingWindow():
    startTime = time.time()

    BeginLoggingWindow=Toplevel()
    BeginLoggingWindow.geometry("800x480")
    #BeginLoggingWindow.attributes('-fullscreen',True)
    BeginLoggingWindow.title("TrackPack Begin Parameter Logging")
    BeginLoggingWindow.configure(bg = "#FFFFFF")

    BeginLoggingWindowCanvas = Canvas(
        BeginLoggingWindow,
        bg = "#FFFFFF",
        height = 480,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    BeginLoggingWindowCanvas.place(x = 0, y = 0)
    BeginLoggingWindowCanvas.create_rectangle(
        22.0,
        329.0,
        159.0,
        450.0,
        fill="#A9A9A9",
        outline=""
    )
    BeginLoggingWindowCanvas.create_rectangle(
        339.0,
        329.0,
        476.0,
        450.0,
        fill="#A9A9A9",
        outline=""
    )
    BeginLoggingWindowCanvas.create_rectangle(
        641.0,
        329.0,
        778.0,
        450.0,
        fill="#A9A9A9",
        outline=""
    )
    BeginLoggingWindowCanvas.create_text(
        185.0,
        50.0,
        anchor="nw",
        text="TrackPack Parameter Logging",
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    BeginLoggingWindowCanvas.create_rectangle(
        220.0,
        95.0,
        580.0,
        145.0,
        fill="#A9A9A9",
        outline=""
    )
    loggingTime = BeginLoggingWindowCanvas.create_text(
        357.0,
        103.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 35 * -1)
    )
    BeginLoggingWindowCanvas.create_rectangle(
        220.0,
        150.0,
        580.0,
        180.0,
        fill="#A9A9A9",
        outline=""
    )
    BeginLoggingWindowCanvas.create_text(
        225.0,
        152.0,
        anchor="nw",
        text="60ft",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    sixtyFootStats = BeginLoggingWindowCanvas.create_text(
        510.0,
        152.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    BeginLoggingWindowCanvas.create_rectangle(
        220.0,
        185.0,
        580.0,
        215.0,
        fill="#A9A9A9",
        outline=""
    )
    BeginLoggingWindowCanvas.create_text(
        225.0,
        187.0,
        anchor="nw",
        text="0-60mph",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    zeroToSixtyStats = BeginLoggingWindowCanvas.create_text(
        510.0,
        187.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    BeginLoggingWindowCanvas.create_rectangle(
        220.0,
        220.0,
        580.0,
        250.0,
        fill="#A9A9A9",
        outline=""
    )
    BeginLoggingWindowCanvas.create_text(
        225.0,
        222.0,
        anchor="nw",
        text="1/8 mile",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    eighthMileStats = BeginLoggingWindowCanvas.create_text(
        375.0,
        220.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    BeginLoggingWindowCanvas.create_rectangle(
        220.0,
        255.0,
        580.0,
        285.0,
        fill="#A9A9A9",
        outline=""
    )
    BeginLoggingWindowCanvas.create_text(
        225.0,
        257.0,
        anchor="nw",
        text="1000ft",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    thousandFootStats = BeginLoggingWindowCanvas.create_text(
        495.0,
        257.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    BeginLoggingWindowCanvas.create_rectangle(
        220.0,
        290.0,
        580.0,
        320.0,
        fill="#A9A9A9",
        outline=""
    )
    BeginLoggingWindowCanvas.create_text(
        225.0,
        292.0,
        anchor="nw",
        text="1/4 mile",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    quarterMileStats = BeginLoggingWindowCanvas.create_text(
        375.0,
        292.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    BeginLoggingWindowCanvas.create_text(
        702.0,
        385.0,
        anchor="nw",
        text="g",
        fill="#000000",
        font=("Inter", 28 * -1)
    )
    speedDisplay = BeginLoggingWindowCanvas.create_text(
        90.0,
        370.0,
        anchor="center",
        fill="#000000",
        font=("Inter", 36 * -1)
    )
    accelerometerDisplay = BeginLoggingWindowCanvas.create_text(
        709.0,
        370.0,
        anchor="center",
        fill="#000000",
        font=("Inter", 36 * -1)
    )
    magnetometerDisplay = BeginLoggingWindowCanvas.create_text(
        406.0,
        389.0,
        anchor="center",
        fill="#000000",
        font=("Inter", 40 * -1)
    )
    BeginLoggingWindowCanvas.create_text(
        89.0,
        404.0,
        anchor="center",
        text="mph",
        fill="#000000",
        font=("Inter", 28 * -1)
    )
    '''
    def stopLogging():
        global maxSpeed
        global currentLog
        BeginLoggingWindow.after_cancel(afterIdentifier)
        currentLog.append(maxSpeed)
        saveLog(currentLog)
        goBackButton = Button(
            BeginLoggingWindow,
            text="Go Back",
            font=("Inter", 22 * -1),
            borderwidth=0,
            highlightthickness=0,
            command=BeginLoggingWindow.destroy,
            relief="flat"
        )
        goBackButton.place(
            x=10.0,
            y=20.0,
            width=160.0,
            height=35.0
        )
        stopButton.destroy()
    stopButton = Button(
        BeginLoggingWindow,
        text="Stop Logging",
        font=("Inter", 22 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=stopLogging,
        relief="flat"
    )
    stopButton.place(
        x=630.0,
        y=20.0,
        width=160.0,
        height=35.0
    )
    '''
    goBackButton = Button(
        BeginLoggingWindow,
        text="Go Back",
        font=("Inter", 22 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=BeginLoggingWindow.destroy,
        relief="flat"
    )
    goBackButton.place(
        x=10.0,
        y=20.0,
        width=160.0,
        height=35.0
    )

    def inertialMeasurementUnit():
        try:
            # Read acceleration data from the accelerometer
            accelerometer_x_l = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTX_L)
            accelerometer_x_h = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTX_H)
            accelerometer_y_l = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTY_L)
            accelerometer_y_h = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTY_H)
            accelerometer_z_l = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTZ_L)
            accelerometer_z_h = bus.read_byte_data(ACCELEROMETER_I2C_ADDRESS, ACCELEROMETER_OUTZ_H)
            # Read acceleration data from the accelerometer
            magnetometer_x_l = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTX_L)
            magnetometer_x_h = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTX_H)
            magnetometer_y_l = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTY_L)
            magnetometer_y_h = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTY_H)
            magnetometer_z_l = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTZ_L)
            magnetometer_z_h = bus.read_byte_data(MAGNETOMETER_I2C_ADDRESS, MAGNETOMETER_OUTZ_H)
            # Convert the raw data to signed 16-bit values
            accelerometer_x = (accelerometer_x_h << 8 | accelerometer_x_l)
            if accelerometer_x > 32767:
                accelerometer_x -= 65536
            accelerometer_y = (accelerometer_y_h << 8 | accelerometer_y_l)
            if accelerometer_y > 32767:
                accelerometer_y -= 65536
            accelerometer_z = (accelerometer_z_h << 8 | accelerometer_z_l)
            if accelerometer_z > 32767:
                accelerometer_z -= 65536
            magnetometer_x = (magnetometer_x_h << 8 | magnetometer_x_l)
            if magnetometer_x > 32767:
                magnetometer_x -= 65536
            magnetometer_y = (magnetometer_y_h << 8 | magnetometer_y_l)
            if magnetometer_y > 32767:
                magnetometer_y -= 65536
            magnetometer_z = (magnetometer_z_h << 8 | magnetometer_z_l)
            if magnetometer_z > 32767:
                magnetometer_z -= 65536
            # Calculate the g-force in each axis
            g_x = accelerometer_x / 16384.0
            g_y = accelerometer_y / 16384.0
            g_z = accelerometer_z / 16384.0
            # Calculate the total g-force
            g_total = math.sqrt(g_x ** 2 + g_y ** 2 + g_z ** 2) - 1.0  # Subtract the 1g offset
            # Display only positive g-force values
            g_total = max(0, g_total)
            # Calculate the direction
            direction = ""
            angle = math.degrees(math.atan2(magnetometer_x, magnetometer_y))
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

            return direction, float(format(g_total, '.1f'))
        except KeyboardInterrupt:
            pass

    def update():
        functionStartTime = time.time()
        global functionRunTime
        global speed
        global distanceTravelled
        global sixtyFootComplete
        global zeroToSixtyComplete
        global eighthMileComplete
        global thousandFootComplete
        global quarterMileComplete
        global afterIdentifier
        global maxSpeed
        global maxGForce
        sensorReadings = inertialMeasurementUnit()
        afterIdentifier = BeginLoggingWindow.after(1, update)
        endTime = time.time()
        elapsedTime = round((endTime - startTime), 2)
        distancePerMilliSecond = (speed / 500000) # account for misc delay
        distanceTravelled += distancePerMilliSecond
        #speed = random.randint(0, 100)
        if (speed > maxSpeed):
            maxSpeed = speed
        if (sensorReadings[1] > maxGForce):
            maxGForce = sensorReadings[1]

        if ((round(distanceTravelled, 3) == round((60 / 5280), 3)) and sixtyFootComplete == False):
            sixtyFootTime = format(elapsedTime, '.2f')
            sixtyFootComplete = True
            currentLog.append(sixtyFootTime)
            #print(sixtyFootComplete)
            BeginLoggingWindowCanvas.itemconfig(
                sixtyFootStats,
                text=sixtyFootTime + "s"
            )
        if (speed >= 60 and zeroToSixtyComplete == False):
            zeroToSixtyTime = format(elapsedTime, '.2f')
            zeroToSixtyComplete = True
            currentLog.append(zeroToSixtyTime)
            #print(zeroToSixtyComplete)
            BeginLoggingWindowCanvas.itemconfig(
                zeroToSixtyStats,
                text=zeroToSixtyTime + "s"
            )
        if ((round(distanceTravelled, 3) == 0.125) and eighthMileComplete == False):
            eighthMileSpeed = speed
            eighthMileTime = format(elapsedTime, '.2f')
            eighthMileComplete = True
            currentLog.append(eighthMileTime)
            currentLog.append(eighthMileSpeed)
            #print(eighthMileComplete)
            BeginLoggingWindowCanvas.itemconfig(
                eighthMileStats,
                text=eighthMileTime + "s @ " + str(speed) + "mph"
            )
        if ((round(distanceTravelled, 3) == round((1000 / 5280), 3)) and thousandFootComplete == False):
            thousandFootTime = format(elapsedTime, '.2f')
            thousandFootComplete = True
            currentLog.append(thousandFootTime)
            #print(thousandFootComplete)
            BeginLoggingWindowCanvas.itemconfig(
                thousandFootStats,
                text=thousandFootTime + "s"
            )
        if ((round(distanceTravelled, 3) == 0.250) and quarterMileComplete == False):
            BeginLoggingWindow.after_cancel(afterIdentifier)
            quarterMileSpeed = speed
            quarterMileTime = format(elapsedTime, '.2f')
            quarterMileComplete = True
            currentLog.append(quarterMileTime)
            currentLog.append(quarterMileSpeed)
            currentLog.append(maxSpeed)
            currentLog.append(maxGForce)
            camera.stop_recording()
            saveLog(currentLog)
            BeginLoggingWindowCanvas.itemconfig(
                quarterMileStats,
                text=quarterMileTime + "s @ " + str(speed) + "mph"
            )
            os.system("MP4Box -add " + "/home/kevin/TrackPack/Videos/" + str(currentLog[0]) + ".h264 " + "/home/kevin/TrackPack/Videos/" + str(currentLog[0]))
            os.system("rm /home/kevin/TrackPack/Videos/" + str(currentLog[0]) + ".h264 ")
            #stopButton.destroy()
            #print(quarterMileComplete)
        BeginLoggingWindowCanvas.itemconfig(
            speedDisplay,
            text=str(speed)
        )

        BeginLoggingWindowCanvas.itemconfig(
            magnetometerDisplay,
            text=str(sensorReadings[0])
        )
        BeginLoggingWindowCanvas.itemconfig(
            accelerometerDisplay,
            text=str(sensorReadings[1])
        )

        BeginLoggingWindowCanvas.itemconfig(
            loggingTime,
            text=str(elapsedTime) + "s"
        )
        functionEndTime = time.time()
        functionRunTime += (functionEndTime - functionStartTime)
        #print(functionRunTime)
    update()

def saveLog(currentLog):
    file = open("TrackPackLogs.txt", "a")
    for i in currentLog:
        file.write(str(i) + " ")
    file.write("\n")
    file.close

def openNoLogsWindow():
    noLogsWindow=Toplevel()
    noLogsWindow.geometry("800x480")
    #noLogsWindow.attributes('-fullscreen',True)
    noLogsWindow.title("TrackPack Review Stored Data")
    noLogsWindow.configure(bg = "#FFFFFF")

    noLogsWindowCanvas = Canvas(
        noLogsWindow,
        bg = "#FFFFFF",
        height = 480,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    noLogsWindowCanvas.place(x = 0, y = 0)
    noLogsWindowCanvas.create_text(
        205.0,
        168.0,
        anchor="nw",
        text="There are no stored logs.",
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    okButton = Button(
        noLogsWindow,
        text="OK",
        font=("Inter", 24 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=noLogsWindow.destroy,
        relief="flat"
    )
    okButton.place(
        x=320.0,
        y=222.0,
        width=160.0,
        height=57.0
    )

def openParameterLoggingWindow():
    ParameterLoggingWindow=Toplevel()
    ParameterLoggingWindow.geometry("800x480")
    #ParameterLoggingWindow.attributes('-fullscreen',True)
    ParameterLoggingWindow.title("TrackPack Parameter Logging")
    ParameterLoggingWindow.configure(bg = "#FFFFFF")
    global speed

    def resetParameters():
        global functionRunTime
        global distanceTravelled
        global sixtyFootComplete
        global zeroToSixtyComplete
        global eighthMileComplete
        global thousandFootComplete
        global quarterMileComplete
        global afterIdentifier
        global currentLog
        global maxSpeed
        functionRunTime = 0
        distanceTravelled = 0
        sixtyFootComplete = False
        zeroToSixtyComplete = False
        eighthMileComplete = False
        thousandFootComplete = False
        quarterMileComplete = False
        afterIdentifier = ""
        currentLog = []
        maxSpeed = 0
        maxGForce = float(0)

    def beginLoggingCountdown():
        global currentLog
        if (speed == 0):
            openVehicleMovingWindow()
        else:
            def countdown(count):
                ParameterLoggingWindowCanvas.itemconfig(countdownText, text=count)
                if count > 0:
                    ParameterLoggingWindow.after(1000, countdown, count - 1)
                else:
                    if (speed == 0):
                        openVehicleMovingWindow()
                    else:
                        ParameterLoggingWindowCanvas.itemconfig(countdownText, text="Go!")
                        resetParameters()
                        currentLog.append(round(time.time()))
                        currentLog.append(datetime.now().month)
                        currentLog.append(datetime.now().day)
                        currentLog.append(datetime.now().year)
                        openBeginLoggingWindow()
                        camera.start_recording("/home/kevin/TrackPack/Videos/" + str(currentLog[0]) + ".h264")
                        #ParameterLoggingWindow.destroy()
            beginLoggingButton.destroy()
            countdownText = ParameterLoggingWindowCanvas.create_text(
                390.0,
                240.0,
                anchor="center",
                fill="#000000",
                font=("Inter", 32 * -1)
            )
            countdown(3)
    ParameterLoggingWindowCanvas = Canvas(
        ParameterLoggingWindow,
        bg = "#FFFFFF",
        height = 480,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    ParameterLoggingWindowCanvas.place(x = 0, y = 0)
    ParameterLoggingWindowCanvas.create_text(
        145.0,
        96.0,
        anchor="nw",
        text="TrackPack Parameter Logging",
        fill="#000000",
        font=("Inter", 36 * -1)
    )
    beginLoggingButton = Button(
        ParameterLoggingWindow,
        text="Begin Logging",
        font=("Inter", 32 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=beginLoggingCountdown,
        relief="flat"
    )
    beginLoggingButton.place(
        x=200.0,
        y=190.0,
        width=380.0,
        height=100.0
    )
    goBackButton = Button(
        ParameterLoggingWindow,
        text="Go Back",
        font=("Inter", 22 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=ParameterLoggingWindow.destroy,
        relief="flat"
    )
    goBackButton.place(
        x=10.0,
        y=20.0,
        width=160.0,
        height=35.0
    )

def openStoredDataWindow():
    try:
        with open("TrackPackLogs.txt", "r") as file:
            logs = []
            for i in file:
                currentLine = i.split()
                logs.append(currentLine)
    except FileNotFoundError:
        openNoLogsWindow()
    else:
        StoredDataWindow=Toplevel()
        StoredDataWindow.geometry("800x480")
        #StoredDataWindow.attributes('-fullscreen',True)
        StoredDataWindow.title("TrackPack Review Stored Data")
        StoredDataWindow.configure(bg = "#FFFFFF")
        StoredDataWindowCanvas = Canvas(
            StoredDataWindow,
            bg = "#FFFFFF",
            height = 480,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        StoredDataWindowCanvas.place(x = 0, y = 0)
        goBackButton = Button(
            StoredDataWindow,
            text="Go Back",
            font=("Inter", 22 * -1),
            borderwidth=0,
            highlightthickness=0,
            command=StoredDataWindow.destroy,
            relief="flat"
        )
        goBackButton.place(
            x=10.0,
            y=20.0,
            width=160.0,
            height=35.0
        )
        yPosition = 91
        buttonList = []
        for i in range(len(logs)):
            def action(x = i):
                openStoredLogWindow(logs[x])
            buttonList.append(Button(
                StoredDataWindow,
                text=logs[i][1] + "/" + logs[i][2] + "/" + logs[i][3],
                font=("Inter", 22 * -1),
                borderwidth=0,
                highlightthickness=0,
                command=action,
                relief="flat"
            ))
            buttonList[i].place(
                x=5.0,
                y=yPosition,
                width=790.0,
                height=41.0
            )
            yPosition += 50

def openStoredLogWindow(logs):
    StoredLogWindow=Toplevel()
    StoredLogWindow.geometry("800x480")
    #StoredLogWindow.attributes('-fullscreen',True)
    StoredLogWindow.title("TrackPack Review Stored Data")
    StoredLogWindow.configure(bg = "#FFFFFF")

    '''
    missingParameters = 12 - len(logs)
    if (missingParameters > 0):
        for i in range(missingParameters):
            logs.append(None)
    '''

    StoredLogWindowCanvas = Canvas(
        StoredLogWindow,
        bg = "#FFFFFF",
        height = 480,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    StoredLogWindowCanvas.place(x = 0, y = 0)
    viewVideoButton = Button(
        StoredLogWindow,
        text="View Video",
        font=("Inter", 22 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=lambda: vlc.MediaPlayer("/home/kevin/TrackPack/Videos/" + logs[0]).play(),
        relief="flat",
        bg="#A9A9A9",
        fg="#000000"
    )
    viewVideoButton.place(
        x=270.0,
        y=350.0,
        width=260.0,
        height=75.0
    )
    StoredLogWindowCanvas.create_rectangle(
        22.0,
        329.0,
        159.0,
        450.0,
        fill="#A9A9A9",
        outline=""
    )
    StoredLogWindowCanvas.create_rectangle(
        641.0,
        329.0,
        778.0,
        450.0,
        fill="#A9A9A9",
        outline=""
    )
    StoredLogWindowCanvas.create_text(
        215.0,
        50.0,
        anchor="nw",
        text="TrackPack Log: " + logs[1] + "/" + logs[2] + "/" + logs[3],
        fill="#000000",
        font=("Inter", 32 * -1),
    )
    StoredLogWindowCanvas.create_rectangle(
        220.0,
        95.0,
        580.0,
        145.0,
        fill="#A9A9A9",
        outline=""
    )
    StoredLogWindowCanvas.create_text(
        357.0,
        103.0,
        anchor="nw",
        text=logs[9],
        fill="#000000",
        font=("Inter", 35 * -1)
    )
    StoredLogWindowCanvas.create_rectangle(
        220.0,
        150.0,
        580.0,
        180.0,
        fill="#A9A9A9",
        outline=""
    )
    StoredLogWindowCanvas.create_text(
        225.0,
        152.0,
        anchor="nw",
        text="60ft",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    StoredLogWindowCanvas.create_text(
        510.0,
        152.0,
        anchor="nw",
        text=logs[4] + "s",
        fill="#000000",
        font=("Inter", 24 * -1),
    )
    StoredLogWindowCanvas.create_rectangle(
        220.0,
        185.0,
        580.0,
        215.0,
        fill="#A9A9A9",
        outline=""
    )
    StoredLogWindowCanvas.create_text(
        225.0,
        187.0,
        anchor="nw",
        text="0-60mph",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    StoredLogWindowCanvas.create_text(
        510.0,
        187.0,
        anchor="nw",
        text=logs[5] + "s",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    StoredLogWindowCanvas.create_rectangle(
        220.0,
        220.0,
        580.0,
        250.0,
        fill="#A9A9A9",
        outline=""
    )
    StoredLogWindowCanvas.create_text(
        225.0,
        222.0,
        anchor="nw",
        text="1/8 mile",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    StoredLogWindowCanvas.create_text(
        375.0,
        220.0,
        anchor="nw",
        text=logs[6] + "s @ " + logs[7] + "mph",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    StoredLogWindowCanvas.create_rectangle(
        220.0,
        255.0,
        580.0,
        285.0,
        fill="#A9A9A9",
        outline=""
    )
    StoredLogWindowCanvas.create_text(
        225.0,
        257.0,
        anchor="nw",
        text="1000ft",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    StoredLogWindowCanvas.create_text(
        495.0,
        257.0,
        anchor="nw",
        text=logs[8] + "s",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    StoredLogWindowCanvas.create_rectangle(
        220.0,
        290.0,
        580.0,
        320.0,
        fill="#A9A9A9",
        outline=""
    )
    StoredLogWindowCanvas.create_text(
        225.0,
        292.0,
        anchor="nw",
        text="1/4 mile",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    StoredLogWindowCanvas.create_text(
        375.0,
        292.0,
        anchor="nw",
        text=logs[9] + "s @ " + logs[10] + "mph",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    StoredLogWindowCanvas.create_text(
        702.0,
        385.0,
        anchor="nw",
        text="g",
        fill="#000000",
        font=("Inter", 28 * -1)
    )
    StoredLogWindowCanvas.create_text(
        90.0,
        370.0,
        anchor="center",
        text=logs[11],
        fill="#000000",
        font=("Inter", 36 * -1)
    )
    StoredLogWindowCanvas.create_text(
        709.0,
        370.0,
        anchor="center",
        text=logs[12],
        fill="#000000",
        font=("Inter", 36 * -1)
    )
    StoredLogWindowCanvas.create_text(
        89.0,
        415.0,
        anchor="center",
        text="mph\n (Top Speed)",
        fill="#000000",
        font=("Inter", 20 * -1),
        justify="center"
    )
    goBackButton = Button(
        StoredLogWindow,
        text="Go Back",
        font=("Inter", 22 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=StoredLogWindow.destroy,
        relief="flat"
    )
    goBackButton.place(
        x=10.0,
        y=20.0,
        width=160.0,
        height=35.0
    )

def checkDTC():
    if malfunctionIndicatorLight == True and CEL_count > 0:
        openDTCWindow()
    else:
        openNoDTCWindow()

def openDTCWindow():
    DTCWindow=Toplevel()
    DTCWindow.geometry("800x480")
    #DTCWindow.attributes('-fullscreen',True)
    DTCWindow.title("TrackPack Diagnostic Information")
    DTCWindow.configure(bg = "#FFFFFF")

    DTCWindowCanvas = Canvas(
        DTCWindow,
        bg = "#FFFFFF",
        height = 480,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    DTCWindowCanvas.place(x = 0, y = 0)
    DTCWindowCanvas.create_text(
        204.0,
        34.0,
        anchor="nw",
        text="TrackPack Diagnostic Info",
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    goBackButton = Button(
        DTCWindow,
        text="Go Back",
        font=("Inter", 22 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=DTCWindow.destroy,
        relief="flat"
    )
    goBackButton.place(
        x=10.0,
        y=20.0,
        width=160.0,
        height=35.0
    )

    rectangleTopLeftYPosition = 91
    rectangleBottomRightYPosition = 132
    textYPosition = 94

    for i in range(len(currentDTCs)):
            DTCWindowCanvas.create_rectangle(
                5.0, #Top-left X-axis
                rectangleTopLeftYPosition, #Top-left Y-axis
                795.0, #Bottom-right X-axis
                rectangleBottomRightYPosition, #Bottom-right Y-axis
                fill="#D3D3D3",
                outline=""
                )
            DTCWindowCanvas.create_text(
                20.0,
                textYPosition,
                anchor="nw",
                text=currentDTCs[i],
                fill="#000000",
                font=("Inter", 32 * -1)
            )
            rectangleTopLeftYPosition += 45
            rectangleBottomRightYPosition += 45
            textYPosition += 45

def openNoDTCWindow():
    noDTCWindow=Toplevel()
    noDTCWindow.geometry("800x480")
    #noDTCWindow.attributes('-fullscreen',True)
    noDTCWindow.title("TrackPack Diagnostic Information")
    noDTCWindow.configure(bg = "#FFFFFF")

    noDTCWindowCanvas = Canvas(
        noDTCWindow,
        bg = "#FFFFFF",
        height = 480,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    noDTCWindowCanvas.place(x = 0, y = 0)
    noDTCWindowCanvas.create_text(
        265.0,
        168.0,
        anchor="nw",
        text="No DTCs Detected.",
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    okButton = Button(
        noDTCWindow,
        text="OK",
        font=("Inter", 24 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=noDTCWindow.destroy,
        relief="flat"
    )
    okButton.place(
        x=320.0,
        y=222.0,
        width=160.0,
        height=57.0
    )

def openVehicleMovingWindow():
    vehicleMovingWindow=Toplevel()
    vehicleMovingWindow.geometry("800x480")
    #vehicleMovingWindow.attributes('-fullscreen',True)
    vehicleMovingWindow.title("TrackPack Parameter Logging")
    vehicleMovingWindow.configure(bg = "#FFFFFF")

    vehicleMovingWindowCanvas = Canvas(
        vehicleMovingWindow,
        bg = "#FFFFFF",
        height = 480,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    vehicleMovingWindowCanvas.place(x = 0, y = 0)
    vehicleMovingWindowCanvas.create_text(
        40.0,
        168.0,
        anchor="nw",
        text="Vehicle must be at a complete stop before logging.",
        fill="#000000",
        font=("Inter", 28 * -1)
    )
    okButton = Button(
        vehicleMovingWindow,
        text="OK",
        font=("Inter", 24 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=vehicleMovingWindow.destroy,
        relief="flat"
    )
    okButton.place(
        x=320.0,
        y=222.0,
        width=160.0,
        height=57.0
    )

def openMoreDataWindow():
    dataWindow=Toplevel()
    dataWindow.geometry("800x480")
    #dataWindow.attributes('-fullscreen',True)
    dataWindow.title("TrackPack OBD-II Data")
    dataWindow.configure(bg = "#FFFFFF")

    def on_canvas_scroll(event):
        dataWindowCanvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def on_canvas_touch_scroll(event):
        dataWindowCanvas.yview_scroll(-1 * event.delta, "units")

    dataWindowCanvas = Canvas(
        dataWindow,
        bg = "#FFFFFF",
        height = 480,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    scrollbar = Scrollbar(dataWindow, orient=VERTICAL, command=dataWindowCanvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    dataWindowCanvas.configure(yscrollcommand=scrollbar.set)
    frame = Frame(dataWindowCanvas, bg="#FFFFFF")
    dataWindowCanvas.create_window((0, 0), window=frame, anchor="nw")
    dataWindowCanvas.bind("<MouseWheel>", on_canvas_scroll)
    dataWindowCanvas.bind("<MouseWheel>", on_canvas_touch_scroll)
    dataWindowCanvas.bind("<Configure>", lambda event: dataWindowCanvas.configure(scrollregion=dataWindowCanvas.bbox("all")))

    dataWindowCanvas.place(x = 0, y = 0)
    dataWindowCanvas.create_text(
        227.0,
        60.0,
        anchor="nw",
        text="TrackPack OBD-II Data",
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    goBackButton = Button(
        dataWindow,
        text="Go Back",
        font=("Inter", 22 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=dataWindow.destroy,
        relief="flat"
    )
    goBackButton.place(
        x=10.0,
        y=20.0,
        width=160.0,
        height=35.0
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        119.0,
        800.0,
        149.0,
        fill="#EDECEB",
        outline="#000000"
    )
    speedDisplay = dataWindowCanvas.create_text(
        605.0,
        119.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        119.0,
        600.0,
        149.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        119.0,
        anchor="nw",
        text="Speed",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        149.0,
        800.0,
        179.0,
        fill="#EDECEB",
        outline="#000000"
    )
    rpmDisplay = dataWindowCanvas.create_text(
        605.0,
        149.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        149.0,
        600.0,
        179.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        149.0,
        anchor="nw",
        text="RPM",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        179.0,
        800.0,
        209.0,
        fill="#EDECEB",
        outline="#000000"
    )
    engineLoadDisplay = dataWindowCanvas.create_text(
        605.0,
        179.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        179.0,
        600.0,
        209.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        179.0,
        anchor="nw",
        text="Load Percentage (%)",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        209.0,
        800.0,
        239.0,
        fill="#EDECEB",
        outline="#000000"
    )
    coolantTemperatureDisplay = dataWindowCanvas.create_text(
        605.0,
        209.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        209.0,
        600.0,
        239.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        209.0,
        anchor="nw",
        text="Engine Coolant Temperature (°F)",
        fill="#000000",
        font=("Inter", 22 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        239.0,
        800.0,
        269.0,
        fill="#EDECEB",
        outline="#000000"
    )
    shortFuelTrim1Display = dataWindowCanvas.create_text(
        605.0,
        239.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        239.0,
        600.0,
        269.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        239.0,
        anchor="nw",
        text="Short Term Fuel Trim Bank 1 (%)",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        269.0,
        800.0,
        299.0,
        fill="#EDECEB",
        outline="#000000"
    )
    longFuelTrim1Display = dataWindowCanvas.create_text(
        605.0,
        269.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        269.0,
        600.0,
        299.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        269.0,
        anchor="nw",
        text="Long Term Fuel Trim Bank 1 (%)",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        299.0,
        800.0,
        329.0,
        fill="#EDECEB",
        outline="#000000"
    )
    shortFuelTrim2Display = dataWindowCanvas.create_text(
        605.0,
        299.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        299.0,
        600.0,
        329.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        299.0,
        anchor="nw",
        text="Short Term Fuel Trim Bank 2 (%)",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        329.0,
        800.0,
        359.0,
        fill="#EDECEB",
        outline="#000000"
    )
    longFuelTrim2Display = dataWindowCanvas.create_text(
        605.0,
        329.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        329.0,
        600.0,
        359.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        329.0,
        anchor="nw",
        text="Long Term Fuel Trim Bank 2 (%)",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        359.0,
        800.0,
        389.0,
        fill="#EDECEB",
        outline="#000000"
    )
    mafDisplay = dataWindowCanvas.create_text(
        605.0,
        359.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        359.0,
        600.0,
        389.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        359.0,
        anchor="nw",
        text="Air Flow Rate",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        389.0,
        800.0,
        419.0,
        fill="#EDECEB",
        outline="#000000"
    )
    oilTemperatureDisplay = dataWindowCanvas.create_text(
        605.0,
        389.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        389.0,
        600.0,
        419.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        389.0,
        anchor="nw",
        text="Oil Temperature",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        419.0,
        600.0,
        449.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        419.0,
        800.0,
        449.0,
        fill="#EDECEB",
        outline="#000000"
    )
    fuelTypeDisplay = dataWindowCanvas.create_text(
        605.0,
        419.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_text(
        5.0,
        419.0,
        anchor="nw",
        text="Fuel Type",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        449.0,
        800.0,
        479.0,
        fill="#EDECEB",
        outline="#000000"
    )
    evapPressureDisplay = dataWindowCanvas.create_text(
        605.0,
        449.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        449.0,
        600.0,
        480.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        449.0,
        anchor="nw",
        text="Evaporative System Vapor Pressure",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        479.0,
        800.0,
        510.0,
        fill="#EDECEB",
        outline="#000000"
    )
    throttlePositionDisplay = dataWindowCanvas.create_text(
        605.0,
        479.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        479.0,
        600.0,
        510.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        479.0,
        anchor="nw",
        text="Throttle Position",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        600.0,
        509.0,
        800.0,
        540.0,
        fill="#EDECEB",
        outline="#000000"
    )
    fuelLevelDisplay = dataWindowCanvas.create_text(
        605.0,
        509.0,
        anchor="nw",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    dataWindowCanvas.create_rectangle(
        0.0,
        509.0,
        600.0,
        540.0,
        fill="#EDECEB",
        outline="#000000"
    )
    dataWindowCanvas.create_text(
        5.0,
        509.0,
        anchor="nw",
        text="Fuel Level",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    def update():
        dataWindowCanvas.itemconfig(
            speedDisplay,
            text=str(speed)
        )
        dataWindowCanvas.itemconfig(
            rpmDisplay,
            text=str(rpm)
        )
        dataWindowCanvas.itemconfig(
            engineLoadDisplay,
            text=str(engineLoad)
        )
        dataWindowCanvas.itemconfig(
            coolantTemperatureDisplay,
            text=str(coolantTemperature)
        )
        dataWindowCanvas.itemconfig(
            shortFuelTrim1Display,
            text=str(shortFuelTrim1)
        )
        dataWindowCanvas.itemconfig(
            longFuelTrim1Display,
            text=str(longFuelTrim1)
        )
        dataWindowCanvas.itemconfig(
            shortFuelTrim2Display,
            text=str(shortFuelTrim2)
        )
        dataWindowCanvas.itemconfig(
            longFuelTrim2Display,
            text=str(longFuelTrim2)
        )
        dataWindowCanvas.itemconfig(
            oilTemperatureDisplay,
            text=str(oilTemperature)
        )
        dataWindowCanvas.itemconfig(
            mafDisplay,
            text=str(maf)
        )
        dataWindowCanvas.itemconfig(
            fuelTypeDisplay,
            text=str(fuelType)
        )
        dataWindowCanvas.itemconfig(
            evapPressureDisplay,
            text=str(evapPressure)
        )
        dataWindowCanvas.itemconfig(
            throttlePositionDisplay,
            text=str(throttlePosition) + "%"
        )
        dataWindowCanvas.itemconfig(
            fuelLevelDisplay,
            text=str(fuelLevel) + "%"
        )
        dataWindow.after(1, update)
    update()
    dataWindowCanvas.pack(side=LEFT, fill=BOTH, expand=True)

def openDataWindow():
    dataWindow=Toplevel()
    dataWindow.geometry("800x480")
    #dataWindow.attributes('-fullscreen',True)
    dataWindow.title("TrackPack OBD-II Data")
    dataWindow.configure(bg = "#FFFFFF")

    dataWindowCanvas = Canvas(
        dataWindow,
        bg = "#FFFFFF",
        height = 480,
        width = 800,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    dataWindowCanvas.place(x = 0, y = 0)
    dataWindowCanvas.create_text(
        227.0,
        60.0,
        anchor="nw",
        text="TrackPack OBD-II Data",
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    goBackButton = Button(
        dataWindow,
        text="Go Back",
        font=("Inter", 22 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=dataWindow.destroy,
        relief="flat"
    )
    goBackButton.place(
        x=10.0,
        y=20.0,
        width=160.0,
        height=35.0
    )
    moreDataButton = Button(
        dataWindow,
        text="View More \nData Parameters",
        font=("Inter", 21 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=openMoreDataWindow,
        relief="flat"
    )
    moreDataButton.place(
        x=143.0,
        y=389.0,
        width=200.0,
        height=80.0
    )
    diagInfoButton = Button(
        dataWindow,
        text="View Diagnostic \nInformation",
        font=("Inter", 21 * -1),
        borderwidth=0,
        highlightthickness=0,
        command=checkDTC,
        relief="flat"
    )
    diagInfoButton.place(
        x=442.0,
        y=389.0,
        width=200.0,
        height=80.0
    )
    dataWindowCanvas.create_rectangle(
        10.0,
        125.0,
        250.0,
        240.0,
        fill="#A9A9A9",
        outline=""
    )
    dataWindowCanvas.create_text(
        40.0,
        135.0,
        anchor="nw",
        text="Engine Coolant\nTemperature (°F)",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    coolantTemperatureDisplay = dataWindowCanvas.create_text(
        115.0,
        195.0,
        anchor="nw",
        text=str(coolantTemperature),
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    dataWindowCanvas.create_rectangle(
        280.0,
        125.0,
        520.0,
        238.0,
        fill="#A9A9A9",
        outline=""
        )
    dataWindowCanvas.create_text(
        285.0,
        150.0,
        anchor="nw",
        text="Engine Speed (RPM)",
        fill="#000000",
        font=("Inter", 22 * -1)
    )
    rpmDisplay = dataWindowCanvas.create_text(
        390.0,
        195.0,
        anchor="nw",
        text=str(rpm),
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    dataWindowCanvas.create_rectangle(
        548.0,
        125.0,
        788.0,
        240.0,
        fill="#A9A9A9",
        outline=""
        )
    dataWindowCanvas.create_text(
        555.0,
        150.0,
        anchor="nw",
        text="Vehicle Speed (MPH)",
        fill="#000000",
        font=("Inter", 22 * -1)
    )
    speedDisplay = dataWindowCanvas.create_text(
        660.0,
        195.0,
        anchor="nw",
        text=str(speed),
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    dataWindowCanvas.create_rectangle(
        10.0,
        257.0,
        250.0,
        372.0,
        fill="#A9A9A9",
        outline=""
    )
    dataWindowCanvas.create_text(
        35.0,
        282.0,
        anchor="nw",
        text="Throttle Position",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    throttlePositionDisplay = dataWindowCanvas.create_text(
        115.0,
        327.0,
        anchor="nw",
        text=str(throttlePosition) + "%",
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    dataWindowCanvas.create_rectangle(
        279.0,
        257.0,
        519.0,
        372.0,
        fill="#A9A9A9",
        outline=""
        )
    dataWindowCanvas.create_text(
        345.0,
        275.0,
        anchor="nw",
        text="Fuel Level",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    fuelLevelDisplay = dataWindowCanvas.create_text(
        390.0,
        327.0,
        anchor="nw",
        text=str(fuelLevel) + "%",
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    dataWindowCanvas.create_rectangle(
        548.0,
        257.0,
        788.0,
        372.0,
        fill="#A9A9A9",
        outline=""
        )
    dataWindowCanvas.create_text(
        560.0,
        282.0,
        anchor="nw",
        text="Oil Temperature (°F)",
        fill="#000000",
        font=("Inter", 22 * -1)
    )
    oilTemperatureDisplay = dataWindowCanvas.create_text(
        660.0,
        327.0,
        anchor="nw",
        text=str(oilTemperature),
        fill="#000000",
        font=("Inter", 32 * -1)
    )
    def update():
        dataWindowCanvas.itemconfig(
            coolantTemperatureDisplay,
            text=str(coolantTemperature)
        )
        dataWindowCanvas.itemconfig(
            rpmDisplay,
            text=str(rpm)
        )
        dataWindowCanvas.itemconfig(
            speedDisplay,
            text=str(speed)
        )
        dataWindowCanvas.itemconfig(
            throttlePositionDisplay,
            text=str(throttlePosition) + "%"
        )
        dataWindowCanvas.itemconfig(
            fuelLevelDisplay,
            text=str(fuelLevel) + "%"
        )
        dataWindowCanvas.itemconfig(
            oilTemperatureDisplay,
            text=str(oilTemperature)
        )
        dataWindow.after(1, update)
    update()


#obd.logger.setLevel(obd.logging.DEBUG)

#connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="38400", fast=False, timeout = 30)

#Continuously query until the amount of supported commands is greater than 100
#while len(connection.supported_commands) < 100:
    #connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="38400", fast=False, timeout = 30)


coolantTemperature = 0
rpm = 0
speed = 60
throttlePosition = 0
fuelLevel = 0
oilTemperature = 0
engineLoad = 0
shortFuelTrim1 = 0
longFuelTrim1 = 0
shortFuelTrim2 = 0
longFuelTrim2 = 0
fuelPressure = 0
intakePressure = 0
maf = 0
fuelType = 0
evapPressure = 0
malfunctionIndicatorLight = False
CEL_count = 0
currentDTCs = []
distanceTravelled = 0
functionRunTime = 0
testbool = False
sixtyFootComplete = False
zeroToSixtyComplete = False
eighthMileComplete = False
thousandFootComplete = False
quarterMileComplete = False
afterIdentifier = ""
currentLog = []
maxSpeed = 0
maxGForce = float(0)

def coolantTemperatureTracker(response):
    global coolantTemperature
    if not response.is_null():
        coolantTemperature = int((response.value.magnitude * (9/5)) + 32)

def rpmTracker(response):
    global rpm
    if not response.is_null():
        rpm = int(response.value.magnitude)

def speedTracker(response):
    global speed
    if not response.is_null():
        speed = int(response.value.magnitude / 1.609344)

def throttlePositionTracker(response):
    global throttlePosition
    if not response.is_null():
        throttlePosition = int(response.value.magnitude)

def fuelLevelTracker(response):
    global fuelLevel
    if not response.is_null():
        fuelLevel = int(response.value.magnitude)

def oilTemperatureTracker(response):
    global oilTemperature
    if not response.is_null():
        oilTemperature = int((response.value.magnitude * (9/5)) + 32)

def statusTracker(response):
    global malfunctionIndicatorLight
    global CEL_count
    if not response.is_null():
        malfunctionIndicatorLight = response.value.MIL
        CEL_count = response.value.DTC_count

def dtcTracker(response):
    global currentDTCs
    if not response.is_null():
        currentDTCs = response.value

def engineLoadTracker(response):
    global engineLoad
    if not response.is_null():
        engineLoad = int(response.value.magnitude)

def shortFuelTrim1Tracker (response):
    global shortFuelTrim1
    if not response.is_null():
        shortFuelTrim1 = int(response.value.magnitude)

def longFuelTrim1Tracker (response):
    global longFuelTrim1
    if not response.is_null():
        longFuelTrim1 = int(response.value.magnitude)

def shortFuelTrim2Tracker (response):
    global shortFuelTrim2
    if not response.is_null():
        shortFuelTrim2 = int(response.value.magnitude)

def longFuelTrim2Tracker (response):
    global longFuelTrim2
    if not response.is_null():
        longFuelTrim2 = int(response.value.magnitude)

def fuelPressureTracker (response):
    global fuelPressure
    if not response.is_null():
        fuelPressure = int(response.value.magnitude)

def intakePressureTracker (response):
    global intakePressure
    if not response.is_null():
        intakePressure = int(response.value.magnitude)

def mafTracker (response):
    global maf
    if not response.is_null():
        maf = int(response.value.magnitude)

def fuelTypeList (response):
    global fuelType
    if not response.is_null():
        fuelType = int(response.value.magnitude)

def evapTracker (response):
    global evapPressure
    if not response.is_null():
        evapPressure = int(response.value.magnitude)


# Start the OBD connection and add the callbacks
'''
connection.watch(obd.commands.COOLANT_TEMP, callback=coolantTemperatureTracker)
connection.watch(obd.commands.RPM, callback=rpmTracker)
connection.watch(obd.commands.SPEED, callback=speedTracker)
connection.watch(obd.commands.THROTTLE_POS, callback=throttlePositionTracker)
connection.watch(obd.commands.FUEL_LEVEL, callback=fuelLevelTracker)
connection.watch(obd.commands.OIL_TEMP, callback=oilTemperatureTracker)
connection.watch(obd.commands.STATUS, callback=statusTracker)
connection.watch(obd.commands.GET_DTC, callback=dtcTracker)
connection.watch(obd.commands.ENGINE_LOAD, callback=engineLoadTracker)
connection.watch(obd.commands.SHORT_FUEL_TRIM_1, callback=shortFuelTrim1Tracker)
connection.watch(obd.commands.LONG_FUEL_TRIM_1	, callback=longFuelTrim1Tracker)
connection.watch(obd.commands.SHORT_FUEL_TRIM_2, callback=shortFuelTrim2Tracker)
connection.watch(obd.commands.LONG_FUEL_TRIM_2	, callback=longFuelTrim2Tracker)
connection.watch(obd.commands.FUEL_PRESSURE, callback=fuelPressureTracker)
connection.watch(obd.commands.INTAKE_PRESSURE, callback=intakePressureTracker)
connection.watch(obd.commands.MAF, callback=mafTracker)
connection.watch(obd.commands.FUEL_TYPE, callback=fuelTypeList)
connection.watch(obd.commands.EVAP_VAPOR_PRESSURE, callback=evapTracker)
connection.start()
'''

mainWindowCanvas = Canvas(
    mainWindow,
    bg = "#FFFFFF",
    height = 480,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
mainWindowCanvas.place(x = 0, y = 0)

button_1 = Button(
    mainWindow,
    font=("Inter", 36 * -1),
    text="OBD-II\nData",
    borderwidth=0,
    highlightthickness=0,
    command=openDataWindow,
    relief="flat"
)
button_1.place(
    x=20.0,
    y=190.0,
    width=220.0,
    height=100.0
)
button_2 = Button(
    mainWindow,
    font=("Inter", 36 * -1),
    text="Parameter\nLogging",
    borderwidth=0,
    highlightthickness=0,
    command=openParameterLoggingWindow,
    relief="flat"
)
button_2.place(
    x=290.0,
    y=190.0,
    width=220.0,
    height=100.0
)
button_3 = Button(
    mainWindow,
    font=("Inter", 36 * -1),
    text="Review\nStored Data",
    borderwidth=0,
    highlightthickness=0,
    command=openStoredDataWindow,
    relief="flat"
)
button_3.place(
    x=560.0,
    y=190.0,
    width=220.0,
    height=100.0
)
mainWindowCanvas.create_text(
    98.0,
    50.0,
    anchor="nw",
    text="TrackPack Mode Selection",
    fill="#000000",
    font=("Inter", 48 * -1)
)
mainWindow.bind('<Escape>', exit)
mainWindow.mainloop()
