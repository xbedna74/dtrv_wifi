from valveKeeper import *
from thermostaticValve import *

class Server:
	"""
	A class used to represent server.

	...

	Attributes
	----------
	keeper : ValveKeeper
		publisher to which server sends updates
	"""
	def __init__(self):
		self.keeper = ValveKeeper()

	def get_info(self, args):
		"""
		Delegates valve information request to publisher, and addes request identifier,
		 or responses with valves identifier list.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		if "id" in args.args:
			return_values = self.keeper.fire(args, "GET_INFO")
			return return_values
		else:
			id_list = []
			for v in self.keeper.get_valves():
				id_list.append(v.get_id())
			return (id_list, 200)

	def get_temperature(self, args):
		"""
		Delegates temperatures request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_TMP")
		return return_values

	def get_current_temperature(self, args):
		"""
		Delegates current temperature request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_CURTMP")
		return return_values

	def get_desired_temperature(self, args):
		"""
		Delegates desired temperature request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_DESTMP")
		return return_values

	def get_eco_temperature(self, args):
		"""
		Delegates eco temperature request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_ECOTMP")
		return return_values

	def get_comfort_temperature(self, args):
		"""
		Delegates comfort temperature request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_COMTMP")
		return return_values

	def get_hour_temperature(self, args):
		"""
		Delegates time based temperature request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_TIMETMP")
		return return_values

	def get_temperature_mode(self, args):
		"""
		Delegates temperature mode request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_TMPMODE")
		return return_values

	def get_heating_mode(self, args):
		"""
		Delegates heating mode request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_HEATMODE")
		return return_values

	def get_current_temperatures(self, args):
		"""
		Delegates current temperatures request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_CURTMPS")
		return return_values

	def get_alias(self, args):
		"""
		Delegates alias request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "GET_ALIAS")
		return return_values

	def post_new_valve(self, args):
		"""
		Creates new ThermostaticValve and adds it to the system.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		if "id" in args.args:
			if not self.keeper.valve_exists(args.args["id"]):
				new_valve = ThermostaticValve(args.args["id"])
				self.keeper.subscribe(new_valve)
				return str(new_valve.get_id()), 201
			else:
				return '', 200
		else:
			return '', 204

	def put_info(self, args):
		"""
		Delegates valve information update request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "PUT_INFO")
		return return_values

	def put_current_temperature(self, args):
		"""
		Delegates current temperature update request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "PUT_CURTMP")
		return return_values

	def put_eco_temperature(self, args):
		"""
		Delegates eco temperature update request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "PUT_ECOTMP")
		return return_values

	def put_comfort_temperature(self, args):
		"""
		Delegates comfort temperature update request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "PUT_COMTMP")
		return return_values

	def put_hour_temperature(self, args):
		"""
		Delegates time based temperature update request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "PUT_TIMETMP")
		return return_values

	def put_temperature_mode(self, args):
		"""
		Delegates temperature mode update request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "PUT_TMPMODE")
		return return_values

	def put_heating_mode(self, args):
		"""
		Delegates heating mode update request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "PUT_HEATMODE")
		return return_values

	def put_alias(self, args):
		"""
		Delegates alias update request to publisher, and addes request identifier.

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		return_values = self.keeper.fire(args, "PUT_ALIAS")
		return return_values

	def delete_valve(self, args):
		"""
		Deletes specified valve from system..

		Parameters
		----------
		args : request
			request object with information about request
		Returns
		-------
		tuple
			tuple with message body and HTTP response code
		"""
		if "id" in args.args:
			self.keeper.unsubscribe(args.args["id"])
			return '', 200
		return '', 404