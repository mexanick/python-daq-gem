import sys, os, time, signal, random
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

gDebug  = False
gSleep  = 100
gMAX_RETRIES = 25
gRetries = 0

class colors:
    WHITE   = '\033[97m'
    CYAN    = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE    = '\033[94m'
    YELLOW  = '\033[93m'
    GREEN   = '\033[92m'
    RED     = '\033[91m'
    ENDC    = '\033[0m'

def emptyBuffer():
    global gRetries, gDebug
    #for i in range(0, 16):
    nRetries = 0
    while (nRetries < gMAX_RETRIES):
        try:
            # time.sleep(0.001*gSleep)
            glib.read("testing")
            return
        except ChipsException, e:
            nRetries += 1
            gRetries += 1
            if gDebug:
                print colors.WHITE, "error encountered, retrying operation (%d,%d)"%(nRetries,gRetries), e
            continue
        pass
    print colors.RED, "error encountered, retried operation (%d)"%(nRetries)
    pass
    
def testRead(register, exp):
    global nOK, nBadHeader, nErrorOnRead, nTimedOut, nMismatch, nOthers, gRetries, gDebug
    nRetries = 0
    while (nRetries < gMAX_RETRIES):
        try:
            # time.sleep(0.001*gSleep)
            controlChar = glib.read(register)
            if (controlChar == exp):
                if gDebug:
                    print colors.GREEN, "-> Match : ", hex(controlChar), colors.ENDC
                nOK += 1
            else:
                if gDebug:
                    print colors.CYAN,"mismatch error",register,"-> Error : ", hex(controlChar), " != ", hex(exp), colors.ENDC
                nMismatch += 1
            return controlChar

        except ChipsException, e:
            if ('amount of data' in e.value):
                if gDebug:
                    print colors.BLUE, "bad header",register, "-> Error : ", e, colors.ENDC
                nBadHeader += 1
            elif ('INFO CODE = 0x4L' in e.value):
                if gDebug:
                    print colors.MAGENTA, "read error",register, "-> Error : ", e, colors.ENDC
                nErrorOnRead += 1
            elif ('INFO CODE = 0x6L' in e.value or 'timed out' in e.value):
                if gDebug:
                    print colors.YELLOW, "timed out",register, "-> Error : ", e, colors.ENDC
                nTimedOut += 1
            else:
                if gDebug:
                    print colors.WHITE, "other error",register, "-> Error : ", e, colors.ENDC
                nOthers += 1
            nRetries += 1
            gRetries += 1
            if gDebug:
                print colors.WHITE, "test read error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries), e
            continue
        pass
    print colors.RED, "error encountered, retried test read operation (%d)"%(nRetries)
    pass

def readReg(register):
    global gRetries, gDebug
    nRetries = 0
    while (nRetries < gMAX_RETRIES):
        try:
            if gDebug:
                print "regRead::%s"%(register)
            # time.sleep(0.001*gSleep)
            controlChar = glib.read(register)
            return controlChar & 0x000000ff

        except ChipsException, e:
            if gDebug:
                print colors.RED, "-> Error : ", e, colors.ENDC
            nRetries += 1
            gRetries += 1
            if gDebug:
                print colors.WHITE, "read error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries), e
            continue
        pass
    print colors.RED, "error encountered, retried read operation (%d)"%(nRetries)
    return 0x0


