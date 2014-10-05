#!/usr/bin/python

import sys
from SerialConnection import *
import DMM

# Main program.
if __name__ == "__main__":
    port = sys.argv[1]
    conn = SerialConnection(port)
    dmm  = DMM.Agilent.Agilent(conn)

    # Prints the identification stuff.
    idn = dmm.identify()
    print "Connected to", idn["oem"], idn["model"]

    print dmm.fetch(True, True)
    print dmm.fetch(False, True)

    conn.close()
