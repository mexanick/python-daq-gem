# System imports
from system import *

# Create window
window = Window("Empty the trigger data buffer")

# Get GLIB access
glib = GLIB('192.168.0.115', 'register_mapping.dat')
glib.setWindow(window)

# Design
window.printLine(4, "Press [s] to empty the trigger data buffer.", "Info", "center")
window.waitForKey("s")

# Empty the buffers
glib.set('glib_empty_trigger_data', 0)

# Design
window.printLine(5, "Trigger buffers emptied", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
