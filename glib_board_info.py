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

print "-> GLIB accessible       :", glib.read("GLIB_TEST")
print "-> GLIB_link1_ErrCnt     :", glib.read("GLIB_link1_ErrCnt")
#glib.write("GLIB_link0_Rst_ErrCnt",0x12)
print "-> GLIB_link1_ErrCnt     :", glib.read("GLIB_link1_ErrCnt")
print "-> GLIB_link1_FIFO_Occ   :", glib.read("GLIB_link1_FIFO_Occ")
print "-> GLIB_link1_I2CRecCnt  :", glib.read("GLIB_link1_I2CRecCnt")
print "-> GLIB_link1_I2CSndCnt  :", glib.read("GLIB_link1_I2CSndCnt")
print "-> GLIB_link1_RegSndCnt  :", glib.read("GLIB_link1_RegSndCnt")
print "-> GLIB_link1_RegRecCnt  :", glib.read("GLIB_link1_RegRecCnt")

print "-> OptoHybrid accessible :", glib.read("OptoHybrid_TEST")
print "-> VFATs accessible      :", glib.read("VFATs_TEST")

print "-> VFAT clock source      :", glib.read("VFAT_SRC")
print "-> VFAT clock backup      :", glib.read("VFAT_BKP")

print "-> CDCE clock source      :", glib.read("CDCE_SRC")
print "-> CDCE clock backup      :", glib.read("CDCE_BKP")

print
print "--=======================================--"


##testing adcs##print "testing ADC values"
##testing adcs##glib.write("vfat2_totem_j57_ctrl0",0x37)
##testing adcs##glib.write("vfat2_totem_j57_ctrl1",0x07)
##testing adcs##
##testing adcs##glib.write("vfat2_totem_j57_vthreshold1",0x04)
##testing adcs##print "VT1 reg 0x%x"%(glib.read("vfat2_totem_j57_vthreshold1")&0x000000ff)
##testing adcs###for step in range(10):
##testing adcs##sleep(5)
##testing adcs##print "VT1 VADC 0x%x"%(glib.read("VADCVal"))
##testing adcs##print "VT1 IADC 0x%x"%(glib.read("IADCVal"))
##testing adcs##	
##testing adcs##glib.write("vfat2_totem_j57_vthreshold1",0x0f)
##testing adcs##print "VT1 reg 0x%x"%(glib.read("vfat2_totem_j57_vthreshold1")&0x000000ff)
##testing adcs###for step in range(10):
##testing adcs##sleep(5)
##testing adcs##print "VT1 VADC 0x%x"%(glib.read("VADCVal"))
##testing adcs##print "VT1 IADC 0x%x"%(glib.read("IADCVal"))
##testing adcs##
##testing adcs##glib.write("vfat2_totem_j57_vthreshold1",0x40)
##testing adcs##print "VT1 reg 0x%x"%(glib.read("vfat2_totem_j57_vthreshold1")&0x000000ff)
##testing adcs###for step in range(10):
##testing adcs##sleep(5)
##testing adcs##print "VT1 VADC 0x%x"%(glib.read("VADCVal"))
##testing adcs##print "VT1 IADC 0x%x"%(glib.read("IADCVal"))
##testing adcs##
##testing adcs##glib.write("vfat2_totem_j57_vthreshold1",0x4f)
##testing adcs##print "VT1 reg 0x%x"%(glib.read("vfat2_totem_j57_vthreshold1")&0x000000ff)
##testing adcs###for step in range(10):
##testing adcs##sleep(5)
##testing adcs##print "VT1 VADC 0x%x"%(glib.read("VADCVal"))
##testing adcs##print "VT1 IADC 0x%x"%(glib.read("IADCVal"))
##testing adcs##
##testing adcs##glib.write("vfat2_totem_j57_vthreshold1",0xff)
##testing adcs##print "VT1 reg 0x%x"%(glib.read("vfat2_totem_j57_vthreshold1")&0x000000ff)
##testing adcs###for step in range(10):
##testing adcs##sleep(5)
##testing adcs##print "VT1 VADC 0x%x"%(glib.read("VADCVal"))
##testing adcs##print "VT1 IADC 0x%x"%(glib.read("IADCVal"))
##testing adcs##
##vfat2_totem_j57_ipreampin  
##vfat2_totem_j57_ipreampfeed
##vfat2_totem_j57_ipreampout 
##vfat2_totem_j57_ishaper    
##vfat2_totem_j57_ishaperfeed
##vfat2_totem_j57_icomp      
##vfat2_totem_j57_vcal       
##vfat2_totem_j57_vthreshold1
##vfat2_totem_j57_vthreshold2
