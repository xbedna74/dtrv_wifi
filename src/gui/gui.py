#!/usr/bin/env python3

import PySimpleGUI as sg

import requests

import sys
import socket
import json
import time

from utils import *

address = "http://"
port = "60000"

def is_ipv4(addr):
	"""
	Checks if given string is valid IPv4 address.

	Parameters
	----------
	addr : str
		string to check for IPv4 address
	Returns
	-------
	boolean
		return True if string is IPv4, otherwise False
	"""
	try:
		socket.inet_pton(socket.AF_INET, addr)
	except AttributeError:
		try:
			socket.inet_aton(addr)
		except socket.error:
			return False
		# to stop using short versions such as "127", which would be "127.0.0.0"
		return address.count('.') == 3
	except socket.error:
		return False

	return True

def get_valve_list(ids):
	"""
	Performs creation of valves list by identifiers to be shown in GUI.

	Parameters
	----------
	ids : list
		list with all identifiers of valves in system
	Returns
	-------
	list
		return list with full names of valves as are shown in gui (ID? <valve_id> (<alias>)
	"""
	valves_list = []
	for valve in ids:
		alias = requests.get(address + "/device/radiator-valve/alias?id=" + str(valve))
		if alias.status_code == 200:
			alias = json.loads(alias.text)
		else:
			alias = ''
		valves_list.append("ID: " + str(valve) + " (" + alias + ")")
	return valves_list


def get_id_from_text(w):
	"""
	Extracts identifier from selected valve in valves list.

	Parameters
	----------
	w : sg.Window
		PySimpleGUI Window instance of used window
	Returns
	-------
	int
		identifier of currently selected valve in GUI
	"""
	selected_id = w["valves"].get()[0].split(' ', 2)[1]
	return selected_id


def set_window_info(w, v, info):
	"""
	Sets certain parts of GUI to given values that correspond with selected valve.

	Parameters
	----------
	w : sg.Window
		PySimpleGUI Window instance of used window
	v : dict
		dictionary of value of all GUI parts
	"""
	if v == '':
		return
	if v["current"]:
		w["cur_tmp"].update(v["current"])
	w["des_tmp"].update(v["desired"])
	w["time_tmp"].update(v["hourly"])
	w["com_tmp"].update(v["comfort"])
	w["eco_tmp"].update(v["eco"])
	w["mode"].update(set_to_index=int(v["mode"]))
	w["heating_mode"].update(set_to_index=int(v["heating_mode"]))
	w["h_band"].update(v["hysteresis_band"])
	w["kp"].update(v["kp"])
	w["ki"].update(v["ki"])
	w["kd"].update(v["kd"])

	info = {"comfort": v["comfort"], "eco": v["eco"], "hourly": v["hourly"], "mode": v["mode"],
	"heating": v["heating_mode"], "band": v["hysteresis_band"], "kp": v["kp"], "ki": v["ki"], "kd": v["kd"]}

	return info


def get_change(change, v, info, ident):
	"""
	Performs check whether valve settings are valid values (if they are of correct type and in valid ranges).
	And puts them in to dictionary with other changes.

	Parameters
	----------
	change : dict
		dictionary with information of changes
	v : dict
		dictionary of value of all GUI parts
	info : dict
		dictionary with last valid values of valve settings
	ident : int
		identifier of valve
	Returns
	-------
	dict
		dictionary with with information about valve to be put to server
	"""

	if not is_float(v["com_tmp"]) or 16.0 > v["com_tmp"] > 26.0:
		v["com_tmp"] = info["comfort"]
	if not is_float(v["eco_tmp"]) or 16.0 > v["eco_tmp"] > 26.0:
		v["eco_tmp"] = info["eco"]
	if v["heating_mode"] not in ["Hysteresis", "PID"]:
		v["heating_mode"] = info["heating"]
	if not is_float(v["h_band"]) or 0.0 > v["h_band"] > 1.0:
		v["h_band"] = info["band"]
	if not isinstance(v["kp"], int) or 0 > v["kp"] > 100:
		v["kp"] = info["kp"]
	if not is_float(v["ki"]) or 0.0 > v["ki"] > 1.0:
		v["ki"] = info["ki"]
	if not is_float(v["kd"]) or 0.0 > v["kd"] > 1.0:
		v["kd"] = info["kd"]

	change[ident]["comfort"] = float(v["com_tmp"])
	change[ident]["eco"] = float(v["eco_tmp"])
	change[ident]["heating_mode"] = 0 if v["heating_mode"] == "Hysteresis" else 1
	change[ident]["hysteresis_band"] = float(v["h_band"])
	change[ident]["kp"] = v["kp"]
	change[ident]["ki"] = float(v["ki"])
	change[ident]["kd"] = float(v["kd"])

	return change


