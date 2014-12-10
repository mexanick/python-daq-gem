# System imports
from system import *

# Get GLIB access
glib = GLIB('192.168.0.115', 'register_mapping.dat')

if (sys.argv[1] == 'w'):
    print "Write to ", sys.argv[2]
    glib.set(sys.argv[2], int(sys.argv[3]))

elif (sys.argv[1] == 'r'):
    print "Read from ", sys.argv[2], " : ", hex(glib.get(sys.argv[2]))





