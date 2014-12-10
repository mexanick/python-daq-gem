# System imports
import time
from system import *

# Create window
window = Window("Observer trigger data")

# Get GLIB access
glib = GLIB('192.168.0.115', 'register_mapping.dat')
glib.setWindow(window)

# Empty trigger data
glib.set("glib_empty_trigger_data", 0)

# Design
window.printLine(4, "Press [s] to get a new data packet.", "Info", "center")
window.waitForKey("s")

# Design
window.printBox(0, 6, 40, "BX: ", "Default", "right")
window.printBox(0, 7, 40, "SBits: ", "Default", "right")

# Get data
while(True):

    window.printBox(40, 6, 40, "", "Default", "left")
    window.printBox(40, 7, 40, "", "Default", "left")

    time.sleep(0.1)

    packet1 = glib.get("glib_request_trigger_data")

    bx = hex((0xffffffc0 & packet1) >> 6)
    sbits = bin(0x0000003f & packet1)

    window.printBox(40, 6, 40, bx, "Default", "left")
    window.printBox(40, 7, 40, sbits, "Default", "left")

    # Wait for Start signal
    window.waitForKey("s")

# Close window
window.close()
