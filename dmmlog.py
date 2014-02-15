#!/usr/bin/python

import sys
import serial

class SerialConnection:
    def __init__(self, port = None):
        self.ser = None

        if port is not None:
            # The user specified a port, so let's open it.
            self.open(port)

    def open(self, port):
        """ Open a connection and check if it's open. """
        self.ser = serial.Serial(port, baudrate = 9600, timeout = 1)

        if not self.ser.isOpen():
            raise Exception("Could not open the port '" + port + "'")

    def close(self):
        """ Close the connection """
        self.ser.close()

    def send(self, command):
        """ Send a command to the device """
        self.ser.write(command + "\r\n")

    def read(self, bytes = None):
        """ Reads a line for the serial port if `bytes` is not specified """
        if bytes is not None:
            return self.ser.read(bytes)

        return self.ser.readline().replace("\r\n", "")

class DMM:
    def __init__(self, conn):
        self.conn = conn

    def _isFloat(self, n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    def identify(self):
        self.conn.send("*IDN?")
        response = self.conn.read()

        if response is not "":
            arr = response.split(",")
            idn = { "oem":     arr[0],
                    "model":   arr[1],
                    "serial":  arr[2],
                    "version": arr[3] }

            return idn
        else:
            self.conn.close()
            raise Exception("Could not identify device")

    def fetch_unit(self, primary = True):
        unit = ""
        if primary:
            self.conn.send("CONF?")
        else:
            self.conn.send("CONF? @2")

        response = self.conn.read()
        response_arr = response.replace("\"", "").replace(",", " ").split(" ")
        setting  = response_arr[0]
        dmmrange = response_arr[1]
        #resolution =  response_arr[2]

        if self._isFloat(dmmrange):
            dmmrange = float(dmmrange)

        if dmmrange is 0.001:
            unit = u"\u00B5"
        elif dmmrange <= 1:
            unit = "m"
        # TODO: kilo mega ranges!

        if setting == "VOLT:DBM":
            unit = "dBm"
        elif setting == "VOLT:DBV":
            unit = "dBV"
        elif (setting.find("VOLT") is 0) or (setting == "DIOD"):
            unit += "V"
        elif (setting == "RES") or (setting == "CONT"):
            unit += u"\u03A9"
        elif setting == "COND":
            unit += "S"
        elif setting == "FREQ":
            unit += "Hz"
        elif setting == "CAP":
            unit += "F"
        elif setting.find("TEMP") is 0:
            if dmmrange == "CEL":
                unit = u"\u00B0C"
            elif dmmrange == "FAR":
                unit = u"\u00B0F"
            else:
                raise Exception("Unknown temperature unit '" + dmmrange + "'")
        elif setting.find("CURR"):
            unit += "A"
        elif (setting == "HRAT") or (setting.find("CPER")):
            unit = "%"
        else:
            raise Exception("Unknown setting '" + response + "'")

        return unit

# Main program.
if __name__ == "__main__":
    port = sys.argv[1]
    conn = SerialConnection(port)
    dmm  = DMM(conn)

    # Prints the identification stuff.
    idn = dmm.identify()
    print "Connected to", idn["oem"], idn["model"]

    print dmm.fetch_unit()
    conn.send("FETC?")
    print conn.read()
    print dmm.fetch_unit(False)
    conn.send("FETC? @2")
    print conn.read()

    conn.close()
