#!/usr/bin/env python3

#returns True if value is float, otherwise returns False
def is_float(value):
	try:
		float(value)
		return True
	except ValueError:
		return False


#returns index of day of the week
def get_day_index(day):
	"""
	Performs change of the short day name to its index.

	Parameters
	----------
	day : string
		short name of the day of the week
	Returns
	-------
	int
		returns index of the day of the week starting with monday
	"""
	return {
			'mon': 0,
			'tue': 1,
			'wed': 2,
			'thu': 3,
			'fri': 4,
			'sat': 5,
			'sun': 6,
		}[day.lower()]

def get_mode_index(mode):
	"""
	Performs change of the temperature name to its index.

	Parameters
	----------
	mode : string
		name of the mode of the week
	Returns
	-------
	int
		returns index of the mode
	"""
	return {
			'comfort': 0,
			'eco': 1,
			'hourly': 2,
		}[mode.lower()]