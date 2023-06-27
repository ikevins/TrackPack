import obd
from tkinter import *
from tkinter import font as tkFont

mainWindow = Tk()

#mainWindow.geometry("800x480")
mainWindow.attributes('-fullscreen',True)
mainWindow.title("TrackPack")
mainWindow.configure(bg = "#FFFFFF")

def exit(e):
    mainWindow.destroy()

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
        x=5.0,
        y=17.0,
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
throttlePosition = 0
fuelLevel = 0
oilTemperature = 0
malfunctionIndicatorLight = False
CEL_count = 0
currentDTCs = []

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
    command=lambda: print("button_2 clicked"),
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
    command=lambda: print("button_3 clicked"),
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
