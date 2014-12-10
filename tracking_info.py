import sys, os, time
sys.path.append('$PYTHONGEMDAQPATH/daqreading/src')
sys.path.append('$PYTHONGEMDAQPATH/daqreading/src/system/')
sys.path.append('$PYTHONGEMDAQPATH/daqreading/src/system/ipbus')

from PyChipsUser import *
glibAddrTable = AddressTable("./glibAddrTable.dat")

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s", "--slot", type="int", dest="slot",
		  help="slot in uTCA crate", metavar="slot", default=115)
parser.add_option("-d", "--debug", action="store_true", dest="debug",
		  help="print debugging information", metavar="debug")
(options, args) = parser.parse_args()

uTCAslot = 115
if options.slot:
	#uTCAslot = 110+options.slot
	uTCAslot = options.slot
print options.slot, uTCAslot
ipaddr = '192.168.0.%d'%(uTCAslot)

########################################
# IP address
########################################
#ipaddr = '192.168.0.115'
glib = ChipsBusUdp(glibAddrTable, ipaddr, 50001)
print "--=======================================--"
print "  Opening GLIB with IP", ipaddr
print "--=======================================--"
########################################
if options.debug:
	chipsLog.setLevel(logging.DEBUG)    # Verbose logging (see packets being sent and received)
print "-> BOARD INFORMATION"
print "--=======================================--"
brd_char 	= ['w','x','y','z']
brd_char[0] = chr(glib.read("board_id_char1"))
brd_char[1] = chr(glib.read("board_id_char2"))
brd_char[2] = chr(glib.read("board_id_char3"))
brd_char[3] = chr(glib.read("board_id_char4"))

board_id = ''.join([brd_char[0],brd_char[1],brd_char[2],brd_char[3]])
print "-> board type  :", board_id




sys_char 	= ['w','x','y','z']
sys_char[0] = chr(glib.read("sys_id_char1"))
sys_char[1] = chr(glib.read("sys_id_char2"))
sys_char[2] = chr(glib.read("sys_id_char3"))
sys_char[3] = chr(glib.read("sys_id_char4"))

sys_id = ''.join([sys_char[0],sys_char[1],sys_char[2],sys_char[3]])
print "-> system type :", sys_id

ver_major = glib.read("ver_major")
ver_minor = glib.read("ver_minor")
ver_build = glib.read("ver_build")
ver = '.'.join([str(ver_major),str(ver_minor),str(ver_build)])
print "-> version nbr :", ver

yyyy  = 2000+glib.read("firmware_yy")
mm  = glib.read("firmware_mm")
dd  = glib.read("firmware_dd")

date = '/'.join([str(dd),str(mm),str(yyyy)])
print "-> sys fw date :", date


mac    = ['00','00','00','00','00','00']
mac[5] = uInt8HexStr(glib.read("mac_b5"))
mac[4] = uInt8HexStr(glib.read("mac_b4"))
mac[3] = uInt8HexStr(glib.read("mac_b3"))
mac[2] = uInt8HexStr(glib.read("mac_b2"))
mac[1] = uInt8HexStr(glib.read("mac_b1"))
mac[0] = uInt8HexStr(glib.read("mac_b0"))
mac_addr = ':'.join([mac[5],mac[4],mac[3],mac[2],mac[1],mac[0]])

print "--=======================================--"
print "Fake tracking data:"
print
from trackingUnpacker import VFAT2TrackingData

#print "column1:"
#column1data = [0]
#data1 = 0
#print "FIFO0 I2CRecCnt = 0x%x"%glib.read("GLIB_link0_I2CRecCnt")
#print "FIFO0 depth = %d"%glib.read("GLIB_link0_FIFO_Occ")
#column1data[0] = glib.read("ch1trackingdata0")
#for hit in range(6):
#	if hit == 0:
#		while ((column1data[0]&0xF000F000) != 0xA000C000):
#			print "trying to find first word"
#			column1data[0] = glib.read("ch1trackingdata%d"%(hit+1))
#	else:
#		column1data.append(glib.read("ch1trackingdata%d"%(hit+1)))
#		
#	#column1data.append(glib.read("trackingdata1"))
#	data1 = (data1<<(32*hit))+column1data[hit]
#print "0x%x"%(data1)
#
#myData = VFAT2TrackingData(column1data)
#myData.printReport()
#
print
print "column2:"
column2data = [0]
data2 = 0
print "OH fw ver:0x%x"%glib.read("OptoHybrid_FW")
glib.write("SendResync",0x1)
glib.write("SendBC0",   0x1)

glib.write("RstL1A",   0x1)
glib.write("RstCal",   0x1)
glib.write("RstResync",0x1)
glib.write("RstBC0",   0x1)

glib.write("TrgSrc",   0x2)

print "FIFO1 I2CRecCnt = 0x%x"%glib.read("GLIB_link1_I2CRecCnt")
print "FIFO0 depth = %d"%glib.read("GLIB_link1_FIFO_Occ")
print "FIFO1 depth = %d"%glib.read("GLIB_link1_FIFO_Occ")
print "FIFO2 depth = %d"%glib.read("GLIB_link1_FIFO_Occ")
print "N L1A %d"%(glib.read("ReadL1A"))
print "N Cal %d"%(glib.read("ReadCal"))
print "N Rsy %d"%(glib.read("ReadResync"))
print "N BC0 %d"%(glib.read("ReadBC0"))
print "N BXC %d"%(glib.read("ReadBX"))


