import sys

class Logger:
	""" Logger class
	
		Static class used throughout the application to display certain
		messages in a standirdized format.
	"""

	@staticmethod
	def log_time_diff(diff_in_seconds):
		print "=== [SERVER]: {}s since last request".format(diff_in_seconds)

		