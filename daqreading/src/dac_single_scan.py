# System imports
import time
from system import *

# Create window
window = Window("Scan one VFAT2's DAC")

# Get GLIB access
glib = GLIB("192.168.0.115", "register_mapping.dat")
glib.setWindow(window)

# Get a VFAT2 number
window.printBox(0, 4, 30, "Select a VFAT2 to scan [8-13]:", "Default", "left")
inputData = window.getInt(31, 4, 2)
VFAT2 = 8 if (inputData < 8 or inputData > 13) else inputData
window.printBox(31, 4, 3, str(VFAT2), "Input", "left")

# Get the DAC to scan
window.printBox(0, 6, 29, "Select a DAC to scan [1-9]:", "Default", "left")
window.printBox(0, 7, 20, "1: IPreampIn", "Default", "left")
window.printBox(20, 7, 20, "2: IPreampFeed", "Default", "left")
window.printBox(40, 7, 20, "3: IPreampOut", "Default", "left")
window.printBox(60, 7, 20, "4: IShaper", "Default", "left")
window.printBox(0, 8, 20, "5: IShaperFeed", "Default", "left")
window.printBox(20, 8, 20, "6: IComp", "Default", "left")
window.printBox(40, 8, 20, "7: VThreshold1", "Default", "left")
window.printBox(60, 8, 20, "8: VThreshold2", "Default", "left")
window.printBox(0, 9, 20, "9: VCal", "Default", "left")
inputData = window.getInt(28, 6, 1)
DAC = 1 if (inputData < 1 or inputData > 9)  else inputData
window.printBox(28, 6, 3, str(DAC), "Input", "left")

# Limits select
window.printBox(0, 11, 23, "Scan DAC from [0-255]:", "Default", "left")
inputData = window.getInt(23, 11, 3)
minimumValue = 0 if (inputData < 0 or inputData > 255)  else inputData
window.printBox(23, 11, 3, str(minimumValue), "Input", "left")

window.printBox(28, 11, 4, "to", "Default", "left")
inputData = window.getInt(31, 11, 3)
maximumValue = 255 if (inputData < 0 or inputData > 255)  else inputData
window.printBox(31, 11, 3, str(maximumValue), "Input", "left")

# Events per threshold
window.printBox(0, 13, 34, "Number of events per value [100]:", "Default", "left")
inputData = window.getInt(34, 13, 5)
nEvents = 100 if (inputData < 0) else inputData
window.printBox(34, 13, 5, str(nEvents), "Input", "left")

# Save results
window.printBox(0, 15, 4, "Save the results [Y/n]:", "Default", "left")
inputData = window.getChar(24, 15)
saveResults = True if (inputData == "y" or inputData == "Y" or inputData == False)  else False
window.printBox(24, 15, 3, ("Yes" if saveResults else "No"), "Input", "left")

# Wait before starting
window.printLine(17, "Press [s] to start the scan.", "Info", "center")
window.waitForKey("s")

# Test if VFAT2 is present
if (glib.isVFAT2(VFAT2) == False):
    # Error
    window.printLine(18, "The selected VFAT2 is not present!", "Error", "center")
#
else:
    # Set the common registers
    glib.setVFAT2(VFAT2, "ctrl1", DAC)
    glib.setVFAT2(VFAT2, "ctrl0", 0x1)
    glib.set("oh_resync", 1)

    # Create a plot and its data
    dacValues = []
    adcValues = []

    # Loop over DAC
    for dacValue in range(minimumValue, maximumValue):

        # Percentage
        percentage = (dacValue - minimumValue) / (1. * maximumValue - minimumValue) * 100.
        window.printLine(18, "Scanning... (" + str(percentage)[:4] + "%)", "Info", "center")

        # Set the DAC
        if (DAC == 1):
            glib.setVFAT2(VFAT2, "ipreampin", dacValue)
        elif (DAC == 2):
            glib.setVFAT2(VFAT2, "ipreampfeed", dacValue)
        elif (DAC == 3):
            glib.setVFAT2(VFAT2, "ipreampout", dacValue)
        elif (DAC == 4):
            glib.setVFAT2(VFAT2, "ishaper", dacValue)
        elif (DAC == 5):
            glib.setVFAT2(VFAT2, "ishaperfeed", dacValue)
        elif (DAC == 6):
            glib.setVFAT2(VFAT2, "icomp", dacValue)
        elif (DAC == 7):
            glib.setVFAT2(VFAT2, "vthreshold1", dacValue)
        elif (DAC == 8):
            glib.setVFAT2(VFAT2, "vthreshold2", dacValue)
        elif (DAC == 9):
            glib.setVFAT2(VFAT2, "vcal", dacValue)

        # Send Resync signal
        glib.set("oh_resync", 0x1)

        # Wait a second
        time.sleep(0.1)

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
        dacValues.append(dacValue)
        adcValues.append(averageADC)

        # Update plot
        graph(dacValues, adcValues, minimumValue, maximumValue, 0, 4096, "DAC value", "ADC value")

    # Write to file
    if (saveResults):
        fileName = "../data/dac-single-" + time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime()) + ".txt"
        f = open(fileName,"w")
        f.write("DAC Single Scan\n")
        f.write("Time: " + time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()) + "\n")
        f.write("VFAT2: " + str(VFAT2) + "\n")
        f.write("Number of events: " + str(nEvents) + "\n")
        f.write("DAC: " + str(DAC) + "\n")
        f.write("Minimum value: " + str(minimumValue) + "\n")
        f.write("Maximum value: " + str(maximumValue) + "\n")
        f.write("_".join(map(str, dacValues)) + "\n")
        f.write("_".join(map(str, adcValues)) + "\n")
        f.close()

    # Reset the common registers
    glib.setVFAT2(VFAT2, "ctrl1", 0x0)
    glib.setVFAT2(VFAT2, "ctrl0", 0x0)
    glib.set("oh_resync", 1)

    # Success
    window.printLine(18, "Scan finished!", "Success", "center")

# Wait before quiting
window.waitQuit()

# Close window
window.close()
