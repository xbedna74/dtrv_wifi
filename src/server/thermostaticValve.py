#!/usr/bin/env python3

import time
import json
from utils import get_day_index, get_mode_index


class ThermostaticValve:
	"""
	A class used to represent thermostatic valve.

	...

	Attributes
	----------
	ids : list
		identifiers of all valves in system
	valves : list
		all instances of valves in system

	id : int
		unique identifier for valve in system
	eco : float
		temperature for eco mode
	comfort : float
		temperature for comfort mode
	week_prg : nested list
		temperature for time based mode
	current_temperature : float
		last measured temperature
	temperatures : list
		last 48 measured temperatures
	temperatures_time : list
		times of temperature measurements
	temperatures_index : int
		index of how many measured temperatures are stored (up to 40)
	"""

	ids = []
	valves = []

	#constructor
	def __init__(self, id):
		"""
		Parameters
		-------
		id : int
			unique identifier of valve
		"""

		self.id = id
		print("New valve created: " + str(self.id))

		self.eco = 17.0
		self.comfort = 21.0

		self.week_prg = [None] * 7
		for i in range(7):
			self.week_prg[i] = [None] * 24
			for j in range(24):
				self.week_prg[i][j] = 21.0 if 5 < j < 22 else 17.0

		self.current_temperature = None
		self.temperatures = [None] * 40 #list of temperature
		self.temperatures_time = [None] * 40
		self.temperatures_index = 0

		self.mode = 0
		self.heating_mode = 0 #0 for hyst, 1 for pid

		self.h_band = 0.1
		self.kp = 30.0
		self.ki = 0.0
		self.kd = 0.0

		self.alias = ''

		self.count = 0

		ThermostaticValve.valves.append(self)
		ThermostaticValve.ids.append(self.id)

	#returns ids of all existing valves
	@staticmethod
	def get_ids():
		"""
		Returns all identifiers of valves in system

		Returns
		-------
		list
			valves identifiers
		"""
		return ThermostaticValve.ids

	@staticmethod
	def add_valve(valve):
		"""
		Appends valve instance to list of valve instances.

		Parameters
		----------
		valve : ThermostaticValve
			valve to be appended
		"""
		ThermostaticValve.valves.append(valve)


	#returns valve id
	def get_id(self):
		"""
		Returns selected valves identifier.

		Returns
		-------
		int
			valves identifier
		"""
		return self.id


	def set_alias(self, alias):
		"""
		Sets selected valves alias.

		Parameters
		----------
		alias : str
			alias to be set
		"""
		self.alias = alias

	def get_alias(self):
		"""
		Returns selected valves alias.

		Returns
		-------
		str
			valves alias
		"""
		return self.alias



	def get_eco_temperature(self):
		"""
		Returns selected valves eco temperature.

		Returns
		-------
		float
			valves eco temperature
		"""
		return self.eco

	def set_eco_temperature(self, tmp):
		"""
		Sets selected valves eco temperature.

		Parameters
		----------
		tmp : float
			eco temperature to be set
		"""
		self.eco = tmp


	def get_comfort_temperature(self):
		"""
		Returns selected valves comfort temperature.

		Returns
		-------
		float
			valves comfort temperature
		"""
		return self.comfort

	def set_comfort_temperature(self, tmp):
		"""
		Sets selected valves comfort temperature.

		Parameters
		----------
		tmp : float
			comfort temperature to be set
		"""
		self.comfort = tmp


	#returns week program temperature at given time
	def get_hourly_temperature(self, day, hour):
		"""
		Returns selected valves time based temperature.

		Parameters
		----------
		day : int
			day of requested temperature
		hour : int
			hour of requested temperature

		Returns
		-------
		float
			valves time based temperature
		"""
		return self.week_prg[day][hour]

	#sets week program of valve
	def set_hourly_temperature(self, day, hour, tmp):
		self.week_prg[day][hour] = tmp


	#sets current temperature and saves it to list for future use
	def set_current_temperature(self, tmp):
		"""
		Sets selected valves current temperature and current time.

		Parameters
		----------
		tmp : float
			current temperature to be set
		"""
		self.current_temperature = tmp
		if self.temperatures_index == 40:
			for i in range(0, len(self.temperatures)):
				if i == 39:
					self.temperatures[i] = tmp
					self.temperatures_time[i] = time.time()
					break
				else:
					self.temperatures[i] = self.temperatures[i + 1]
					self.temperatures_time[i] = self.temperatures_time[i + 1]
		else:
			self.temperatures[self.temperatures_index] = tmp
			self.temperatures_time[self.temperatures_index] = time.time()
			self.temperatures_index += 1

	#returns current temperature
	def get_current_temperature(self):
		"""
		Returns selected valves current temperature.

		Returns
		-------
		float
			valves current temperature
		"""
		return self.current_temperature

	def get_current_temperatures(self):
		"""
		Returns selected valves current temperatures.

		Returns
		-------
		list
			valves current temperatures
		"""
		return self.temperatures[:self.temperatures_index], self.temperatures_time[:self.temperatures_index]

	#returns temperature according to selected mode
	def get_desired_temperature(self):
		"""
		Returns selected valves desired temperature according to temperature mode.

		Returns
		-------
		float
			valves desired temperature
		"""
		if self.mode == 0:
			return self.get_comfort_temperature()
		elif self.mode == 1:
			return self.get_eco_temperature()
		elif self.mode == 2:
			return self.get_hourly_temperature(get_day_index(time.strftime("%a")), int(time.strftime("%H")))


	def get_temperature_mode(self):
		"""
		Returns selected valves temperature mode.

		Returns
		-------
		int
			valves temperature mode
		"""
		return self.mode

	def set_temperature_mode(self, mode):
		"""
		Sets selected valves temperature mode.

		Parameters
		----------
		tmp : int
			temperature mode to be set
		"""
		self.mode = mode

	def get_heating_mode(self):
		"""
		Returns selected valves heating mode.

		Returns
		-------
		int
			valves heating mode
		"""
		return self.heating_mode

	def set_heating_mode(self, mode):
		"""
		Sets selected valves heating mode.

		Parameters
		----------
		tmp : int
			heating mode to be set
		"""
		self.heating_mode = mode

	def get_hysteresis_band(self):
		"""
		Returns selected valves hysteresis band.

		Returns
		-------
		float
			valves hysteresis band
		"""
		return self.h_band

	def set_hysteresis_band(self, band):
		"""
		Sets selected valves hysteresis band.

		Parameters
		----------
		band : float
			hysteresis band to be set
		"""
		self.h_band = band

	def get_pid_coeficients(self):
		"""
		Returns selected valves PID coeficients.

		Returns
		-------
		floats
			valves PID coeficients
		"""
		return self.kp, self.ki, self.kd

	def set_pid_coeficients(self, kp, ki, kd):
		"""
		Sets selected valves PID coeficients.

		Parameters
		----------
		kp : float
			proportional coeficient to be set
		ki : float
			integral coeficient to be set
		kd : float
			derivative coefient to be set
		"""
		self.kp = kp
		self.ki = ki
		self.kd = kd

	@staticmethod
	def get_valve(identifier):
		"""
		Returns valve according to identifier.

		Parameters
		----------
		identifier : int
			valves identifier

		Returns
		-------
		ThermostaticValve
			valve with matching identifier as was given
		"""
		if (isinstance(identifier, str) and identifier.isdigit()) or isinstance(identifier, int):
			for valve in ThermostaticValve.valves:
				if int(identifier) == valve.get_id():
					return valve

		return None

	#deletes valve from system
	@staticmethod
	def remove_valve(identifier):
		"""
		Removes specified valve by identifier.

		Parameters
		----------
		identifier : int
			identifier of valve to be deleted
		Returns
		-------
		boolean
			True if valve was succesfully removed, False otherwise
		"""
		del_valve = ThermostaticValve.get_valve(identifier)

		if del_valve is not None:
			ThermostaticValve.valves.remove(del_valve)
			ThermostaticValve.ids.remove(int(identifier))
			return True
		else:
			return False

	def update(self, message, message_type):
		"""
		Performs request specified by message_type.

		Parameters
		----------
		message : request
			request object that contains information like request argument or message body (json)
		message_type : string
			identifier of request type
		Returns
		-------
		tuple
			returns tuple containing message body and http response code
		int
			returns code that specifies if request was performed succesfully and what should caller do next
		"""
		args = message.args
		_json = message.json
		if _json is None and message_type[:3] == "PUT":
			return ('', 404), -1

		if "id" in args and int(args["id"]) != int(self.get_id()):
			return (), -1

		if message_type == "GET_INFO" and "id" in args:
			kp, ki, kd = self.get_pid_coeficients()
			info = {
				"comfort": self.get_comfort_temperature(),
				"eco": self.get_eco_temperature(),
				"current": self.get_current_temperature(),
				"desired": self.get_desired_temperature(),
				"mode": self.get_temperature_mode(),
				"heating_mode": self.get_heating_mode(),
				"hysteresis_band": self.get_hysteresis_band(),
				"kp": kp,
				"ki": ki,
				"kd": kd
			}
			if "day" in args and "hour" in args:
				info["hourly"] = self.get_hourly_temperature(int(args["day"]), int(args["hour"]))
			return (info, 200), 1

		elif message_type == "GET_TMP" and "id" in args:
			temperatures = {
				"comfort": self.get_comfort_temperature(),
				"eco": self.get_eco_temperature(),
				"current": self.get_current_temperature(),
				"desired": self.get_desired_temperature(),
			}
			if "day" in args and "hour" in args:
				temperatures["hourly"] = self.get_hourly_temperature(int(args["day"]), int(args["hour"]))
			return (temperatures, 200), 1

		elif message_type == "GET_CURTMP" and "id" in args:
			cur_tmp = self.get_current_temperature()
			return (str(cur_tmp), 200), 1

		elif message_type == "GET_DESTMP" and "id" in args:
			des_tmp = self.get_desired_temperature()
			return (str(des_tmp), 200), 1

		elif message_type == "GET_ECOTMP" and "id" in args:
			des_tmp = self.get_eco_temperature()
			return (str(des_tmp), 200), 1

		elif message_type == "GET_COMTMP" and "id" in args:
			des_tmp = self.get_comfort_temperature()
			return (str(des_tmp), 200), 1

		elif message_type == "GET_TIMETMP" and "id" in args:
			time_tmp = self.get_hourly_temperature(int(args["day"]), int(args["hour"]))
			return (str(time_tmp), 200), 1

		elif message_type == "GET_TMPMODE" and "id" in args:
			mode = self.get_temperature_mode()
			return (str(mode), 200), 1

		elif message_type == "GET_HEATMODE" and "id" in args:
			alg = self.get_heating_mode()
			hyst = self.get_hysteresis_band()
			coeficients = self.get_pid_coeficients()
			h_dict = {"heating_mode": alg, "hysteresis_band": hyst,
				"kp": coeficients[0], "ki": coeficients[1], "kd": coeficients[2]}
			print(h_dict)
			return (h_dict, 200), 1

		elif message_type == "GET_ALIAS" and "id" in args:
			alias = self.get_alias()
			return (alias, 200), 1

		elif message_type == "GET_CURTMPS" and "id" in args:
			tmps, times = self.get_current_temperatures()
			d = {}
			for x, y in zip(tmps, times):
				d[str(int(y))] = x
			return (d, 200), 1

		elif message_type == "PUT_INFO":
			valve1 = json.loads(_json)
			if str(self.get_id()) in valve1:
				valve1 = valve1[str(self.get_id())]
			else:
				return ('', 404), -1

			if "comfort" in valve1:
				self.set_comfort_temperature(valve1["comfort"])
			if "eco" in valve1:
				self.set_eco_temperature(valve1["eco"])
			if "mode" in valve1:
				mode = get_mode_index(valve1["mode"])
				self.set_temperature_mode(mode)
			if "heating_mode" in valve1:
				self.set_heating_mode(valve1["heating_mode"])
			if "hysteresis_band" in valve1:
				self.set_hysteresis_band(valve1["hysteresis_band"])
			if "kp" in valve1 and "ki" in valve1 and "kd" in valve1:
				self.set_pid_coeficients(valve1["kp"], valve1["ki"], valve1["kd"])

			return (' ', 200), 3

		elif message_type == "PUT_CURTMP" and "id" in args:
			_json = json.loads(_json)
			self.set_current_temperature(_json)
			return (' ', 200), 2

		elif message_type == "PUT_ECOTMP" and "id" in args:
			_json = json.loads(_json)
			self.set_eco_temperature(_json)
			return (' ', 200), 2

		elif message_type == "PUT_COMTMP" and "id" in args:
			_json = json.loads(_json)
			self.set_comfort_temperature(_json)
			return (' ', 200), 2

		elif message_type == "PUT_TIMETMP" and "id" in args:
			_json = json.loads(_json)
			self.set_hourly_temperature(int(args["day"]), int(args["hour"]), float(_json))
			return (' ', 200), 2

		elif message_type == "PUT_TMPMODE" and "id" in args:
			_json = json.loads(_json)
			self.set_temperature_mode(int(_json))
			return (' ', 200), 2

		elif message_type == "PUT_HEATMODE" and "id" in args:
			_json = json.loads(_json)
			self.set_heating_mode(int(_json))
			return (' ', 200), 2

		elif message_type == "PUT_ALIAS" and "id" in args:
			_json = json.loads(_json)
			self.set_alias(_json)
			return (' ', 200), 2