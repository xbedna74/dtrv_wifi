#!/usr/bin/env python3

from thermostaticValve import ThermostaticValve

class ValveKeeper:
	"""
	A class used to represent publisher for ThermostaticValve objects.

	...

	Attributes
	----------
	valves : set
		set of ThermostaticValve that are subscribed
	"""
	def __init__(self):
		self.valves = set()

	def subscribe(self, s):
		"""
		Adds ThermostaticValve to set of valves.

		Parameters
		----------
		s : ThermostaticValve
			object that wants to subscribe to this publisher
		"""
		self.valves.add(s)

	def unsubscribe(self, s):
		"""
		Removes ThermostaticValve from set and deletes it from system.

		Parameters
		----------
		s : ThermostaticValve
			unsibscribing object
		"""
		for v in self.valves:
			if v.get_id() == s:
				self.valves.discard(v)
				ThermostaticValve.remove_valve(s)
				del v
				break

	def fire(self, message, message_type):
		"""
		Updates subscribers with new request.

		Parameters
		----------
		message : string
			request object that contains information like request argument or message body (json)
		message_type : string
			identifier of request type
		Returns
		-------
		tuple
			returns tuple containing message body and http response code
		"""
		delivered = False
		for v in self.valves:
			response, return_code = v.update(message, message_type)
			if return_code == 1 or return_code == 2:
				return response
			elif return_code == 3:
				delivered = True

		if delivered:
			return ('', 200)

		return ('', 404)

	def get_valves(self):
		"""
		Returns list with subcribed ThermostaticValve objects.

		Returns
		-------
		list
			returns list containing subcribed ThermostaticValve objects
		"""
		return self.valves

	def valve_exists(self, id):
		"""
		Checks if valve specified by identifier is subscibed.

		Parameters
		----------
		id : int
			identifier specifying ThermostaticValve
		Returns
		-------
		boolean
			returns True if valve is subscribed, False otherwise
		"""
		for v in self.valves:
			if int(v.get_id()) == int(id):
				return True

		return False