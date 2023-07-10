import obd
import random
import time
from tkinter import *
from tkinter import font as tkFont
from picamera import PiCamera
import time
camera = PiCamera()
camera.resolution = (1280, 720)
camera.vflip = False
camera.contrast = 10

mainWindow = Tk()

#mainWindow.geometry("800x480")
mainWindow.attributes('-fullscreen',True)
mainWindow.title("TrackPack")
mainWindow.configure(bg = "#FFFFFF")

def exit(e):
    mainWindow.destroy()

def openBeginLoggingWindow():
    startTime = time.time()

    BeginLoggingWindow=Toplevel()
    #BeginLoggingWindow.geometry("800x480")
    BeginLoggingWindow.attributes('-fullscreen',True)
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
        515.0,
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
        515.0,
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
        400.0,
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
        500.0,
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
        400.0,
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
        text=str(speed),
        fill="#000000",
        font=("Inter", 36 * -1)
    )
    BeginLoggingWindowCanvas.create_text(
        709.0,
        370.0,
        anchor="center",
        text="1",
        fill="#000000",
        font=("Inter", 36 * -1)
    )
    BeginLoggingWindowCanvas.create_text(
        406.0,
        389.0,
        anchor="center",
        text="N",
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
        afterIdentifier = BeginLoggingWindow.after(1, update)
        endTime = time.time()
        elapsedTime = round(((endTime - startTime) - functionRunTime), 2)
        distancePerMilliSecond = (speed / 3600000) # Miles per ms
        distanceTravelled += distancePerMilliSecond
        if ((round(distanceTravelled, 4) == round((60 / 5280), 4)) and sixtyFootComplete == False):
            sixtyFootTime = elapsedTime
            sixtyFootComplete = True
            #print(sixtyFootComplete)
            BeginLoggingWindowCanvas.itemconfig(
                sixtyFootStats,
                text=str(sixtyFootTime) + "s"
            )
        if (speed >= 60 and zeroToSixtyComplete == False):
            zeroToSixtyTime = elapsedTime
            zeroToSixtyComplete = True
            #print(zeroToSixtyComplete)
            BeginLoggingWindowCanvas.itemconfig(
                zeroToSixtyStats,
                text=str(zeroToSixtyTime) + "s"
            )
        if ((round(distanceTravelled, 4) == 0.125) and eighthMileComplete == False):
            eighthMileTime = elapsedTime
            eighthMileComplete = True
            #print(eighthMileComplete)
            BeginLoggingWindowCanvas.itemconfig(
                eighthMileStats,
                text=str(eighthMileTime) + " @ " + str(speed) + "mph"
            )
        if ((round(distanceTravelled, 4) == round((1000 / 5280), 4)) and thousandFootComplete == False):
            thousandFootTime = elapsedTime
            thousandFootComplete = True
            #print(thousandFootComplete)
            BeginLoggingWindowCanvas.itemconfig(
                thousandFootStats,
                text=str(thousandFootTime) + "s"
            )
        if ((round(distanceTravelled, 4) == 0.250) and quarterMileComplete == False):
            quarterMileTime = elapsedTime
            camera.stop_recording()
            quarterMileComplete = True
            #print(quarterMileComplete)
            BeginLoggingWindowCanvas.itemconfig(
                quarterMileStats,
                text=str(quarterMileTime) + " @ " + str(speed) + "mph"
            )
            BeginLoggingWindow.after_cancel(afterIdentifier)
        BeginLoggingWindowCanvas.itemconfig(
            speedDisplay,
            text=str(speed)
        )
        BeginLoggingWindowCanvas.itemconfig(
            loggingTime,
            text=str(elapsedTime) + "s"
        )
        functionEndTime = time.time()
        functionRunTime += (functionEndTime - functionStartTime)
        #print(functionRunTime)
    update()

def openParameterLoggingWindow():
    ParameterLoggingWindow=Toplevel()
    #ParameterLoggingWindow.geometry("800x480")
    ParameterLoggingWindow.attributes('-fullscreen',True)
    ParameterLoggingWindow.title("TrackPack Parameter Logging")
    ParameterLoggingWindow.configure(bg = "#FFFFFF")
    global speed
    def beginLoggingCountdown():
        if (speed == 0):
            openVehicleMovingWindow()
        else:
            def countdown(count):
                ParameterLoggingWindowCanvas.itemconfig(countdownText, text=count)
                if count > 0:
                    ParameterLoggingWindow.after(1000, countdown, count - 1)
                else:
                    ParameterLoggingWindowCanvas.itemconfig(countdownText, text="Go!")
                    openBeginLoggingWindow()
                    camera.start_recording(/home/ikevins/Desktop/testvideo.h264)
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
    StoredDataWindow=Toplevel()
    #StoredDataWindow.geometry("800x480")
    StoredDataWindow.attributes('-fullscreen',True)
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

def checkDTC():
    if malfunctionIndicatorLight == True and CEL_count > 0:
        openDTCWindow()
    else:
        openNoDTCWindow()

def openDTCWindow():
    DTCWindow=Toplevel()
    #DTCWindow.geometry("800x480")
    DTCWindow.attributes('-fullscreen',True)
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
    #noDTCWindow.geometry("800x480")
    noDTCWindow.attributes('-fullscreen',True)
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
        254.0,
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
    #vehicleMovingWindow.geometry("800x480")
    vehicleMovingWindow.attributes('-fullscreen',True)
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
        50.0,
        168.0,
        anchor="nw",
        text="Vehicle must be at a complete stop before logging.",
        fill="#000000",
        font=("Inter", 32 * -1)
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

def openDataWindow():
    dataWindow=Toplevel()
    #dataWindow.geometry("800x480")
    dataWindow.attributes('-fullscreen',True)
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
        command=lambda: print("button_2 clicked"),
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
        95.0,
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
        font=("Inter", 24 * -1)
    )
    rpmDisplay = dataWindowCanvas.create_text(
        360.0,
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
        font=("Inter", 24 * -1)
    )
    speedDisplay = dataWindowCanvas.create_text(
        650.0,
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
        100.0,
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
        340.0,
        282.0,
        anchor="nw",
        text="Fuel Level",
        fill="#000000",
        font=("Inter", 24 * -1)
    )
    fuelLevelDisplay = dataWindowCanvas.create_text(
        370.0,
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
        font=("Inter", 24 * -1)
    )
    oilTemperatureDisplay = dataWindowCanvas.create_text(
        640.0,
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

obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="38400", fast=False, timeout = 30)

#Continuously query until the amount of supported commands is greater than 100
while len(connection.supported_commands) < 100:
    connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="38400", fast=False, timeout = 30)

coolantTemperature = 0
rpm = 0
speed = 0
speedTotal = 0
throttlePosition = 0
fuelLevel = 0
oilTemperature = 0
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

# Start the OBD connection and add the callbacks
connection.watch(obd.commands.COOLANT_TEMP, callback=coolantTemperatureTracker)
connection.watch(obd.commands.RPM, callback=rpmTracker)
connection.watch(obd.commands.SPEED, callback=speedTracker)
connection.watch(obd.commands.THROTTLE_POS, callback=throttlePositionTracker)
connection.watch(obd.commands.FUEL_LEVEL, callback=fuelLevelTracker)
connection.watch(obd.commands.OIL_TEMP, callback=oilTemperatureTracker)
connection.watch(obd.commands.STATUS, callback=statusTracker)
connection.watch(obd.commands.GET_DTC, callback=dtcTracker)
connection.start()

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