#glib.write("GLIB_link1_FIFO_Flush",0x1)
#glib.write("GLIB_link1_FIFO_Flush",0x1)
#glib.write("GLIB_link1_FIFO_Flush",0x1)
#
glib.write("vfat2_cms_j8_ctrl0",0x0)
glib.write("vfat2_cms_j8_ctrl1",0x0)
glib.write("vfat2_cms_j8_ctrl2",0x0)
glib.write("vfat2_cms_j8_ctrl3",0x0)

print "CtrlReg0::0x%x"%(glib.read("vfat2_totem_j57_ctrl0")&0xFF)
print "CtrlReg1::0x%x"%(glib.read("vfat2_totem_j57_ctrl1")&0xFF)
print "CtrlReg2::0x%x"%(glib.read("vfat2_totem_j57_ctrl2")&0xFF)
print "CtrlReg3::0x%x"%(glib.read("vfat2_totem_j57_ctrl3")&0xFF)
#
#print "FIFO0 depth = %d"%glib.read("GLIB_link1_FIFO_Occ")
#print "FIFO1 depth = %d"%glib.read("GLIB_link1_FIFO_Occ")
#print "FIFO2 depth = %d"%glib.read("GLIB_link1_FIFO_Occ")
column2data[0] = glib.read("ch2trackingdata0")
if (not column2data[0]):
	print "no tracking data first word found, sending test patterns"
	glib.write("vfat2_totem_j57_ctrl0",0x37)
	glib.write("vfat2_totem_j57_ctrl3",0x10)
	time.sleep(5)
	glib.write("vfat2_totem_j57_ctrl3",0x00)
	print "FIFO1 depth = %d (first resend)"%glib.read("GLIB_link1_FIFO_Occ")
	column2data[0] = glib.read("ch2trackingdata0")
	print "N L1A %d"%(glib.read("ReadL1A"))
	print "N Cal %d"%(glib.read("ReadCal"))
	print "N Rsy %d"%(glib.read("ReadResync"))
	print "N BC0 %d"%(glib.read("ReadBC0"))
	print "N BXC %d"%(glib.read("ReadBX"))
	print "column2data[0] 0x%x"%column2data[0]

if (not column2data[0]):
	print "no tracking data first word found, sending test patterns (second time)"
	glib.write("vfat2_totem_j57_ctrl0",0x37)
	glib.write("vfat2_totem_j57_ctrl3",0x10)
	time.sleep(5)
	glib.write("vfat2_totem_j57_ctrl3",0x00)
	print "FIFO1 depth = %d (second resend)"%glib.read("GLIB_link1_FIFO_Occ")
	column2data[0] = glib.read("ch2trackingdata0")
	print "N L1A %d"%(glib.read("ReadL1A"))
	print "N Cal %d"%(glib.read("ReadCal"))
	print "N Rsy %d"%(glib.read("ReadResync"))
	print "N BC0 %d"%(glib.read("ReadBC0"))
	print "N BXC %d"%(glib.read("ReadBX"))
	print "column2data[0] 0x%x"%column2data[0]

if (not column2data[0]):
	print "no tracking data first word found, sending L1A+CalPulse"
	glib.write("vfat2_totem_j57_ctrl0",0x37)
	glib.write("vfat2_totem_j57_ctrl3",0x00)
	glib.write("SendL1ACal",0x0d)
	glib.write("SendL1ACal",0x0e)
	glib.write("SendL1ACal",0x0f)
	glib.write("SendL1ACal",0x10)
	glib.write("SendL1ACal",0x20)
	time.sleep(5)
	print "FIFO1 depth = %d (second resend)"%glib.read("GLIB_link1_FIFO_Occ")
	column2data[0] = glib.read("ch2trackingdata0")
	print "N L1A %d"%(glib.read("ReadL1A"))
	print "N Cal %d"%(glib.read("ReadCal"))
	print "N Rsy %d"%(glib.read("ReadResync"))
	print "N BC0 %d"%(glib.read("ReadBC0"))
	print "N BXC %d"%(glib.read("ReadBX"))
	print "column2data[0] 0x%x"%column2data[0]

if (not column2data[0]):
	print "no tracking data first word found, sending L1As"
	glib.write("vfat2_totem_j57_ctrl0",0x37)
	glib.write("vfat2_totem_j57_ctrl3",0x00)
	glib.write("SendL1A",0x1)
	glib.write("SendL1A",0x1)
	glib.write("SendL1A",0x1)
	glib.write("SendL1A",0x1)
	glib.write("SendL1A",0x1)
	time.sleep(5)
	print "FIFO1 depth = %d (second resend)"%glib.read("GLIB_link1_FIFO_Occ")
	column2data[0] = glib.read("ch2trackingdata0")
	print "N L1A %d"%(glib.read("ReadL1A"))
	print "N Cal %d"%(glib.read("ReadCal"))
	print "N Rsy %d"%(glib.read("ReadResync"))
	print "N BC0 %d"%(glib.read("ReadBC0"))
	print "N BXC %d"%(glib.read("ReadBX"))
	print "column2data[0] 0x%x"%column2data[0]

