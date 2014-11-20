#!/usr/bin/python

import sys
import time
import DMM

def grab_sample(dmm, csv, count):
    tmp_data = [ count[0], time.strftime("%c"),
            dmm.fetch(True, False), dmm.fetch(False, False) ]

    line = str(tmp_data[0]) + "," + tmp_data[1] + "," + tmp_data[2][:-1] + "," + tmp_data[3][:-1] + ",\n"
    csv.write(line.encode('ascii', 'ignore').decode('ascii'))

    print("Reading %d:" % tmp_data[0])
    print tmp_data[2]
    print tmp_data[3]
    print "-----------"

    count[0] += 1

# Main program.
if __name__ == "__main__":
    port = sys.argv[1]
    conn = DMM.SerialConnection(port)
    dmm  = DMM.Agilent.DMM(conn)

    # Prints the identification stuff.
    idn = dmm.identify()
    print "Connected to", idn["oem"], idn["model"]

    count = [ 0 ]
    csv = open(time.strftime("%c") + ".log", "w")

    thread = DMM.Logging(1, lambda: grab_sample(dmm, csv, count))
    thread.start()
    raw_input("Press Enter to continue...\n")
    thread.stop()

    csv.close()
    conn.close()

