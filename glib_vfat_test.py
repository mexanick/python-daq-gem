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
print
print "--=======================================--"
print "  Opening GLIB with IP", ipaddr
print "--=======================================--"
print
########################################
#chipsLog.setLevel(logging.DEBUG)    # Verbose logging (see packets being sent and received)
print
print "--=======================================--"
print "-> BOARD INFORMATION"
print "--=======================================--"
print
brd_char 	= ['w','x','y','z']
brd_char[0] = chr(glib.read("board_id_char1"))
brd_char[1] = chr(glib.read("board_id_char2"))
brd_char[2] = chr(glib.read("board_id_char3"))
brd_char[3] = chr(glib.read("board_id_char4"))

print
board_id = ''.join([brd_char[0],brd_char[1],brd_char[2],brd_char[3]])
print "-> board type  :", board_id




sys_char 	= ['w','x','y','z']
sys_char[0] = chr(glib.read("sys_id_char1"))
sys_char[1] = chr(glib.read("sys_id_char2"))
sys_char[2] = chr(glib.read("sys_id_char3"))
sys_char[3] = chr(glib.read("sys_id_char4"))

print
sys_id = ''.join([sys_char[0],sys_char[1],sys_char[2],sys_char[3]])
print "-> system type :", sys_id

ver_major = glib.read("ver_major")
ver_minor = glib.read("ver_minor")
ver_build = glib.read("ver_build")
print
ver = '.'.join([str(ver_major),str(ver_minor),str(ver_build)])
print "-> version nbr :", ver

yyyy  = 2000+glib.read("firmware_yy")
mm  = glib.read("firmware_mm")
dd  = glib.read("firmware_dd")

print
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

#####################################################################
os.system('$PYTHONGEMDAQPATH/daqreading/src/system/ipbus/scripts/glib_i2c_eeprom_read_eui.py')
os.system('$PYTHONGEMDAQPATH/daqreading/src/system/ipbus/scripts/glib_i2c_mac_ip_status.py')
#####################################################################
print
print
print "-> -----------------"
print "-> BOARD STATUS     "
print "-> -----------------"
print "-> sfp1 absent       :", glib.read("glib_sfp1_mod_abs")
print "-> sfp1 rxlos        :", glib.read("glib_sfp1_rxlos")
print "-> sfp1 txfault      :", glib.read("glib_sfp1_txfault")
print "-> sfp2 absent       :", glib.read("glib_sfp2_mod_abs")
print "-> sfp2 rxlos        :", glib.read("glib_sfp2_rxlos")
print "-> sfp2 txfault      :", glib.read("glib_sfp2_txfault")
print "-> sfp3 absent       :", glib.read("glib_sfp3_mod_abs")
print "-> sfp3 rxlos        :", glib.read("glib_sfp3_rxlos")
print "-> sfp3 txfault      :", glib.read("glib_sfp3_txfault")
print "-> sfp4 absent       :", glib.read("glib_sfp4_mod_abs")
print "-> sfp4 rxlos        :", glib.read("glib_sfp4_rxlos")
print "-> sfp4 txfault      :", glib.read("glib_sfp4_txfault")
print "-> ethphy interrupt  :", glib.read("gbe_int")
print "-> fmc1 presence     :", glib.read("fmc1_present")
print "-> fmc2 presence     :", glib.read("fmc2_present")
print "-> fpga reset state  :", glib.read("fpga_reset")
print "-> cdce locked       :", glib.read("cdce_lock")
print "-> cdce locked       :", glib.read("cdce_lock")

#print "-> ip_addr           :", glib.read("ip_addr")
print "-> ip_addr           :%d.%d.%d.%d"%(glib.read("ip_b3"), glib.read("ip_b2"), glib.read("ip_b1"), glib.read("ip_b0"))
amc_slot = glib.read("v6_cpld") & 0x0f

print "-> cpld bus state    :", uInt8HexStr(glib.read("v6_cpld"))
if ((amc_slot>0) and (amc_slot<13)):
	print "-> amc slot #        :", amc_slot
else:
	print "-> amc slot #        :",amc_slot,"[not in crate]"

print "-> mac address (ipb) :", mac_addr

print
print "--=======================================--"
print


ebmask = 0x000000ff

vfats = [
	"totem_j58",
	"cms_j8",
	"totem_j55",	
	"cms_j26",
	"totem_j57",
	"cms_j44",
	]
registers = [
	"ctrl0",#"ctrl1","ctrl2","ctrl3",
	#"hitcounter0","hitcounter1","hitcounter2",
	#"upsetreg","lat"
	]

##for vfat in vfats:
##	regval = glib.read("vfat2_%s_ctrl0"%(vfat)) & ebmask
##	print "0x%02x"%regval
##	regval |= 0x01
##	print "writing 0x%02x to %s"%(regval,vfat)
##	glib.write("vfat2_%s_ctrl0"%(vfat),regval)
##
##time.sleep(5)
chipids = []
thechipid = 0x0000
print "0x%02x"%(glib.read("vfat2_cms_j8_chipid0") & ebmask)
print "0x%02x"%(glib.read("vfat2_cms_j8_chipid0") & ebmask)
print "0x%02x"%(glib.read("vfat2_cms_j8_chipid0") & ebmask)
print "0x%02x"%(glib.read("vfat2_cms_j8_chipid0") & ebmask)

thechipid  = (glib.read("vfat2_cms_j8_chipid1") & ebmask)<<8
thechipid |= (glib.read("vfat2_cms_j8_chipid0") & ebmask)
chipids.append(("cms_j8",thechipid))

thechipid  = (glib.read("vfat2_cms_j26_chipid1") & ebmask)<<8
thechipid |= (glib.read("vfat2_cms_j26_chipid0") & ebmask)
chipids.append(("cms_j26",thechipid))

thechipid  = (glib.read("vfat2_cms_j44_chipid1") & ebmask)<<8
thechipid |= (glib.read("vfat2_cms_j44_chipid0") & ebmask)
chipids.append(("cms_j44",thechipid))

thechipid  = (glib.read("vfat2_totem_j58_chipid1") & ebmask)<<8
thechipid |= (glib.read("vfat2_totem_j58_chipid0") & ebmask)
chipids.append(("totem_j58",thechipid))

thechipid  = (glib.read("vfat2_totem_j55_chipid1") & ebmask)<<8
thechipid |= (glib.read("vfat2_totem_j55_chipid0") & ebmask)
chipids.append(("totem_j55",thechipid))

thechipid  = (glib.read("vfat2_totem_j57_chipid1") & ebmask)<<8
thechipid |= (glib.read("vfat2_totem_j57_chipid0") & ebmask)
chipids.append(("totem_j57",thechipid))

for chip in chipids:
	print chip[0],"0x%04x"%(chip[1])

vfatregs = []
for vfat in vfats:
	for reg in registers:
		#print "reading register: %s_%s"%(vfat,reg)
		vfatregs.append(["%s_%s"%(vfat,reg),glib.read("vfat2_%s_%s"%(vfat,reg))])

for regval in vfatregs:
	print regval[0],"0x%02x::0x%08x"%(regval[1]&ebmask,regval[1])
print
print "--=======================================--"
print

