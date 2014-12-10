# System imports
from system import *

# Create window
window = Window("OptoHybrid configuration")

# Get GLIB access
glib = GLIB('192.168.0.115', 'register_mapping.dat')
glib.setWindow(window)

# Print GLIB firmware version
glib_firmware_version = glib.get('glib_firmware_version')
window.printBox(0, 4, 40, "GLIB firmware version: ", "Default", "right")
window.printBox(40, 4, 40, hex(glib_firmware_version), "Default", "left")

# Print OptoHybrid firmware version
oh_firmware_version = glib.get('oh_firmware_version')
window.printBox(0, 5, 40, "OptoHybrid firmware version: ", "Default", "right")
window.printBox(40, 5, 40, hex(oh_firmware_version), "Default", "left")

# Design
window.printLine(7, "General settings", "Info", "center")

# Settings
window.printBox(0, 9, 40, "Trigger source: ", "Default", "right")
window.printBox(0, 10, 40, "SBit select: ", "Default", "right")
window.printBox(0, 11, 40, "VFAT2 clock source: ", "Default", "right")
window.printBox(0, 12, 40, "VFAT2 allow fallback: ", "Default", "right")
window.printBox(0, 13, 40, "CDCE clock source: ", "Default", "right")
window.printBox(0, 14, 40, "CDCE allow fallback: ", "Default", "right")

window.printBox(45, 9, 30, "[0: internal, 1: external, 2: both]", "Default", "left")
window.printBox(45, 10, 30, "[VFAT2 # : 0 - 5]", "Default", "left")
window.printBox(45, 11, 30, "[0: internal, 1: external]", "Default", "left")
window.printBox(45, 12, 30, "[0]", "Default", "left")
window.printBox(45, 13, 30, "[0: internal, 1: external] ", "Default", "left")
window.printBox(45, 14, 30, "[0] ", "Default", "left")

# Get values
trig = window.getInt(40, 9, 5)
sbit = window.getInt(40, 10, 5)
vfat2clk = window.getInt(40, 11, 5)
vfat2fallback = window.getInt(40, 12, 5)
cdceclk = window.getInt(40, 13, 5)
cdcefallback = window.getInt(40, 14, 5)

if (trig == -1):
    trig = 0
if (sbit == -1):
    sbit = 0
if (vfat2clk == -1):
    vfat2clk = 0
if (vfat2fallback == -1):
    vfat2fallback = 0
if (cdceclk == -1):
    cdceclk = 0
if (cdcefallback == -1):
    cdcefallback = 0

# Design
window.printLine(16, "Press [s] to apply the settings or [ctrl+c] to quit", "Info", "center")

# Wait for Start signal
window.waitForKey("s")

# Apply values
glib.set('oh_trigger_source', trig)
glib.set('oh_sbit_select', sbit)
glib.set('oh_vfat2_src_select', vfat2clk)
glib.set('oh_vfat2_fallback', vfat2fallback)
glib.set('oh_cdce_src_select', cdceclk)
glib.set('oh_cdce_fallback', cdcefallback)

# Design
window.printLine(17, "Settings applied", "Success", "center")
window.printLine(18, "Press [q] to quit the program", "Warning", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
