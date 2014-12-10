import threading
import sys, os, time, signal
sys.path.append('$PYTHONGEMDAQPATH/daqreading/src')
sys.path.append('$PYTHONGEMDAQPATH/daqreading/src/system/')
sys.path.append('$PYTHONGEMDAQPATH/daqreading/src/system/ipbus')

from PyChipsUser import *

nOK          = 0.
nBadHeader   = 0.
nErrorOnRead = 0.
nTimedOut    = 0.
nMismatch    = 0.
nOthers      = 0.

class colors:
    BLUE   = '\033[94m'
    GREEN  = '\033[92m'
    ORANGE = '\033[93m'
    RED    = '\033[91m'
    ENDC   = '\033[0m'

def timer():
   now = time.localtime(time.time())
   return now[5]

def testRead(register, exp):
    global nOK, nBadHeader, nErrorOnRead, nTimedOut, nMismatch, nOthers

    # print "Reading VFAT2 register : ", register

    try:

        controlChar = glib.read(register)

        if (controlChar == exp):

            # print colors.GREEN, "-> Match : ", hex(controlChar), colors.ENDC

            nOK += 1

        else:

            # print colors.RED, "-> Error, result does not match expectation : ", hex(controlChar), " != ", hex(exp), colors.ENDC

            nMismatch += 1

    except ChipsException, e:

        # print colors.BLUE, "-> Error : ", e, colors.ENDC

        if ('amount of data' in e.value):
            nBadHeader += 1

        elif ('INFO CODE = 0x4L' in e.value):
            nErrorOnRead += 1

        elif ('INFO CODE = 0x6L' in e.value or 'timed out' in e.value):
            nTimedOut += 1

        else:
            nOthers += 1

        pass

def signal_handler(signal, frame):
#def signal_handler():
    global nOK, nBadHeader, nErrorOnRead, nTimedOut, nMismatch, nOthers

    nTotal = nOK + nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers
    nError = nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers

    #print
    print "Results on ", int(nTotal), " events"
    print ">  ", colors.GREEN, "OK            : %10.4f%% (%5d/%d)"%(nOK          / nTotal * 100., nOK         ,nTotal), colors.ENDC
    print ">  ", colors.RED,   "Error         : %10.4f%% (%5d/%d)"%(nError       / nTotal * 100., nError      ,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Bad data      : %10.4f%% (%5d/%d)"%(nBadHeader   / nTotal * 100., nBadHeader  ,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Error on read : %10.4f%% (%5d/%d)"%(nErrorOnRead / nTotal * 100., nErrorOnRead,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Timed out     : %10.4f%% (%5d/%d)"%(nTimedOut    / nTotal * 100., nTimedOut   ,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Mismatch      : %10.4f%% (%5d/%d)"%(nMismatch    / nTotal * 100., nMismatch   ,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Others        : %10.4f%% (%5d/%d)"%(nOthers      / nTotal * 100., nOthers     ,nTotal), colors.ENDC
    sys.exit(0)
    
def printReport():
#def signal_handler():
    global nOK, nBadHeader, nErrorOnRead, nTimedOut, nMismatch, nOthers

    nTotal = nOK + nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers
    nError = nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers

    #print
    print "Results on ", int(nTotal), " events"
    print ">  ", colors.GREEN, "OK            : %10.4f%% (%5d/%d)"%(nOK          / nTotal * 100., nOK         ,nTotal), colors.ENDC
    print ">  ", colors.RED,   "Error         : %10.4f%% (%5d/%d)"%(nError       / nTotal * 100., nError      ,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Bad data      : %10.4f%% (%5d/%d)"%(nBadHeader   / nTotal * 100., nBadHeader  ,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Error on read : %10.4f%% (%5d/%d)"%(nErrorOnRead / nTotal * 100., nErrorOnRead,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Timed out     : %10.4f%% (%5d/%d)"%(nTimedOut    / nTotal * 100., nTimedOut   ,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Mismatch      : %10.4f%% (%5d/%d)"%(nMismatch    / nTotal * 100., nMismatch   ,nTotal), colors.ENDC
    print ">> ", colors.BLUE,  "Others        : %10.4f%% (%5d/%d)"%(nOthers      / nTotal * 100., nOthers     ,nTotal), colors.ENDC

    
from optparse import OptionParser
from datetime import timedelta
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-l", "--duration", type="int", dest="duration",
                      help="Duration of test in minutes", metavar="duration")
    parser.add_option("-s", "--slot", type="int", dest="slot",
                      help="slot in uTCA crate", metavar="slot", default=5)
    (options, args) = parser.parse_args()
    
    uTCAslot = 115
    if options.slot:
	uTCAslot = 110+options.slot
    ipaddr = '192.168.0.%d'%(110+options.slot)

    glibAddrTable = AddressTable("./glibAddrTable.dat")
    glib = ChipsBusUdp(glibAddrTable, ipaddr, 50001)

    signal.signal(signal.SIGINT, signal_handler)

    print
    print "Opening GLIB with IP", ipaddr
    print "Processing (for %d seconds)... press Ctrl+C to terminate and get statistics sooner"%(options.duration*15)
    
    qmins = 0
    start = time.time()
    print start
    dtime = 0
    check = True
        #while not ((qmins+1) > options.duration):
    #while (True):
    offset = 0x1050000
    while (check):
        for val in range(48):
            #print offset+val,"0x%x"%(offset+val)
            #print offset+val+(val<<8),"0x%x"%(offset+val+(val<<8))
            res = testRead("vfat2_ctrl%x"%val, offset+val+(val<<8))
            #time.sleep(0.0005)
#        res = testRead("vfat2_ctrl0", offset+val)
##        time.sleep(0.0005)
#
#        res = testRead("vfat2_ctrl1", 0x1050101)
##        time.sleep(0.0007)
#
#        res = testRead("vfat2_ctrl2", 0x1050202)
##        time.sleep(0.0009)
        dtime = time.time()-start
        if int(dtime%15) == 14:
            print qmins, dtime, int(dtime%15)
            qmins = qmins + 1
            printReport()
            time.sleep(1)
            sys.stdout.flush()
        if options.duration > 0:
            check = not ((qmins+1) > options.duration)
    printReport()
    sys.stdout.flush()
    
