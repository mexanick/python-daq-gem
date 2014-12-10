# System imports
import time
from system import *

# Create window
window = Window("Scan one VFAT2's threshold")

# Get GLIB access
glib = GLIB("192.168.0.115", "register_mapping.dat")
glib.setWindow(window)

# Get a VFAT2 number
window.printBox(0, 4, 30, "Select a VFAT2 to scan [8-13]:", "Default", "left")
inputData = window.getInt(31, 4, 2)
VFAT2 = 8 if (inputData < 8 or inputData > 13) else inputData
window.printBox(31, 4, 3, str(VFAT2), "Input", "left")

# Limits select
window.printBox(0, 6, 29, "Scan threshold from [0-255]:", "Default", "left")
inputData = window.getInt(29, 6, 3)
minimumValue = 0 if (inputData < 0 or inputData > 255)  else inputData
window.printBox(29, 6, 3, str(minimumValue), "Input", "left")

window.printBox(34, 6, 4, "to", "Default", "left")
inputData = window.getInt(37, 6, 3)
maximumValue = 255 if (inputData < 0 or inputData > 255)  else inputData
window.printBox(37, 6, 3, str(maximumValue), "Input", "left")

# Events per threshold
window.printBox(0, 8, 38, "Number of events per threshold [100]:", "Default", "left")
inputData = window.getInt(38, 8, 5)
nEvents = 100 if (inputData < 0) else inputData
window.printBox(38, 8, 5, str(nEvents), "Input", "left")

# Save results
window.printBox(0, 10, 4, "Save the results [Y/n]:", "Default", "left")
inputData = window.getChar(24, 10)
saveResults = True if (inputData == "y" or inputData == "Y" or inputData == False)  else False
window.printBox(24, 10, 3, ("Yes" if saveResults else "No"), "Input", "left")

# Wait before starting
window.printLine(12, "For this scan to work, the VFAT2 has to be biased and running!", "Warning", "center")
window.printLine(13, "Press [s] to start the scan.", "Info", "center")
window.waitForKey("s")

# Test if VFAT2 is present
testVFAT2Present = glib.getVFAT2(VFAT2, "chipid0")

if (((testVFAT2Present & 0x4000000) >> 26) == 1):
    # Error
    window.printLine(14, "VFAT2 not present!", "Error", "center")

else:

    # Create a plot and its data
    threshold = []
    dataPoints = []

    # Loop over Threshold 1
    for VThreshold1 in range(minimumValue, maximumValue):

        # Percentage
        percentage = (VThreshold1 - minimumValue) / (1. * maximumValue - minimumValue) * 100.
        window.printLine(14, "Scanning... (" + str(percentage)[:4] + "%)", "Info", "center")

        # Set Threshold 1
        glib.setVFAT2(VFAT2, "vthreshold1", VThreshold1)

        # Send Resync signal
        glib.set("oh_resync", 0x1)

        # Empty tracking fifo
        glib.set("glib_empty_tracking_data", 0)

        # Efficiency variable
        hitCount = 0.

        # Read tracking packets
        for i in range(0, nEvents):

            # Send 5 LV1A signal (to be sure...)
            glib.set("oh_lv1a", 0x1)
            glib.set("oh_lv1a", 0x1)
            glib.set("oh_lv1a", 0x1)
            glib.set("oh_lv1a", 0x1)
            glib.set("oh_lv1a", 0x1)
            glib.set("oh_lv1a", 0x1)

            # Get a tracking packet (with a limit)
            while (True):

                # Request new data
                isNewData = glib.get("glib_request_tracking_data")

                if (isNewData == 0x1):
                    break

            packet1 = glib.get("glib_tracking_data_1")
            packet2 = glib.get("glib_tracking_data_2")
            packet3 = glib.get("glib_tracking_data_3")
            packet4 = glib.get("glib_tracking_data_4")
            packet5 = glib.get("glib_tracking_data_5")

            data1 = ((0x0000ffff & packet5) << 16) | ((0xffff0000 & packet4) >> 16)
            data2 = ((0x0000ffff & packet4) << 16) | ((0xffff0000 & packet3) >> 16)
            data3 = ((0x0000ffff & packet3) << 16) | ((0xffff0000 & packet2) >> 16)
            data4 = ((0x0000ffff & packet2) << 16) | ((0xffff0000 & packet1) >> 16)

            if (data1 + data2 + data3 + data4 != 0):
                hitCount += 1.

        hitCount /= (nEvents * 1.)

        # Add data
        threshold.append(VThreshold1)
        dataPoints.append(hitCount)

        # Update plot
        graph(threshold, dataPoints, 0, 255, 0, 1, "Threshold", "Percentage of hits")

        # Wait a bit
        time.sleep(0.1)

    # Write to file
    if (saveResults):
        fileName = "../data/threshold-" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
        f = open(fileName,"w")
        f.write("VThreshold1 Scan\n")
        f.write("Time: " + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")
        f.write("VFAT2: " + str(VFAT2) + "\n")
        f.write("Number of events: " + str(nEvents) + "\n")
        f.write("_".join(map(str, threshold)) + "\n")
        f.write("_".join(map(str, dataPoints)) + "\n")
        f.close()

    # Success
    window.printLine(14, "Scan finished!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