def draw_graph_lines(g, w):
	"""
	Performs drawing of graph according to temperature values that were measured by selected valve.

	Parameters
	----------
	g : sg.Graph

	w : sg.Window
		PySimpleGUI Window instance of used window
	"""
	g.erase()
	g.draw_line((0, 0), (0, 200), width=2)
	g.draw_line((0, 0), (40, 0), width=2)
	g.draw_text("°C", (-1, 195))
	g.draw_text("t", (37.5, -10))
	g.draw_text("25", (-1, 150))
	g.draw_text("20", (-1, 100))
	g.draw_text("15", (-1, 50))
	g.draw_text("10", (-1, 5))
	g.draw_line((0, 150), (40, 150), color="grey")
	g.draw_line((0, 100), (40, 100), color="grey")
	g.draw_line((0, 50), (40, 50), color="grey")

	req = requests.get(address + "/device/radiator-valve/temperature/currents?id=" + str(get_id_from_text(w)))

	if req.status_code != 200:
		return
	temperatures = json.loads(req.text)

	tmps = []
	times = []
	for key in temperatures:
		tmps.append(temperatures[key])
		times.append(int(key) - (int(key) % 60))

	if tmps == []:
		return

	end_time = int(times[len(times) - 1])
	start_time = end_time - (8 * 60 * 60)

	g.draw_text(time.strftime("%H:%M", time.localtime(end_time)), (37.5, -5))
	g.draw_text(time.strftime("%H:%M", time.localtime((start_time + end_time) / 2)), (20.5, -5))
	g.draw_text(time.strftime("%H:%M", time.localtime(start_time)), (0.5, -5))

	for i in range(len(tmps) - 2, -1, -1):
		if times[i] / 720 > start_time / 720 + 1:
			g.draw_line(((times[i + 1] - start_time) / 720 - 2, int(tmps[i + 1] * 10) - 100),
			            ((times[i] - start_time) / 720 - 2, int(tmps[i] * 10) - 100), color="red", width=2)


