#!/usr/bin/env python3

import unittest
from thermostaticValve import ThermostaticValve
import time

class TestValveMethods(unittest.TestCase):

	def test_constructor(self):
		t = ThermostaticValve(1)
		self.assertEqual(t.get_id(), 1)
		self.assertEqual(t.get_eco_temperature(), 17.0)
		self.assertEqual(t.get_comfort_temperature(), 21.0)
		self.assertEqual(t.get_current_temperature(), None)
		self.assertEqual(t.get_current_temperatures(), ([], []))
		self.assertEqual(t.get_temperature_mode(), 0)
		self.assertEqual(t.get_heating_mode(), 0)
		self.assertEqual(t.get_alias(), '')
		self.assertEqual(t.get_hysteresis_band(), 0.1)
		self.assertEqual(t.get_pid_coeficients(), (30.0, 0.0, 0.0))
		self.assertEqual([t], ThermostaticValve.valves)

		ThermostaticValve.remove_valve(1)

	def test_setter_getter(self):
		t = ThermostaticValve(2)
		self.assertEqual(t.get_id(), 2)
		t.set_alias("alias")
		self.assertEqual(t.get_alias(), "alias")

		t.set_eco_temperature(20.0)
		self.assertEqual(t.get_eco_temperature(), 20.0)

		t.set_comfort_temperature(20.0)
		self.assertEqual(t.get_comfort_temperature(), 20.0)

		t.set_hourly_temperature(5, 10, 20.0)
		self.assertEqual(t.get_hourly_temperature(5, 10), 20.0)

		with self.assertRaises(IndexError):
			t.set_hourly_temperature(7, 10, 20.0)
		with self.assertRaises(IndexError):
			t.get_hourly_temperature(7, 10)
		with self.assertRaises(IndexError):
			t.set_hourly_temperature(0, 24, 20.0)
		with self.assertRaises(IndexError):
			t.get_hourly_temperature(0, 24)

		t.set_current_temperature(20.0)
		self.assertEqual(t.get_current_temperature(), 20.0)
		self.assertEqual(t.get_current_temperatures()[0], [20.0])
		self.assertEqual(int(t.get_current_temperatures()[1][0]), int(time.time()))

		t.set_comfort_temperature(25.0)
		t.set_temperature_mode(0)
		self.assertEqual(t.get_desired_temperature(), 25.0)
		self.assertEqual(t.get_temperature_mode(), 0)
		t.set_eco_temperature(18.0)
		t.set_temperature_mode(1)
		self.assertEqual(t.get_desired_temperature(), 18.0)
		self.assertEqual(t.get_temperature_mode(), 1)

		t.set_hysteresis_band(0.5)
		self.assertEqual(t.get_hysteresis_band(), 0.5)
		t.set_pid_coeficients(1.0, 1.1, 1.2)
		self.assertEqual(t.get_pid_coeficients(), (1.0, 1.1, 1.2))

		t.set_heating_mode(0)
		self.assertEqual(t.get_heating_mode(), 0)
		t.set_heating_mode(1)
		self.assertEqual(t.get_heating_mode(), 1)

		ThermostaticValve.remove_valve(2)

	def test_static_methods(self):
		t = ThermostaticValve(3)
		self.assertEqual(ThermostaticValve.get_valve(3), t)
		self.assertEqual(ThermostaticValve.get_ids(), [3])
		self.assertEqual(ThermostaticValve.valves, [t])
		ThermostaticValve.add_valve(t)
		self.assertEqual(ThermostaticValve.valves, [t, t])
		ThermostaticValve.valves.remove(t)
		self.assertEqual(ThermostaticValve.valves, [t])


if __name__ == "__main__":
	unittest.main(verbosity=2)