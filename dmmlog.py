#!/usr/bin/python

import sys
from SerialConnection import *
import DMM

def grab_sample():
    print dmm.fetch(True, True)
    print dmm.fetch(False, True)
    print ""

# Main program.
if __name__ == "__main__":
    port = sys.argv[1]
    conn = SerialConnection(port)
    dmm  = DMM.Agilent.DMM(conn)

    # Prints the identification stuff.
    idn = dmm.identify()
    print "Connected to", idn["oem"], idn["model"]

    thread = DMM.Logging(1, grab_sample)
    thread.start()
    raw_input("Press Enter to continue...\n")
    thread.stop()

    conn.close()

