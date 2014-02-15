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
        self.ser.close()

    def send(self, command):
        """ Send a command to the device """
        self.ser.write(command + "\r\n")

    def read(self, bytes = None):
        """ Reads a line for the serial port if `bytes` is not specified """
        if bytes is not None:
            return self.ser.read(bytes)

        return self.ser.readline()

# Main program.
if __name__ == "__main__":
    port = sys.argv[1]
    conn = SerialConnection(port)

    conn.send("*IDN?")
    print conn.read()

    conn.close()