def testWrite(register, value):
    global nOK, nBadHeader, nErrorOnRead, nTimedOut, nMismatch, nOthers, gRetries
    if gDebug:
        print "Writting VFAT2 register : ", register
    nRetries = 0
    while (nRetries < gMAX_RETRIES):
        try:
            # time.sleep(0.001*gSleep)
            glib.write(register, value)
            # if gDebug:
            #    print colors.GREEN, "-> OK : ", hex(controlChar), colors.ENDC
            nOK += 1
            return

        except ChipsException, e:
            if ('amount of data' in e.value):
                if gDebug:
                    print colors.BLUE, "bad header",register, "-> Error : ", e, colors.ENDC
                nBadHeader += 1
            elif ('INFO CODE = 0x4L' in e.value):
                if gDebug:
                    print colors.MAGENTA, "read error",register, "-> Error : ", e, colors.ENDC
                nErrorOnRead += 1
            elif ('INFO CODE = 0x6L' in e.value or 'timed out' in e.value):
                if gDebug:
                    print colors.YELLOW, "timed out",register, "-> Error : ", e, colors.ENDC
                nTimedOut += 1
            else:
                if gDebug:
                    print colors.WHITE, "other error",register, "-> Error : ", e, colors.ENDC
                nOthers += 1
            nRetries += 1
            gRetries += 1
            if gDebug:
                print colors.WHITE, "test write error encountered (%s), retrying operation (%d,%d)"%(register,nRetries,gRetries), e
            continue
        pass
    print colors.RED, "error encountered, retried test write operation (%d)"%(nRetries)
    pass

def signal_handler(signal, frame):
    printReport()
    #global nOK, nBadHeader, nErrorOnRead, nTimedOut, nMismatch, nOthers, gRetries
    #nTotal = nOK + nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers
    #nError = nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers
    #
    #if nTotal == 0:
    #    nTotal = 1
    #
    ##print
    #print "Results on ", int(nTotal), " events"
    #print ">  ", colors.GREEN,  "OK            : %10.4f%% (%5d/%d)"%(nOK          / nTotal * 100., nOK         ,nTotal), colors.ENDC
    #print ">  ", colors.RED,    "Error         : %10.4f%% (%5d/%d)"%(nError       / nTotal * 100., nError      ,nTotal), colors.ENDC
    #print ">> ", colors.PINK,   "Bad data      : %10.4f%% (%5d/%d)"%(nBadHeader   / nTotal * 100., nBadHeader  ,nTotal), colors.ENDC
    #print ">> ", colors.YELLOW, "Error on read : %10.4f%% (%5d/%d)"%(nErrorOnRead / nTotal * 100., nErrorOnRead,nTotal), colors.ENDC
    #print ">> ", colors.ORANGE, "Timed out     : %10.4f%% (%5d/%d)"%(nTimedOut    / nTotal * 100., nTimedOut   ,nTotal), colors.ENDC
    #print ">> ", colors.VIOLET, "Mismatch      : %10.4f%% (%5d/%d)"%(nMismatch    / nTotal * 100., nMismatch   ,nTotal), colors.ENDC
    #print ">> ", colors.BLUE,   "Others        : %10.4f%% (%5d/%d)"%(nOthers      / nTotal * 100., nOthers     ,nTotal), colors.ENDC
    sys.exit(0)

def printReport():
#def signal_handler():
    global nOK, nBadHeader, nErrorOnRead, nTimedOut, nMismatch, nOthers, gRetries
    nTotal = nOK + nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers
    nError = nBadHeader + nErrorOnRead + nTimedOut + nMismatch + nOthers

    if nTotal == 0:
        nTotal = 1

    #print
    print "Results on ", int(nTotal), " events"
    print ">  ", colors.GREEN,   "OK            : %10.4f%% (%5d/%d)"%(nOK          / nTotal * 100., nOK         ,nTotal), colors.ENDC
    print ">  ", colors.RED,     "Error         : %10.4f%% (%5d/%d)"%(nError       / nTotal * 100., nError      ,nTotal), colors.ENDC
    print ">> ", colors.BLUE,    "Bad data      : %10.4f%% (%5d/%d)"%(nBadHeader   / nTotal * 100., nBadHeader  ,nTotal), colors.ENDC
    print ">> ", colors.MAGENTA, "Error on read : %10.4f%% (%5d/%d)"%(nErrorOnRead / nTotal * 100., nErrorOnRead,nTotal), colors.ENDC
    print ">> ", colors.YELLOW,  "Timed out     : %10.4f%% (%5d/%d)"%(nTimedOut    / nTotal * 100., nTimedOut   ,nTotal), colors.ENDC
    print ">> ", colors.CYAN,    "Mismatch      : %10.4f%% (%5d/%d)"%(nMismatch    / nTotal * 100., nMismatch   ,nTotal), colors.ENDC
    print ">> ", colors.WHITE,   "Others        : %10.4f%% (%5d/%d)"%(nOthers      / nTotal * 100., nOthers     ,nTotal), colors.ENDC
    print ">> ", colors.RED,     "Retries       : %10d"             %(gRetries), colors.ENDC


