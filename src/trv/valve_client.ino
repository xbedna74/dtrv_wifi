/**
	Name: valve_client
	Purpose: Controls position of valve based on desired temperature, and communicates with server.
	@author Radim Bednarik
*/

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <EEPROM.h>
#include "DHT.h"

#define OPENING D1 //INPUT1
#define CLOSING D2 //INPUT2

#define DHTPIN D7

#define FULL_MOTION 30000 //time that it takes to fully open/close radiator valve

#define MEASURE_TIME 180000 //time in miliseconds in between measurements

const char* ssid = "your_ssid"; //SSID of WiFi
const char* password = "your_password"; //password of WiFi

String target_ip = "your_target_ip"; //ip address of server

String address = "http://" + target_ip + ":60000"; //address of the server

DHT dht(DHTPIN, DHT22);

byte mac[6];
unsigned int id;

bool posted = false;
bool start = true;

float desired_tmp = 21.0;
float tmp_array[3];
int tmp_index = 0;
float last_tmp = 0;
float tmp;
float hum;

int pos = 0;

bool open_window = false;
unsigned int open_window_timer;

float hysteresis_band = 0.1;
bool hysteresis_falling = true;

float kp = 30.0;
float ki = 0.0;
float kd = 0.0;

int control_mode = 0; // 0 for hysteresis and 1 for pid

unsigned long _time = 0;
unsigned int _count = 0;

int count = 0;

void setup () {
	Serial.begin(9600);

	pinMode(DHTPIN, INPUT); //initializing DHT
	dht.begin();

	pinMode(OPENING, OUTPUT); //initializing pins for motor
	pinMode(CLOSING, OUTPUT);
	digitalWrite(OPENING, HIGH);
	digitalWrite(CLOSING, HIGH);
  

	WiFi.macAddress(mac); //getting mac of esp8266 for identifier
	id = (mac[3] << 16) + (mac[4] << 8) + mac[5];

	WiFi.begin(ssid, password);

	Serial.print("Connecting");
	while (WiFi.status() != WL_CONNECTED) { //loop for wifi connecting
		delay(1000);
		Serial.print(".");
	}
	Serial.println("CONNECTED!");
	
	HTTPClient http;
	http.begin(address + "/device/radiator-valve?id=" + String(id)); //setting http target

	int err_count = 0;
	while (1) { //trying to POST valve to server
		int httpCode = http.POST(" ");
		if (httpCode == 200 || httpCode == 201) {
			posted = true;
			break;
		}
		else if (httpCode < 0) {
			break;
		}
		else {
			delay(50);
			err_count = err_count + 1;
			Serial.println("Not posted correctly " + String(err_count));
			if (err_count > 10)
				break;
		}
	}

	//reading from EEPROM, whether position of valve is already set
	EEPROM.begin(128);
	byte b1 = EEPROM.read(99);
	byte b2 = EEPROM.read(100);
	byte b3 = EEPROM.read(101);
	EEPROM.end();
	int v1 = b1;
	int v2 = b2;
	int v3 = b3;
	if (v1 == 111 && v3 == 111) {
		pos = v3;
		if (pos == 30) //if position is 30, then temperature is rising, therefor hysteresis_falling must be false
			hysteresis_falling = false;
		else //otherwise change position to 0
			change_position(0);
	}
	else {//valve should be mounted when position is 30 (fully opened), so after mounting to the valve, change position to 0
		digitalWrite(OPENING, LOW);
		digitalWrite(CLOSING, HIGH);
		delay(FULL_MOTION + 1000);
		digitalWrite(OPENING, HIGH);
		digitalWrite(CLOSING, HIGH);
	}
	Serial.println("ID: " + String(id));
}

