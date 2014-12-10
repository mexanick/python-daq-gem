# System imports
from system import *

# Create window
window = Window("Start or stop VFAT2s")

# Get GLIB access
glib = GLIB('192.168.0.115', 'register_mapping.dat')
glib.setWindow(window)

# Design
window.printLine(4, "Select the VFAT2s you want to start [1] or stop [0, default]", "Default", "left")

# VFAT2s
VFAT2 = [False, False, False, False, False, False]

window.printBox(0, 5, 11, "VFAT2 #8: ", "Default", "left")
inputData = window.getInt(11, 5, 1)
VFAT2[0] = True if (inputData == 1) else False
window.printBox(11, 5, 5, ("Start" if VFAT2[0] else "Stop"), "Input", "left")

window.printBox(0, 6, 11, "VFAT2 #9: ", "Default", "left")
inputData = window.getInt(11, 6, 1)
VFAT2[1] = True if (inputData == 1) else False
window.printBox(11, 6, 5, ("Start" if VFAT2[1] else "Stop"), "Input", "left")

window.printBox(0, 7, 11, "VFAT2 #10: ", "Default", "left")
inputData = window.getInt(11, 7, 1)
VFAT2[2] = True if (inputData == 1) else False
window.printBox(11, 7, 5, ("Start" if VFAT2[2] else "Stop"), "Input", "left")

window.printBox(0, 8, 11, "VFAT2 #11: ", "Default", "left")
inputData = window.getInt(11, 8, 1)
VFAT2[3] = True if (inputData == 1) else False
window.printBox(11, 8, 5, ("Start" if VFAT2[3] else "Stop"), "Input", "left")

window.printBox(0, 9, 11, "VFAT2 #12: ", "Default", "left")
inputData = window.getInt(11, 9, 1)
VFAT2[4] = True if (inputData == 1) else False
window.printBox(11, 9, 5, ("Start" if VFAT2[4] else "Stop"), "Input", "left")

window.printBox(0, 10, 11, "VFAT2 #13: ", "Default", "left")
inputData = window.getInt(11, 10, 1)
VFAT2[5] = True if (inputData == 1) else False
window.printBox(11, 10, 5, ("Start" if VFAT2[5] else "Stop"), "Input", "left")

# Design
window.printLine(13, "Press [s] to apply the settings.", "Info", "center")
window.waitForKey("s")

#
for i in range(0, 6):
    if (glib.isVFAT2(i + 8) == True):
        config = glib.getVFAT2(i + 8, 'ctrl0')
        if (VFAT2[i] == True):
            glib.setVFAT2(i + 8, 'ctrl0', 0x37)
        else:
            glib.setVFAT2(i + 8, 'ctrl0', 0x36)

# Design
window.printLine(14, "Settings applied!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
