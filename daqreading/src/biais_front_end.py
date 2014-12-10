# System imports
from system import *

# Create window
window = Window("Bias a VFAT2's front-end")

# Get GLIB access
glib = GLIB("192.168.0.115", "register_mapping.dat")
glib.setWindow(window)

# Get a VFAT2 number
window.printBox(0, 4, 30, "Select a VFAT2 to scan [8-13]:", "Default", "left")
inputData = window.getInt(31, 4, 2)
VFAT2 = 8 if (inputData < 8 or inputData > 13) else inputData
window.printBox(31, 4, 3, str(VFAT2), "Input", "left")

# Get a IPreampIn
window.printBox(0, 6, 20, "IPreampIn:", "Default", "left")
window.printBox(17, 6, 10, "[168]", "Default", "left")
inputData = window.getInt(13, 6, 3)
IPreampIn = 168 if (inputData < 0 or inputData > 255) else inputData
window.printBox(13, 6, 3, str(IPreampIn), "Input", "left")

# Get a IPreampFeed
window.printBox(0, 7, 20, "IPreampFeed:", "Default", "left")
window.printBox(17, 7, 10, "[80]", "Default", "left")
inputData = window.getInt(13, 7, 3)
IPreampFeed = 80 if (inputData < 0 or inputData > 255) else inputData
window.printBox(13, 7, 3, str(IPreampFeed), "Input", "left")

# Get a IPreampOut
window.printBox(0, 8, 20, "IPreampOut:", "Default", "left")
window.printBox(17, 8, 10, "[150]", "Default", "left")
inputData = window.getInt(13, 8, 3)
IPreampOut = 150 if (inputData < 0 or inputData > 255) else inputData
window.printBox(13, 8, 3, str(IPreampOut), "Input", "left")

# Get a IShaper
window.printBox(0, 9, 20, "IShaper:", "Default", "left")
window.printBox(17, 9, 10, "[150]", "Default", "left")
inputData = window.getInt(13, 9, 3)
IShaper = 150 if (inputData < 0 or inputData > 255) else inputData
window.printBox(13, 9, 3, str(IShaper), "Input", "left")

# Get a IShaperFeed
window.printBox(0, 10, 20, "IShaperFeed:", "Default", "left")
window.printBox(17, 10, 10, "[100]", "Default", "left")
inputData = window.getInt(13, 10, 3)
IShaperFeed = 100 if (inputData < 0 or inputData > 255) else inputData
window.printBox(13, 10, 3, str(IShaperFeed), "Input", "left")

# Get a IComp
window.printBox(0, 11, 20, "IComp:", "Default", "left")
window.printBox(17, 11, 10, "[120]", "Default", "left")
inputData = window.getInt(13, 11, 3)
IComp = 120 if (inputData < 0 or inputData > 255) else inputData
window.printBox(13, 11, 3, str(IComp), "Input", "left")

# Get a VThreshold1
window.printBox(0, 12, 20, "VThreshold1:", "Default", "left")
window.printBox(17, 12, 10, "[10]", "Default", "left")
inputData = window.getInt(13, 12, 3)
VThreshold1 = 10 if (inputData < 0 or inputData > 255) else inputData
window.printBox(13, 12, 3, str(VThreshold1), "Input", "left")

# Get a VThreshold2
window.printBox(0, 13, 20, "VThreshold2:", "Default", "left")
window.printBox(17, 13, 10, "[0]", "Default", "left")
inputData = window.getInt(13, 13, 3)
VThreshold2 = 0 if (inputData < 0 or inputData > 255) else inputData
window.printBox(13, 13, 3, str(VThreshold2), "Input", "left")

window.printLine(15, "Press [s] to bias the front-end.", "Info", "center")
window.waitForKey("s")

# Test if VFAT2 is present
if (glib.isVFAT2(VFAT2) == False):
    # Error
    window.printLine(16, "The selected VFAT2 is not present!", "Error", "center")
#
else:
    # Bias front-end
    glib.setVFAT2(VFAT2, "ipreampin", IPreampIn)
    glib.setVFAT2(VFAT2, "ipreampfeed", IPreampFeed)
    glib.setVFAT2(VFAT2, "ipreampout", IPreampOut)
    glib.setVFAT2(VFAT2, "ishaper", IShaper)
    glib.setVFAT2(VFAT2, "ishaperfeed", IShaperFeed)
    glib.setVFAT2(VFAT2, "icomp", IComp)
    glib.setVFAT2(VFAT2, "vthreshold1", VThreshold1)
    glib.setVFAT2(VFAT2, "vthreshold2", VThreshold2)
    glib.set("oh_resync", 0)

    # Success
    window.printLine(16, "Front-end biased!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
