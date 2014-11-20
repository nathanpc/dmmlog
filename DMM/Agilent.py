#!/usr/bin/python

import dmm

class DMM(dmm.DMM):
    def identify(self):
        """Identify the device.
		
		Note:
			Do not include the `self` parameter in the ``Args`` section.

		Returns:
			A dictionary with at least two parameters: "oem" and "model".
		"""
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

    def fetch_unit(self, primary = True, include_range = False):
        """Fetch the unit from the device

		Note:
			Do not include the `self` parameter in the ``Args`` section.

		Args:
			primary (bool, optional): Are you fetching the primary reading?
			include_range (bool, optional): Include the range in the output. (Example: "mV")

		Returns:
			String with the unit and range if `include_range` is True.
		"""
        unit = ""
        if primary:
            self.conn.send("CONF?")
        else:
            self.conn.send("CONF? @2")

        # Grab the response and parse it.
        response = self.conn.read()
        response_arr = response.replace("\"", "").replace(",", " ").split(" ")
        setting  = response_arr[0]
        dmmrange = response_arr[1]

        if include_range:
            # Check if the range is a float.
            if self._isFloat(dmmrange):
                dmmrange = float(dmmrange)

                # Get the first part of the unit.
                if dmmrange == 0.001:
                    #unit = u"\u00B5"
                    unit = "u"
                elif dmmrange <= 1 < 10000:
                    unit = "m"
                elif dmmrange >= 10000:
                    unit = "k"

        # Get the second part of the unit
        if setting == "VOLT:DBM":
            # dBm
            unit = "dBm"
        elif setting == "VOLT:DBV":
            # dBV
            unit = "dBV"
        elif (setting.find("VOLT") == 0) or (setting == "DIOD"):
            # Voltage and diode.
            unit += "V"
        elif (setting == "RES") or (setting == "CONT"):
            # Resistance and continuity.
            unit += u"\u03A9"
        elif setting == "COND":
            # Conductivity
            unit += "S"
        elif setting == "FREQ":
            # Frequency
            unit += "Hz"
        elif setting == "CAP":
            # Capacitance
            unit += "F"
        elif setting.find("TEMP") == 0 or (setting.find("T1") == 0) or (setting.find("T2") == 0):
            # Temperature
            if dmmrange == "CEL":
                # Celcius
                unit = u"\u00B0C"
            elif dmmrange == "FAR":
                # Fahrenreit
                unit = u"\u00B0F"
            else:
                # Unknown
                raise Exception("Unknown temperature unit '" + dmmrange + "'")
        elif setting.find("CURR") == 0:
            # Currency
            unit += "A"
        elif (setting == "HRAT") or (setting.find("CPER") == 0):
            # Duty cycle and currency percentage.
            unit = "%"
        else:
            # Unknown
            raise Exception("Unknown setting '" + response + "'")

        return unit

    def fetch_value(self, primary = True):
        """Fetch the value from the DMM.

		Note:
			Do not include the `self` parameter in the ``Args`` section.

		Args:
			primary (bool, optional): Are you fetching the primary reading?

		Returns:
			String with the reading value from the DMM.
		"""
        if primary:
            self.conn.send("FETC?")
        else:
            self.conn.send("FETC? @2")

        reading = float(self.conn.read())
        return reading

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
        value = self.fetch_value(primary)
        unit  = self.fetch_unit(primary, range_value)

        if range_value:
            if unit[0] == "u":
                # Micro
                value *= 1000000
            elif unit[0] == "m":
                # Milli
                value *= 1000
            elif unit[0] == "k":
                # Kilo
                value /= 1000

                if value >= 1000:
                    # Mega
                    value /= 1000
                    unit = "M" + unit[1:]

        return str(value) + unit