from optparse import OptionParser
from datetime import timedelta
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-l", "--duration", type="int", dest="duration", default=1,
                      help="Duration of test in minutes", metavar="duration")
    parser.add_option("-s", "--slot", type="int", dest="slot",
                      help="slot in uTCA crate", metavar="slot", default=5)
    parser.add_option("-w", "--wait", type="int", dest="wait",
                      help="sleep time in ms", metavar="wait", default=100)
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      help="debug", metavar="debug")
    (options, args) = parser.parse_args()
    
    uTCAslot = 115
    if options.slot:
	uTCAslot = 110+options.slot
    ipaddr = '192.168.0.%d'%(110+options.slot)
    
    #global gDebug
    gDebug = options.debug
    gSleep = options.wait

    glibAddrTable = AddressTable("./glibAddrTable.dat")
    glib = ChipsBusUdp(glibAddrTable, ipaddr, 50001)

    signal.signal(signal.SIGINT, signal_handler)

    print
    print "Opening GLIB with IP", ipaddr
    print "Processing (for %d seconds)... press Ctrl+C to terminate and get statistics sooner"%(options.duration*15)
    #######user input testing on specific values
    #####while True:
    ####    #raw_input("Press enter to send read command to response register")
    ####    #print "0x%02x"%(readReg("vfat2_response"))
    ####    #raw_input("Press enter to send read command to chipID0 register")
    ####    #print "0x%02x"%readReg("vfat2_cms_j8_chipid0")
    ####    #raw_input("Press enter to send read command to chipID1 register")
    ####    #print "0x%02x"%readReg("vfat2_cms_j8_chipid1")
    ####    #raw_input("Press enter to send read command to chipID0 register")
    ####    #print "0x%02x"%readReg("vfat2_totem_j58_chipid0")
    ####    #raw_input("Press enter to send read command to chipID1 register")
    ####    #print "0x%02x"%readReg("vfat2_totem_j58_chipid1")
    ####    #raw_input("Press enter to send read command to chipid0 register")
    ####    #print "0x%02x"%readReg("vfat2_totem_j55_chipid0")
    ####    #raw_input("Press enter to send read command to chipid1 register")
    ####    #print "0x%02x"%readReg("vfat2_totem_j55_chipid1")
    ####    #raw_input("Press enter to send read command to chipid0 register")
    ####    #print "0x%02x"%readReg("vfat2_cms_j26_chipid0")
    ####    #raw_input("Press enter to send read command to chipid1 register")
    ####    #print "0x%02x"%readReg("vfat2_cms_j26_chipid1")
    ####    #raw_input("Press enter to send read command to chipid0 register")
    ####    #print "0x%02x"%readReg("vfat2_cms_j44_chipid0")
    ####    #raw_input("Press enter to send read command to chipid1 register")
    ####    #print "0x%02x"%readReg("vfat2_cms_j44_chipid1")
    ####    #raw_input("Press enter to send read command to chipid0 register")
    ####    #print "0x%02x"%readReg("vfat2_totem_j57_chipid0")
    ####    #raw_input("Press enter to send read command to chipid1 register")
    ####    #print "0x%02x"%readReg("vfat2_totem_j57_chipid1")
    ####    
    ##### Empty buffer
    emptyBuffer()
    
    vfats = [
        ["cms_j8",    0x3090000, [0x78, 0xfa],0x00],
        ["cms_j26",   0x30b0000, [0x84, 0xfa],0x00],
        ["cms_j44",   0x30d0000, [0x80, 0xfa],0x00],
        ["totem_j58", 0x3080000, [0x68, 0xb0],0x00],
        ["totem_j55", 0x30a0000, [0xe8, 0xc0],0x00],
        ["totem_j57", 0x30c0000, [0x68, 0xbc],0x00],
        ]
    regsToCheck = [
        ["chipid0", 0x0800],
        ["chipid1", 0x0900],
        ["ctrl0",   0x0000],
        ["ctrl1",   0x0100],
        ["ctrl2",   0x9500],
        ["ctrl3",   0x9600],

        ["ipreampin",   0x0200],
        ["ipreampfeed", 0x0300],
        ["ipreampout",  0x0400],
        ["ishaper",     0x0500],
        ["ishaperfeed", 0x0600],
        ["icomp",       0x0700],

        ["vthreshold1",   0x9200],
        ["vthreshold2",   0x9300],

        ["upsetreg",    0x0a00],
        ["hitcounter0", 0x0b00],
        ["hitcounter1", 0x0c00],
        ["hitcounter2", 0x0d00],

        ["lat",      0x1000],
        ["vcal",     0x9100],
        ["calphase", 0x9400],
        ]
    ##j8  = 0xfa68
    ##j26 = 0xfa78
    ##j44 = 0xfa84
    ##j58 = 0xb080
    ##j55 = 0xc068
    ##j57 = 0xbce8
    #for vfat in vfats:
    #    for reg in regsToCheck:
    #        print "%s_%s"%(vfat[0],reg[0]), "0x%02x"%readReg("vfat2_%s_%s"%(vfat[0],reg[0]))
    #        
    #raw_input("Press enter to run tests")
    #emptyBuffer()
    
    qmins = 0
    start = time.time()
    print start
    dtime = 0
    check = True
    
    ## full tests
    while (check):
        for vfat in vfats:
            for reg in regsToCheck: 
                if "chipid" not in reg[0] and "hitcounter" not in reg[0] and "upset" not in reg[0]:
                    if gDebug:
                        print reg[0]
                    val = random.randint(0, 255)
                    res = vfat[1]+reg[1] + val
                    if gDebug:
                        print "testing write/read with %s_%s 0x%02x 0x%08x"%(vfat[0],reg[0],val,res)
                        print "0x%x, 0x%x"%(readReg( "vfat2_%s_%s"%(vfat[0],reg[0])),val)
                    testWrite("vfat2_%s_%s"%(vfat[0],reg[0]), val)
                    testRead( "vfat2_%s_%s"%(vfat[0],reg[0]), res)
                elif "chipid" in reg[0]:
                    res = vfat[1]+reg[1] + vfat[2][0]
                    if "chipid1" in reg[0]:
                        res = vfat[1]+reg[1] + vfat[2][1]
                    testRead( "vfat2_%s_%s"%(vfat[0],reg[0]), res)
                else:
                    res = vfat[1]+reg[1]
                    #testRead( "vfat2_%s_%s"%(vfat[0],reg[0]), res)
                    readReg( "vfat2_%s_%s"%(vfat[0],reg[0]))
    
                dtime = time.time()-start
                if int(dtime%15) == 14:
                    print qmins, dtime, int(dtime%15)
                    qmins = qmins + 1
                    printReport()
                    time.sleep(1)
                    sys.stdout.flush()
                if options.duration > 0:
                    check = not ((qmins+1) > options.duration)
                if not check:
                    break
            if not check:
                break
        if not check:
            break
    printReport()
    sys.stdout.flush()
