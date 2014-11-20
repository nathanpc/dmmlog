#!/usr/bin/python

import threading

class Logging(threading.Thread):
	def __init__(self, interval, log_function):
		"""Initializes the `Logging` class.

		Note:
			Do not include the `self` parameter in the ``Args`` section.

		Args:
			interval (int): Interval in seconds between each sample.
			log_function (function): A function that will be called every time the timer decides it is time to take a sample. You should use this function to log.
		"""
		threading.Thread.__init__(self)

		self.stopped = threading.Event()
		self.interval = interval
		self.log_function = log_function

	def run(self):
		""" What to do while logging. """
		while not self.stopped.wait(self.interval):
			self.log_function()

	def stop(self):
		""" Stops logging. """
		self.stopped.set()
