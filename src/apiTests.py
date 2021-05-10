#!/usr/bin/env python3

import unittest
import requests
import json
import time

class TestApiMethods(unittest.TestCase):

	def test_valve_creation_deletion(self):
		addr = "http://192.168.1.210:60000/device/radiator-valve"
		req = requests.post(addr + "?id=42")
		self.assertEqual(req.status_code, 201)
		self.assertEqual(int(json.loads(req.text)), 42)
		req = requests.post(addr + "?id=42")
		self.assertEqual(req.status_code, 200)
		self.assertEqual(json.loads(req.text), '')

		req = requests.get(addr)
		self.assertEqual(req.status_code, 200)
		self.assertEqual(json.loads(req.text), ['42'])

		req = requests.get(addr + "?id=42")
		info = json.loads(req.text)
		self.assertEqual(req.status_code, 200)
		self.assertEqual(info["comfort"], 21.0)
		self.assertEqual(info["eco"], 17.0)
		self.assertEqual(info["current"], None)
		self.assertEqual(info["desired"], 21.0)
		self.assertEqual(info["mode"], 0)
		self.assertEqual(info["heating_mode"], 0)
		self.assertEqual(info["hysteresis_band"], 0.1)
		self.assertEqual(info["kp"], 30)
		self.assertEqual(info["ki"], 0.0)
		self.assertEqual(info["kd"], 0.0)

		req = requests.get(addr + "/temperature?id=42&day=0&hour=8")
		info = json.loads(req.text)
		self.assertEqual(req.status_code, 200)
		self.assertEqual(info["comfort"], 21.0)
		self.assertEqual(info["eco"], 17.0)
		self.assertEqual(info["current"], None)
		self.assertEqual(info["desired"], 21.0)
		self.assertEqual(info["hourly"], 21.0)

		req = requests.get(addr + "/mode/heating?id=42")
		info = json.loads(req.text)
		self.assertEqual(info["heating_mode"], 0)
		self.assertEqual(info["hysteresis_band"], 0.1)
		self.assertEqual(info["kp"], 30.0)
		self.assertEqual(info["ki"], 0.0)
		self.assertEqual(info["kd"], 0.0)

		req = requests.delete(addr + "?id=42")
		self.assertEqual(req.status_code, 200)
		req = requests.get(addr)
		self.assertEqual(req.status_code, 200)
		self.assertEqual(json.loads(req.text), [])

	def test_valve_updates(self):
		addr = "http://192.168.1.210:60000/device/radiator-valve"
		req = requests.post(addr + "?id=42")
		self.assertEqual(req.status_code, 201)
		self.assertEqual(int(json.loads(req.text)), 42)

		info = {'42':
		{"comfort": 22.0, "eco": 19.0, "mode": "eco", "hysteresis_band": 0.3, "kp": 3.0, "ki": 0.1, "kd": 0.2}}
		req = requests.put(addr, json=json.dumps(info))
		self.assertEqual(req.status_code, 200)

		req = requests.get(addr + "?id=42")
		info = json.loads(req.text)
		self.assertEqual(req.status_code, 200)
		self.assertEqual(info["comfort"], 22.0)
		self.assertEqual(info["eco"], 19.0)
		self.assertEqual(info["current"], None)
		self.assertEqual(info["desired"], 19.0)
		self.assertEqual(info["mode"], 1)
		self.assertEqual(info["heating_mode"], 0)
		self.assertEqual(info["hysteresis_band"], 0.3)
		self.assertEqual(info["kp"], 3.0)
		self.assertEqual(info["ki"], 0.1)
		self.assertEqual(info["kd"], 0.2)

		req = requests.put(addr + "/temperature/current?id=42", json=json.dumps('21.6'))
		self.assertEqual(req.status_code, 200)
		req = requests.get(addr + "/temperature/current?id=42")
		self.assertEqual(req.status_code, 200)
		self.assertEqual(json.loads(req.text), '21.6')
		req = requests.get(addr + "/temperature/currents?id=42")
		self.assertEqual(req.status_code, 200)
		time.sleep(2)
		req = requests.put(addr + "/temperature/current?id=42", json=json.dumps('21.7'))
		self.assertEqual(req.status_code, 200)
		req = requests.get(addr + "/temperature/current?id=42")
		self.assertEqual(req.status_code, 200)
		self.assertEqual(json.loads(req.text), '21.7')
		req = requests.get(addr + "/temperature/currents?id=42")
		self.assertEqual(req.status_code, 200)
		vals = json.loads(req.text).values()
		i = 0
		for v in vals:
			if i == 0:
				self.assertEqual(v, '21.6')
			else:
				self.assertEqual(v, '21.7')
			i += 1

		req = requests.put(addr + "/alias?id=42", json=json.dumps("room"))
		self.assertEqual(req.status_code, 200)
		req = requests.get(addr + "/alias?id=42")
		self.assertEqual(req.status_code, 200)
		self.assertEqual(json.loads(req.text), "room")


if __name__ == "__main__":
	unittest.main(verbosity=2)