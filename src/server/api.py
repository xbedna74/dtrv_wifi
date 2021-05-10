#!/usr/bin/env python3

import flask
from flask import request

from server import *

app = flask.Flask(__name__)
server = Server()


@app.route("/device/radiator-valve", methods=["GET"])
def get_info():
	"""
	Handles request for valve info.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_info(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/temperature", methods=["GET"])
def get_temperature():
	"""
	Handles request for valve temperatures.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_temperature(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/temperature/current", methods=["GET"])
def get_current_temperature():
	"""
	Handles request for last temperatures posted.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_current_temperature(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/temperature/desired", methods=["GET"])
def get_desired_temperature():
	"""
	Handles request for valve desired temperature.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_desired_temperature(request)
	print(response[0])
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/temperature/eco", methods=["GET"])
def get_eco_temperature():
	"""
	Handles request for valve eco temperatures.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_eco_temperature(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/temperature/comfort", methods=["GET"])
def get_comfort_temperature():
	"""
	Handles request for valve comfort temperatures.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_comfort_temperature(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/temperature/hourly", methods=["GET"])
def get_hour_temperature():
	"""
	Handles request for valve time based temperatures.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_hour_temperature(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/mode/temperature", methods=["GET"])
def get_temperature_mode():
	"""
	Handles request for valve temperature mode (eco, comfort, time program...).

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_temperature_mode(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/mode/heating", methods=["GET"])
def get_heating_mode():
	"""
	Handles request for valve heating mode (hysteresis, PID).

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_heating_mode(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/temperature/currents", methods=["GET"])
def get_current_temperatures():
	"""
	Handles request for valve temperature measurements.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_current_temperatures(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve/alias", methods=["GET"])
def get_alias():
	"""
	Handles request for valve alias.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.get_alias(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve", methods=["POST"])
def post_new_valve():
	"""
	Handles request for valve creation in system.

	Returns
	-------
	str
		the response message for client in json
	int
		the HTTP response code
	"""
	response = server.post_new_valve(request)
	return flask.jsonify(response[0]), response[1]


@app.route("/device/radiator-valve", methods=["PUT"])
def put_info():
	"""
	Handles request for valves info update.

	Returns
	-------
	str
		empty string
	int
		the HTTP response code
	"""
	response = server.put_info(request)
	return response[0], response[1]


@app.route("/device/radiator-valve/temperature/current", methods=["PUT"])
def put_current_temperature():
	"""
	Handles request for valve temperature measurement update.

	Returns
	-------
	str
		empty string
	int
		the HTTP response code
	"""
	response = server.put_current_temperature(request)
	return response[0], response[1]


@app.route("/device/radiator-valve/temperature/eco", methods=["PUT"])
def put_eco_temperature():
	"""
	Handles request for valve eco temperature update.

	Returns
	-------
	str
		empty string
	int
		the HTTP response code
	"""
	response = server.put_eco_temperature(request)
	return response[0], response[1]


@app.route("/device/radiator-valve/temperature/comfort", methods=["PUT"])
def put_comfort_temperature():
	"""
	Handles request for valve comfort temperature update.

	Returns
	-------
	str
		empty string
	int
		the HTTP response code
	"""
	response = server.put_comfort_temperature(request)
	return response[0], response[1]


@app.route("/device/radiator-valve/temperature/hourly", methods=["PUT"])
def put_hour_temperature():
	"""
	Handles request for valve time based temperature update.

	Returns
	-------
	str
		empty string
	int
		the HTTP response code
	"""
	response = server.put_hour_temperature(request)
	return response[0], response[1]


@app.route("/device/radiator-valve/mode/temperature", methods=["PUT"])
def put_temperature_mode():
	"""
	Handles request for valve temperature mode update.

	Returns
	-------
	str
		empty string
	int
		the HTTP response code
	"""
	response = server.put_temperature_mode(request)
	return response[0], response[1]


@app.route("/device/radiator-valve/mode/heating", methods=["PUT"])
def put_heating_mode():
	"""
	Handles request for valve heating mode update.

	Returns
	-------
	str
		empty string
	int
		the HTTP response code
	"""
	response = server.put_heating_mode(request)
	return response[0], response[1]


@app.route("/device/radiator-valve/alias", methods=["PUT"])
def put_alias():
	"""
	Handles request for valve alias update.

	Returns
	-------
	str
		empty string
	int
		the HTTP response code
	"""
	response = server.put_alias(request)
	return response[0], response[1]


@app.route("/device/radiator-valve", methods=["DELETE"])
def delete_valve():
	"""
	Handles request for valve deletion in system.

	Returns
	-------
	str
		empty string
	int
		the HTTP response code
	"""
	response = server.delete_valve(request)
	return response[0], response[1]


app.run(host="0.0.0.0", port="60000")