if (column2data[0]):
	for hit in range(7):
		#if hit == 0:
		#	#while ((column2data[0]&0xF000F000) != 0xA000C000):
		#	#print "trying to find first word (0x%x)"%(column2data[0])
		#	column2data[0] = glib.read("ch2trackingdata%d"%(hit+1))
		#else:
		column2data.append(glib.read("ch2trackingdata%d"%(hit+1)))

	check1 = bin((column2data[6]&0xF0000000)>>28)
	check2 = bin((column2data[6]&0x0000F000)>>12)
	check3 = bin((column2data[5]&0xF0000000)>>28)
	
	bc     = hex((0x0fff0000 & column2data[6]) >> 16)
	ec     = hex((0x00000ff0 & column2data[6]) >> 4)
	chipid = hex((0x0fff0000 & column2data[5]) >> 16)
	data1  = bin(((0x0000ffff & column2data[5]) << 16) | ((0xffff0000 & column2data[4]) >> 16))
	data2  = bin(((0x0000ffff & column2data[4]) << 16) | ((0xffff0000 & column2data[3]) >> 16))
	data3  = bin(((0x0000ffff & column2data[3]) << 16) | ((0xffff0000 & column2data[2]) >> 16))
	data4  = bin(((0x0000ffff & column2data[2]) << 16) | ((0xffff0000 & column2data[1]) >> 16))
	crc    = hex(0x0000ffff & column2data[1])
	bx     = hex(column2data[7])

	#data2 = (data2<<(32*hit))+column2data[hit]
	#print hit, "0x%08x"%(column2data[hit])

	#print "0x%x"%(data2)
	#myData = VFAT2TrackingData(column2data)
	print "N L1A %d"%(glib.read("ReadL1A"))
	print "N Cal %d"%(glib.read("ReadCal"))
	print "N Rsy %d"%(glib.read("ReadResync"))
	print "N BC0 %d"%(glib.read("ReadBC0"))
	print "N BXC %d"%(glib.read("ReadBX"))
	#myData.printReport()

	print "packet6msb = %s"%(bin((0xffff0000&column2data[6])>>16))
	print "packet6lsb = %s"%(bin((0x0000ffff&column2data[6])))
	print "packet5msb = %s"%(bin((0xffff0000&column2data[5])>>16))
	print "packet5lsb = %s"%(bin((0x0000ffff&column2data[5])))
	print "packet4msb = %s"%(bin((0xffff0000&column2data[4])>>16))
	print "packet4lsb = %s"%(bin((0x0000ffff&column2data[4])))
	print "packet3msb = %s"%(bin((0xffff0000&column2data[3])>>16))
	print "packet3lsb = %s"%(bin((0x0000ffff&column2data[3])))
	print "packet2msb = %s"%(bin((0xffff0000&column2data[2])>>16))
	print "packet2lsb = %s"%(bin((0x0000ffff&column2data[2])))
	print "packet1msb = %s"%(bin((0xffff0000&column2data[1])>>16))
	print "packet1lsb = %s"%(bin((0x0000ffff&column2data[1])))

	print "check1 = %s"%(check1)
	print "check2 = %s"%(check2)
	print "check3 = %s"%(check3)
	print "bc     = %s"%(bc    )
	print "ec     = %s"%(ec    )
	print "chipid = %s"%(chipid)
	print "data1  = %s"%(data1 )
	print "data2  = %s"%(data2 )
	print "data3  = %s"%(data3 )
	print "data4  = %s"%(data4 )
	print "crc    = %s"%(crc   )
	print "bx     = %s"%(bx    )

##print
##print "column3:"
##column3data = [3]
##data3 = 0
##print "FIFO2 I2CRecCnt = 0x%x"%glib.read("GLIB_link2_I2CRecCnt")
##print "FIFO2 depth = %d"%glib.read("GLIB_link2_FIFO_Occ")
##column3data[0] = glib.read("ch3trackingdata0")
##for hit in range(6):
##	if hit == 0:
##		while ((column3data[0]&0xF000F000) != 0xA000C000):
##			print "trying to find first word"
##			column3data[0] = glib.read("ch3trackingdata%d"%(hit+1))
##	else:
##		column3data.append(glib.read("ch3trackingdata%d"%(hit+1)))
####for hit in range(6):
####	if hit == 0:
####		while ((column3data[0]&0xF000F000) != 0xA000C000):
####			print "trying to find first word"
####			column3data[0] = glib.read("trackingdata3")
####	else:
####		column3data.append(glib.read("trackingdata3"))
####		
####	#column3data.append(glib.read("trackingdata3"))
##	data3 = (data3<<(32*hit))+column3data[hit]
##print "0x%x"%(data3)
##
##myData = VFAT2TrackingData(column3data)
##myData.printReport()
print
print "--=======================================--"
print
