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
		"""Identify the device.
		
		Note:
			Do not include the `self` parameter in the ``Args`` section.

		Returns:
			A dictionary with at least two parameters: "oem" and "model".
		"""
		return None

    def fetch(self, primary = True, range_value = False):
        """Fetch the full reading (value and unit) from the DMM.

		Note:
			Do not include the `self` parameter in the ``Args`` section.

		Args:
			primary (bool, optional): Are you fetching the primary reading?
			range_value (bool, optional): Include the range in the output. (Example: "123.4mV")

		Returns:
			String with the reading and range if `range_value` is True.
		"""
        return None