void loop() {
	//every 3 minute the value from sensor is read and valve is controlled
	if (start || millis() - _time >= MEASURE_TIME * _count) {

		if (!start)
			last_tmp = tmp;

		tmp = dht.readTemperature();
		Serial.println(String(tmp));

		if (tmp_index != 3)
			tmp_array[tmp_index++] = tmp;
		else {
			for (int i = 0; i < 3; i++) {
				if (i != 2)
					tmp_array[i] = tmp_array[i + 1];
				else
					tmp_array[i] = tmp;
			}
		}

		//every 12 minutes data are sent to the server
		if (start || millis() - _time >= MEASURE_TIME*4) {
			start = false;
			if (posted) {
				// putting current temperature
				StaticJsonDocument<10> put_doc;
				HTTPClient putTmp;
				String put_address = String(address + "/device/radiator-valve/temperature/current?id=") + String(id);
				putTmp.begin(put_address);
				int httpCode;
				JsonVariant put_var = put_doc.to<JsonVariant>();
				put_var.set(String(tmp));
				Serial.println("Temperature: " + String(tmp));
				String json;
				serializeJson(put_doc, json);
				putTmp.addHeader("Content-Type", "application/json");
				if ((httpCode = putTmp.PUT(json)) < 0) {
					Serial.println("Put error occured: " + httpCode);
				}
				putTmp.end();

				//getting value of desired temperature
				StaticJsonDocument<10> get_des_doc;
				HTTPClient getDesired;
				String get_des_address = String(address + "/device/radiator-valve/temperature/desired?id=") + String(id);
				getDesired.begin(get_des_address);
				if ((httpCode = getDesired.GET()) < 0) {
					Serial.println("Get desired error occured: " + httpCode);
				}
				else if (httpCode == 200) {
					Serial.print("Desired value: ");
					String jsond = getDesired.getString();
					deserializeJson(get_des_doc, jsond);
					JsonVariant des_var = get_des_doc.as<JsonVariant>();
					float des_val = des_var.as<float>();
					desired_tmp = des_val;
					Serial.println(des_val);
				}
				getDesired.end();

				//getting heating algorithm information
				StaticJsonDocument<JSON_OBJECT_SIZE(50)> get_heat_doc;
				HTTPClient getHeating;
				String get_heat_address = String(address + "/device/radiator-valve/mode/heating?id=") + String(id);
				getHeating.begin(get_heat_address);
				if ((httpCode = getHeating.GET()) < 0) {
					Serial.println("Get heating error occured: " + httpCode);
				}
				else if (httpCode == 200) {
					Serial.print("Heating value: ");
					String jsonh = getHeating.getString();
					deserializeJson(get_heat_doc, jsonh);
					JsonObject obj = get_heat_doc.as<JsonObject>();
					int last_c_mode = control_mode;
					control_mode = obj["heating_mode"];
					hysteresis_band = obj["hysteresis_band"];
					kp = obj["kp"];
					ki = obj["ki"];
					kd = obj["kd"];
					Serial.println("Heating mode:" + String(control_mode) + " Hysteresis band:" + String(hysteresis_band));
					Serial.println("Kp:" + String(kp) + " Ki:" + String(ki) + " Kd:" + String(kd));
					if (last_c_mode == 1 && control_mode == 0) {
						change_position(0);
						hysteresis_falling = true;
					}
				}
				getHeating.end();
			}
			else { //if valve is not posted, it tries every 10 minutes
				HTTPClient http;
				http.begin(address + "/device/radiator-valve?id=" + String(id));
				int httpCode = http.POST(" ");
				if (httpCode == 200 || httpCode == 201)
					posted = true;
			}

			_count = 0;
			_time = millis();
		}
		_count++;
		control_valve();
		Serial.println("Position: " + String(pos));
	}
}

/**
	Controls the position of valve.
*/
void control_valve() {
	int _position;

	//if open window was detected in past and is still set to true
	if (open_window) {
		if (millis() - open_window_timer > MEASURE_TIME*2)
			open_window = false;
		else
			return;
	}

	//open window detection, done by comparing temperatures with 6 minute interval
	if (tmp_index == 3 && (tmp_array[0] - tmp > 1.0)) {
		_position = 0;
		open_window = true;
		open_window_timer = millis();
	}
	else {
		//controlling valve according to set algorithm
		if (control_mode == 0)
			_position = hysteresis_control();
		else
			_position = pid_control();
	}

	if(pos == _position) {
		return;
	}

	//writing to EEPROM newly calculated position of valve
	EEPROM.begin(128);
	EEPROM.write(99, 111);
	EEPROM.write(101, 111);
	EEPROM.write(100, _position);
	change_position(_position);
	pos = _position;
	EEPROM.commit();
	EEPROM.end();
}

/**
	Calculates if position of valve should change with hysteresis alghoritm.
	@return the new position of valve.
*/
int hysteresis_control() {
	if(tmp >= desired_tmp + hysteresis_band && !hysteresis_falling) {
		hysteresis_falling = true;
		return 0;
	}
	else if(tmp <= desired_tmp - hysteresis_band && hysteresis_falling) {
		hysteresis_falling = false;
		return 30;
	}
	return pos;
}

/**
	Calculates if position of valve should change with PID controller alghoritm.
	@return the new position of valve
*/
int pid_control()
{
	static float i;

	float error = tmp - desired_tmp;
	float p = kp * error;
	i += ki * error * (MEASURE_TIME / 60000);
	float d = kd * ((last_tmp == 0) ? 0 : tmp - last_tmp) / (MEASURE_TIME / 60000);

	float output = p + i + d;
	int rounded_output;
	if (output > 30)
		rounded_output = 30;
	else if (output < 0)
		rounded_output = 0;
	else
		rounded_output = output + 0.5;


	return rounded_output;
}

/**
	Performs the change of motor position to adjust the valve.
	@param des_pos newly desired position of valve
*/
void change_position(int des_pos) {
	int diff = pos - des_pos;
	int motion_time = abs(FULL_MOTION / 30 * diff);
	if (diff > 0) {
		digitalWrite(CLOSING, HIGH);
		digitalWrite(OPENING, LOW);
		delay(motion_time);
		digitalWrite(CLOSING, HIGH);
		digitalWrite(OPENING, HIGH);
	}
	else if (diff < 0) {
		digitalWrite(OPENING, HIGH);
		digitalWrite(CLOSING, LOW);
		delay(motion_time);
		digitalWrite(OPENING, HIGH);
		digitalWrite(CLOSING, HIGH);
	}
}