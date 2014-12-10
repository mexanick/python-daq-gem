import sys, os, time, signal
sys.path.append('$PYTHONGEMDAQPATH/daqreading/src')
sys.path.append('$PYTHONGEMDAQPATH/daqreading/src/system/')
sys.path.append('$PYTHONGEMDAQPATH/daqreading/src/system/ipbus')

from PyChipsUser import *

nOK = 0.
nBadHeader = 0.
nErrorOnRead = 0.
nTimedOut = 0.
nMismatch = 0.
nOthers = 0.

class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def testRead(register, exp):
    global nOK, nBadHeader, nErrorOnRead, nTimedOut, nMismatch, nOthers

    #print "Reading VFAT2 register : ", register

    try:

        controlChar = glib.read(register)

        if (controlChar == exp):

            #print colors.GREEN, "-> Match : ", hex(controlChar), colors.ENDC

            nOK += 1

        else:

            print colors.RED, "-> Error, result does not match expectation : ", hex(controlChar), " != ", hex(exp), colors.ENDC

            nMismatch += 1

    except ChipsException, e:

        print colors.BLUE, "-> Error : ", e, colors.ENDC

        if ('amount of data' in e.value):
            nBadHeader += 1

        elif ('INFO CODE = 0x4L' in e.value):
            nErrorOnRead += 1

        elif ('INFO CODE = 0x6L' in e.value or 'timed out' in e.value):
            print e.value
            nTimedOut += 1

        else:
            nOthers += 1

        pass

def signal_handler(signal, frame):
    global nOK, nBadHeader, nErrorOnRead, nTimedOut, nMismatch, nOthers

    nTotal = nOK + nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers
    nError = nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers

    print
    print "Results on ", int(nTotal), " events"
    print "> ",  colors.GREEN, "OK : ", nOK / nTotal * 100., "%", colors.ENDC
    print "> ",  colors.RED, "Error : ", nError / nTotal * 100., "%", colors.ENDC
    print ">> ", colors.BLUE, "Bad data : ", nBadHeader / nTotal * 100., "%", colors.ENDC
    print ">> ", colors.BLUE, "Error on read : ", nErrorOnRead / nTotal * 100., "%", colors.ENDC
    print ">> ", colors.BLUE, "Timed out : ", nTimedOut / nTotal * 100., "%", colors.ENDC
    print ">> ", colors.BLUE, "Mismatch : ", nMismatch / nTotal * 100., "%", colors.ENDC
    print ">> ", colors.BLUE, "Others : ", nOthers / nTotal * 100., "%", colors.ENDC
    sys.exit(0)

if __name__ == "__main__":

    ipaddr = '192.168.0.115'

    glibAddrTable = AddressTable("./glibAddrTable.dat")
    glib = ChipsBusUdp(glibAddrTable, ipaddr, 50001)

    signal.signal(signal.SIGINT, signal_handler)

    print
    print "Opening GLIB with IP", ipaddr
    print "Processing... press Ctrl+C to terminate and get statistics"

    while True:

        res = testRead("vfat2_ctrl0", 0x1050000)
        # time.sleep(0.001)

        res = testRead("vfat2_ctrl1", 0x1050101)
        # time.sleep(0.001)

        res = testRead("vfat2_ctrl2", 0x1050202)
        # time.sleep(0.001)


