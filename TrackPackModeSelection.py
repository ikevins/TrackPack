import obd
import asyncio
from tkinter import *
from tkinter import font as tkFont
from random import randint

mainWindow = Tk()

mainWindow.geometry("800x480")
mainWindow.title("TrackPack")
mainWindow.configure(bg = "#FFFFFF")

obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="38400", fast=False, timeout = 30)

#Continuously query until the amount of supported commands is greater than 100
while len(connection.supported_commands) < 100:
    connection = obd.Async("/dev/rfcomm0", protocol="6", baudrate="38400", fast=False, timeout = 30)

def coolantTemperatureTracker(t):
    global coolantTemperature
    if not t.is_null():
        coolantTemperature = int(t.value.magnitude)

def rpmTracker(rpm_t):
    global rpm
    if not rpm_t.is_null():
        rpm = rpm_t.value.magnitude

def throttlePositionTracker(tp_t):
    global throttlePosition
    if not tp_t.is_null():
        throttlePosition = tp_t.value.magnitude
coolantTemperature = 0
rpm = 0
throttlePosition = 0

# Start the OBD connection and add the callbacks
async def startOBDConnection():
    await connection.watch(obd.commands.COOLANT_TEMP, callback=coolantTemperatureTracker)
    await connection.watch(obd.commands.RPM, callback=rpmTracker)
    await connection.watch(obd.commands.THROTTLE_POS, callback=throttlePositionTracker)
    await connection.start()

def update():
    dataWindowCanvas.itemconfig(
        ectDisplay,
        text="Engine Coolant \nTemperature °F\n\n" + str(coolantTemperature)
    )
    mainWindow.after(1000, update)

def openDataWindow():
    dataWindow=Toplevel()
    dataWindow.geometry("800x480")
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
        31.0,
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
        command=lambda: print("button_3 clicked"),
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
    ectDisplay = dataWindowCanvas.create_text(
        55.0,
        134.0,
        anchor="nw",
        text="Engine Coolant \nTemperature °F\n\n" + str(coolantTemperature),
        fill="#000000",
        font=("Inter", 21 * -1)
    )
    dataWindowCanvas.create_rectangle(
        280.0,
        123.0,
        520.0,
        238.0,
        fill="#A9A9A9",
        outline=""
        )
    dataWindowCanvas.create_text(
        310.0,
        136.0,
        anchor="nw",
        text="Engine Speed RPM\n\n" + str(rpm),
        fill="#000000",
        font=("Inter", 21 * -1)
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
        605.0,
        136.0,
        anchor="nw",
        text="Air/Fuel Ratio",
        fill="#000000",
        font=("Inter", 21 * -1)
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
        45.0,
        267.0,
        anchor="nw",
        text="Throttle Position %\n\n" + str(throttlePosition),
        fill="#000000",
        font=("Inter", 21 * -1)
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
        316.0,
        267.0,
        anchor="nw",
        text="Oil Pressure PSI",
        fill="#000000",
        font=("Inter", 21 * -1)
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
        580.0,
        267.0,
        anchor="nw",
        text="Oil Temperature °F",
        fill="#000000",
        font=("Inter", 21 * -1)
    )

    asyncio.create_task(startOBDConnection())
    update()

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
mainWindow.mainloop()
