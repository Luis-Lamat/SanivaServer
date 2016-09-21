import sys
from flask import jsonify

class Error:
	""" Error class
	
		Static class used throughout the application to display certain
		errors in a standirdized HTTP format.
	"""

	@staticmethod
	def gateway_timeout():
		message = {
			'status': 504,
			'message': 'Gateway timeout',
		}
		resp = jsonify(message)
		resp.status_code = 504
		return resp

	@staticmethod
	def bad_request():
		message = {
			'status': 400,
			'message': 'Bad request',
		}
		resp = jsonify(message)
		resp.status_code = 400
		return resp