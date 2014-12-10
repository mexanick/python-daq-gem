# System imports
import time
from system import *

# Create window
window = Window("Scan all VFAT2's DACs")

# Get GLIB access
glib = GLIB("192.168.0.115", "register_mapping.dat")
glib.setWindow(window)

# Get a VFAT2 number
window.printBox(0, 4, 30, "Select a VFAT2 to scan [8-13]:", "Default", "left")
inputData = window.getInt(31, 4, 2)
VFAT2 = 8 if (inputData < 8 or inputData > 13) else inputData
window.printBox(31, 4, 3, str(VFAT2), "Input", "left")

# Events per threshold
window.printBox(0, 6, 34, "Number of events per value [100]:", "Default", "left")
inputData = window.getInt(34, 6, 5)
nEvents = 100 if (inputData < 0) else inputData
window.printBox(34, 6, 5, str(nEvents), "Input", "left")

# Save results
window.printBox(0, 8, 4, "Save the results [Y/n]:", "Default", "left")
inputData = window.getChar(24, 8)
saveResults = True if (inputData == "y" or inputData == "Y" or inputData == False)  else False
window.printBox(24, 8, 3, ("Yes" if saveResults else "No"), "Input", "left")

# Wait before starting
window.printLine(10, "Press [s] to start the scan.", "Info", "center")
window.waitForKey("s")

# Test if VFAT2 is present
if (glib.isVFAT2(VFAT2) == False):
    # Error
    window.printLine(11, "The selected VFAT2 is not present!", "Error", "center")
#
else:

    # Turn VFAT2 on
    glib.setVFAT2(VFAT2, "ctrl0", 0x1)

    dacValues = [None] * 9
    adcValues = [None] * 9

    for DAC in range(1, 10):

        # Set the DAC register
        glib.setVFAT2(VFAT2, "ctrl1", DAC)

        # Create a plot and its data
        dacValues[DAC - 1] = []
        adcValues[DAC - 1] = []

        # Loop over DAC
        for dacValue in range(0, 255):

            # Set the DAC
            if (DAC == 1):
                glib.setVFAT2(VFAT2, "ipreampin", dacValue)
                dacName = "IPreampIn"
            elif (DAC == 2):
                glib.setVFAT2(VFAT2, "ipreampfeed", dacValue)
                dacName = "IPreampFeed"
            elif (DAC == 3):
                glib.setVFAT2(VFAT2, "ipreampout", dacValue)
                dacName = "IPreampOut"
            elif (DAC == 4):
                glib.setVFAT2(VFAT2, "ishaper", dacValue)
                dacName = "IShaper"
            elif (DAC == 5):
                glib.setVFAT2(VFAT2, "ishaperfeed", dacValue)
                dacName = "IShaperFeed"
            elif (DAC == 6):
                glib.setVFAT2(VFAT2, "icomp", dacValue)
                dacName = "IComp"
            elif (DAC == 7):
                glib.setVFAT2(VFAT2, "vthreshold1", dacValue)
                dacName = "VThreshold1"
            elif (DAC == 8):
                glib.setVFAT2(VFAT2, "vthreshold2", dacValue)
                dacName = "VThreshold2"
            elif (DAC == 9):
                glib.setVFAT2(VFAT2, "vcal", dacValue)
                dacName = "VCal"

            # Success
            window.printLine(11, "Scanning... Current DAC: " + dacName, "Info", "center")

            # Send Resync signal
            glib.set("oh_resync", 0x1)

            # Average ADC value
            averageADC = 0

            # Get N ADC
            for i in range(0, nEvents):

                time.sleep(0.1)

                if (DAC <= 6):
                    averageADC += glib.get("oh_adc_i")
                else:
                    averageADC += glib.get("oh_adc_v")

            averageADC /= (nEvents * 1.)

            # Add data
            dacValues[DAC - 1].append(dacValue)
            adcValues[DAC - 1].append(averageADC)

            # Update plot
            graph(dacValues[DAC - 1], adcValues[DAC - 1], 0, 255, 0, 4096, "DAC value", "ADC value")

    # Write to file
    if (saveResults):
        fileName = "../data/dac-all-" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
        f = open(fileName,"w")
        f.write("DAC All Scan\n")
        f.write("Time: " + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")
        f.write("VFAT2: " + str(VFAT2) + "\n")
        f.write("Number of events: " + str(nEvents) + "\n")
        for DAC in range(1, 10):
            f.write("_".join(map(str, dacValues[DAC - 1])) + "\n")
            f.write("_".join(map(str, adcValues[DAC - 1])) + "\n")
        f.close()

    # Reset the common registers
    glib.setVFAT2(VFAT2, "ctrl1", 0x0)
    glib.setVFAT2(VFAT2, "ctrl0", 0x0)
    glib.set("oh_resync", 1)

    # Success
    window.printLine(12, "Scan finished!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