def run():
	"""
	Creates elements needed for GUI and runs loop for event handling.
	"""
	sg.theme('TealMono')

	# first column containing listbox with list of existing valves in system
	first_col = [[sg.Listbox(key="valves", enable_events=True, values=([]), size=(28, 30))]]
	# second column contains all elements that can be used to set desired control of temperature
	"""
	second column is divided into two tabs, one containing elements with settings and the other containing graph canvas
	on which is drawn graph of temperature movements of selected valve
	"""
	second_col = [[sg.Text("Current temperature: "), sg.Text(key="cur_tmp", text="---", size=(10, 0))],
	              [sg.Text("Desired temperature: "), sg.Text(key="des_tmp", text="---", size=(10, 0))],
	              [sg.HSeparator()],
	              [sg.Text("Comfort temperature: "),
	               sg.Spin(key="com_tmp", values=([x / 10.0 for x in range(160, 261, 1)]), initial_value='21.0',
	                       enable_events=True)],
	              [sg.HSeparator()],
	              [sg.Text("Eco temperature: "),
	               sg.Spin(key="eco_tmp", values=([x / 10.0 for x in range(160, 261, 1)]), initial_value='17.0',
	                       enable_events=True)],
	              [sg.HSeparator()],
	              [sg.Text("Day: "),
	               sg.Combo(values=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], default_value="Mon",
	                        enable_events=True, key="day_change", size=(5, 0)),
	               sg.Text("Hour: "),
	               sg.Combo(values=[i for i in range(0, 24)], default_value=0, enable_events=True, key="hour_change",
	                        size=(5, 0))],
	              [sg.Text("Select temperature: "),
	               sg.Spin(key="time_tmp", values=([x / 10.0 for x in range(160, 261)]), initial_value='17.0',
	                       enable_events=True)],
	              [sg.HSeparator()],
	              [sg.Text("Input alias:"), sg.Input(key="in_alias", size=(20, 0))],
	              [sg.Button(button_text="Set alias", key="set_alias")],
	              [sg.HSeparator()],
	              [sg.Text("Mode: "),
	               sg.Combo(values=["Comfort", "Eco", "Hourly", "Away"], default_value="Comfort", key="mode",
	                        enable_events=True, size=(13, 0))],
	              [sg.HSeparator()],
	              [sg.Text("Heating mode:"),
	               sg.Combo(values=["Hysteresis", "PID"], default_value="Hysteresis", enable_events=True,
	                        key="heating_mode"),
	               sg.Text("Hyst. band:"),
	               sg.Spin(key="h_band", values=([x / 10.0 for x in range(0, 10)]), enable_events=True),
	               sg.Text("Kp:"),
	               sg.Spin(key="kp", values=([x for x in range(0, 100)]), enable_events=True,
	                       initial_value='30'),
	               sg.Text("Ki:"),
	               sg.Spin(key="ki", values=([x / 10.0 for x in range(0, 10)]), enable_events=True,
	                       initial_value='0.0'),
	               sg.Text("Kd:"),
	               sg.Spin(key="kd", values=([x / 10.0 for x in range(0, 10)]), enable_events=True,
	                       initial_value='0.0')],
	              [sg.HSeparator()],
	              [sg.Button(button_text="Delete valve", key="delete_valve")],
	              [sg.Text(text="Time:"), sg.Text(key="time", text=time.strftime("%H:%M"))]]

	graph = sg.Graph((500, 360), (-2, -20), (41, 200), background_color="white", pad=(10, 10))

	tab1 = [[sg.Column(first_col), sg.VSeperator(),
	         sg.TabGroup([[sg.Tab("Settings", second_col, key="settings")],
	                      [sg.Tab("Graph", [[graph]], key="valve_graph")]], enable_events=True, key="valve_tab")]]

	layout = [[sg.TabGroup([[sg.Tab("Valves", tab1)]], tab_location="topleft")]]

	window = sg.Window(title='Smart thermostatic valves control', layout=layout, size=(850, 500))

	change_info = {}
	change = False
	time_interval = time.monotonic()
	valve_selected = None

	settings_info = {}

	# event handling loop
	while True:
		# reading event, values of elements (whenever event occurs, timeout is event)
		event, values = window.read(timeout=5000)

		# event for closing window (pressing x button on window)
		if event == sg.WIN_CLOSED:
			# if changes were made, send them to server before closing window
			if change and values["valves"]:
				change_info[get_id_from_text(window)] = {}
				change_info = get_change(change_info, values, settings_info, get_id_from_text(window))
				change_info = json.dumps(change_info)
				requests.put(address + "/device/radiator-valve", json=change_info)
			break  # closing window with break

		# checking if server is on and getting identifiers of valves in system
		try:
			valve_ids = requests.get(address + "/device/radiator-valve")
		except requests.exceptions.ConnectionError:
			print("Trying to connect")
			continue

		valve_ids = json.loads(valve_ids.text)

		# time interval when changes should be sent to server, or settings should be requested
		if time.monotonic() - time_interval > 10:
			if change and values["valves"]:
				print(values["com_tmp"])
				change_info[get_id_from_text(window)] = {}
				change_info = get_change(change_info, values, settings_info, get_id_from_text(window))
				change_info = json.dumps(change_info)
				requests.put(address + "/device/radiator-valve", json=change_info)
				change_info = {}

				change = False
			elif values["valves"]:
				if (values["day_change"] not in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] or
					values["hour_change"] not in [h for h in range(0, 24)]):
					values["day_change"] = "Mon"
					values["hour_change"] = 0
					window["day_change"].update("Mon")
					window["hour_change"].update(0)

				req = requests.get(
					address + "/device/radiator-valve?id=" + str(get_id_from_text(window)) + "&day=" +
					str(get_day_index(values["day_change"])) + "&hour=" + str(values["hour_change"]))
				if req.status_code == 200:
					valve_info = json.loads(req.text)
					settings_info = set_window_info(window, valve_info, settings_info)

			elif not values["valves"]:
				window["cur_tmp"].update("---")
				window["des_tmp"].update("---")

			time_interval = time.monotonic()

		# updating shown time
		window["time"].update(time.strftime("%H:%M"))

		# do if timeout occurred or there is difference between GUIs valves list, and servers valves list
		if event == "__TIMEOUT__" or valve_ids != [x.split(' ', 2)[1] for x in window["valves"].get_list_values()]:
			print("list are not the same")
			print(valve_ids)
			print(values["valves"])
			valves_list = get_valve_list(valve_ids)

			# setting selected valve to be the same as it was before changing the list
			if values["valves"]:
				old_id = values["valves"][0].split(' ', 2)[1]
				new_id = None
				for i in range(0, len(valves_list)):
					if old_id == valves_list[i].split(' ', 2)[1]:
						new_id = i
						break
				window["valves"].update(valves_list)
				window["valves"].update(set_to_index=new_id) if new_id is not None else None
			else:
				window["valves"].update(valves_list)

		# if no valve is selected from list and event is not selection of valve, then continue the loop
		if valve_selected is None and event != "valves":
			continue

		# if valve was selected
		if event == "valves":
			print("Event valves")
			if valve_selected is not None:
				# if valve was selected, and other one was just selected, PUT settings to the server
				if valve_selected not in change_info or not isinstance(change_info[valve_selected], dict):
					change_info[valve_selected] = {}
				change_info = get_change(change_info, values, settings_info, valve_selected)

				change_info = json.dumps(change_info)
				requests.put(address + "/device/radiator-valve", json=change_info)
				change_info = {}

			valve_selected = values["valves"][0].split(' ', 2)[1] if values["valves"] else None
			# get settings of newly set valve
			if valve_selected is not None:
				if (values["day_change"] not in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] or
					values["hour_change"] not in [h for h in range(0, 24)]):
					values["day_change"] = "Mon"
					values["hour_change"] = 0
					window["day_change"].update("Mon")
					window["hour_change"].update(0)

				req = requests.get(
					address + "/device/radiator-valve?id=" + str(get_id_from_text(window)) + "&day=" +
					str(get_day_index(values["day_change"])) + "&hour=" + str(values["hour_change"]))
				if req.status_code == 200:
					valve_info = json.loads(req.text)
					print(valve_info)
					settings_info = set_window_info(window, valve_info, settings_info)

				print(values["valve_tab"])
				if values["valve_tab"] == "valve_graph":
					draw_graph_lines(graph, window)
			else:
				continue

		# if tab with graph was selected, graph is drawn
		elif event == "valve_tab" and values["valve_tab"] == "valve_graph":
			draw_graph_lines(graph, window)

		# put information about selected time based temperature
		elif event == "time_tmp":
			requests.put(
				address + "/device/radiator-valve/temperature/hourly?id=" + str(get_id_from_text(window)) + "&day=" +
				str(get_day_index(values["day_change"])) + "&hour=" + str(values["hour_change"]),
				json=json.dumps(values["time_tmp"]))

		# get information about time based temperature on day or hour change in GUI
		elif event == "day_change" or event == "hour_change":
			if (values["day_change"] not in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] or
					values["hour_change"] not in [h for h in range(0, 24)]):
				values["day_change"] = "Mon"
				values["hour_change"] = 0
				window["day_change"].update("Mon")
				window["hour_change"].update(0)

			req = requests.get(
				address + "/device/radiator-valve/temperature/hourly?id=" + str(get_id_from_text(window)) + "&day=" +
				str(get_day_index(values["day_change"])) + "&hour=" + str(values["hour_change"]))

			if req.status_code == 200:
				hour_tmp = json.loads(req.text)
				window["time_tmp"].update(hour_tmp)

		# put alias if alias button was selected
		elif event == "set_alias":
			alias = values["in_alias"]
			window["in_alias"].update('')
			requests.put(address + "/device/radiator-valve/alias?id=" + str(get_id_from_text(window)),
			             json=json.dumps(alias))

		# put mode if mode was changed in GUI
		elif event == "mode":
			mode = -1
			if values["mode"] == "Comfort":
				mode = 0
			elif values["mode"] == "Eco":
				mode = 1
			elif values["mode"] == "Hourly":
				mode = 2
			if mode != -1:
				requests.put(address + "/device/radiator-valve/mode/temperature?id=" + str(get_id_from_text(window)),
				         json=json.dumps(mode))

		# if information that does not need to be conveyed right away changes, change is registered and after set time they are posted to server
		elif event in ["eco_tmp", "com_tmp", "heating_mode", "h_band", "kp", "ki", "kd"]:
			change = True

		# button for valve deletion pressed
		elif event == "delete_valve":
			requests.delete(address + "/device/radiator-valve?id=" + str(get_id_from_text(window)))


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Expected one argument. Given " + str(len(sys.argv) - 1) + ".")
		sys.exit(-1)

	addr = sys.argv[1]

	if is_ipv4(addr):
		address = address + addr + ":" + port
	else:
		print("Given argument is not IPv4 address.")
		sys.exit(-1)

	run()
