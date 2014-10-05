#!/usr/bin/python

class DMM:
    def __init__(self, conn):
        self.conn = conn

    def _isFloat(self, n):
        """ Check if `n` is a float """
        try:
            float(n)
            return True
        except ValueError:
            return False

    def identify(self):
		""" Identify the device """
		return None

    def fetch_unit(self, primary = True, include_range = False):
        """ Fetch the unit from the device """
        return None

    def fetch_value(self, primary = True):
        """ Fetch the value from the DMM. """
        return None

    def fetch(self, primary = True, range_value = False):
        """ Fetch the full reading (value and unit) from the DMM. """
        return None
