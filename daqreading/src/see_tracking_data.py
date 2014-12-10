# System imports
import time
from system import *

# Create window
window = Window("Observer tracking data")

# Get GLIB access
glib = GLIB('192.168.0.115', 'register_mapping.dat')
glib.setWindow(window)

# Design
window.printLine(4, "Press [s] to get a new data packet or [ctrl+c] to quit", "Info", "center")
window.waitForKey("s")

# Design
window.printBox(0, 6, 40, "BC: ", "Default", "right")
window.printBox(0, 7, 40, "EC: ", "Default", "right")
window.printBox(0, 8, 40, "ChipID: ", "Default", "right")
window.printBox(0, 9, 40, "Data 1: ", "Default", "right")
window.printBox(0, 10, 40, "Data 2: ", "Default", "right")
window.printBox(0, 11, 40, "Data 3: ", "Default", "right")
window.printBox(0, 12, 40, "Data 4: ", "Default", "right")
window.printBox(0, 13, 40, "CRC: ", "Default", "right")
window.printBox(0, 14, 40, "BX: ", "Default", "right")

# Get data
while(True):

    window.printBox(40, 6, 40, "", "Default", "left")
    window.printBox(40, 7, 40, "", "Default", "left")
    window.printBox(40, 8, 40, "", "Default", "left")
    window.printBox(40, 9, 40, "", "Default", "left")
    window.printBox(40, 10, 40, "", "Default", "left")
    window.printBox(40, 11, 40, "", "Default", "left")
    window.printBox(40, 12, 40, "", "Default", "left")
    window.printBox(40, 13, 40, "", "Default", "left")
    window.printBox(40, 14, 40, "", "Default", "left")

    time.sleep(0.1)

    # Get a tracking packet (with a limit)
    while (True):

        # Request new data
        isNewData = glib.get("glib_request_tracking_data")
        time.sleep(0.1)

        if (isNewData == 0x1):
            break

    packet1 = glib.get("glib_tracking_data_1")
    packet2 = glib.get("glib_tracking_data_2")
    packet3 = glib.get("glib_tracking_data_3")
    packet4 = glib.get("glib_tracking_data_4")
    packet5 = glib.get("glib_tracking_data_5")
    packet6 = glib.get("glib_tracking_data_6")
    packet7 = glib.get("glib_tracking_data_7")

    bc = hex((0x0fff0000 & packet6) >> 16)
    ec = hex((0x00000ff0 & packet6) >> 4)
    chipid = hex((0x0fff0000 & packet5) >> 16)
    data1 = bin(((0x0000ffff & packet5) << 16) | ((0xffff0000 & packet4) >> 16))
    data2 = bin(((0x0000ffff & packet4) << 16) | ((0xffff0000 & packet3) >> 16))
    data3 = bin(((0x0000ffff & packet3) << 16) | ((0xffff0000 & packet2) >> 16))
    data4 = bin(((0x0000ffff & packet2) << 16) | ((0xffff0000 & packet1) >> 16))
    crc = hex(0x0000ffff & packet1)
    bx = hex(packet7)

    window.printBox(40, 6, 40, bc, "Default", "left")
    window.printBox(40, 7, 40, ec, "Default", "left")
    window.printBox(40, 8, 40, chipid, "Default", "left")
    window.printBox(40, 9, 40, data1, "Default", "left")
    window.printBox(40, 10, 40, data2, "Default", "left")
    window.printBox(40, 11, 40, data3, "Default", "left")
    window.printBox(40, 12, 40, data4, "Default", "left")
    window.printBox(40, 13, 40, crc, "Default", "left")
    window.printBox(40, 14, 40, bx, "Default", "left")

    # Wait for Start signal
    window.waitForKey("s")

# Close window
window.close()
