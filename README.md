# dtrv_wifi
Digital TRV with WiFi communication
## Flask server
### Launching on Linux
First is needed update of programs.
`sudo apt-get update`
Next is needed installation of `pip` and `virtualenv`.
`sudo apt-get install python3-pip`
`sudo apt-get install python3-venv`
After that move to the directory with flask server and create virtual enviroment and activate it.
`python3 -m venv venv`
`source venv/bin/activate`
Then you have to install Flask to the virtual enviroment and launch the server.
`pip install Flask`
`python3 api.py`
Server can be shut down with keys `Ctrl+C` and virtual enviroment can be deactivated with `deactivate` command.
### Launching on Windows
First you need to install python3 and pip.
Installation guide for python3 is available here: https://phoenixnap.com/kb/how-to-install-python-3-windows.
Installation guide for pip is available here: //phoenixnap.com/kb/install-pip-windows.
Then installation of Flask is needed.
`pip install Flask`/`pip3 install Flask`
The you move to the directory with server and launch it.
`python3 api.py`
Server can be shut down with keys `Ctrl+C`.

## GUI
### Launching on Linux/Windows
First is needed update of programs.
`sudo apt-get update`
Next is needed installation of `pip` and library `tkinter`.
`sudo apt-get install python3-pip`
`sudo apt-get install python3-tk`
Next is needed installation of libraries `requests` and `PySimpleGUI`.
`pip install requests`/`pip3 install requests`
`pip install PySimpleGUI`/`pip3 install PySimpleGUI`
The you move to the directory with GUI and launch it.
`python3 gui.py <IP_address>`, where IP_address is needed argument with IP address of server.

### Controlling
The head can be set to three different modes. Comfort, eco or weekly mode, comfort and eco acquire only one desired temperature and can be used when needed to increase or decrease the temperature quickly for some time, weekly mode contains 24 values for 7 days a week, so you can set suitable temperatures for sleep, for the time when the house is occupied or when the user is regularly at work.

The head contains two control algorithms, hysteresis and PID.
The behavior of the hysteresis algorithm is set by means of a hysteresis band, which limits the desired temperature from both sides, heats until the upper limit is exceeded and does not heat until the lower limit is exceeded, it is an algorithm that oscillates around the setpoint with the hysteresis band deviation, the larger the band value the larger the deviation, but the lower the number of valve adjustments and vice versa with a smaller band value.
The PID algorithm depends on three coefficients Kp, Ki and Kd. The equation of the algorithm is "P = Kp \ * e + ∑ (Ki \ * e_n \ * 3) + Kd \ * (t_ (n-1) -t_n) / 3", where P is the position of the valve, which takes values from from 0 to 30, e is the difference between the setpoint and the actual value, t is the measured temperature. These coefficients can be set so that the heating corresponds to your needs and spaces.

## Uploading code to valve head
It is necessary to have Arduino IDE installed (here https://www.arduino.cc/en/software).
After starting the Arduino environment, open File -> Preferences.
In the "Additional Board Manager URLs" window, enter this link https://arduino.esp8266.com/stable/package_esp8266com_index.json.
Then go to "Boards Manager" via Tools -> Board -> Boards Manager. Enter esp8266 here and install esp8266 from ESP8266 Community.
Then go to Tools -> Library manager and enter "DHT sensor library" and install it from the creator of Adafruit. And also install the "AdruinoJson" library from the creator Benoit Blanchon.
Then select "NodeMCU 1.0 (ESP-12E Module)" in Tools -> Board -> ESP8266 Boards.
Enter additional settings in Tools as follows:
`Builtint Led: "2"`
`Upload Speed: "115200"`
`CPU Frequency: "80 MHz"`
`Flash Size: "4MB (FS:2MB OTA:~1019KB)"`
`Debug port: "Disabled"`
`Debug level: "None"`
`IwIP Variant. "v2 Lower Memory"`
`VTables: "Flash"`
`Exceptions: "Legacy (new can return nullptr)"`
`Erase Flash: "All Flash Contents"`.

After opening the code, you need to change the SSID and password of the WiFi network to connect. The SSID must be entered in the `ssid` variable and it is the name of the network that is displayed on other devices (phone, computer). Enter the WiFi password in the `password` variable. In the `target_ip` variable, enter the IP address where the server is running.
Then it is possible to upload the code to the connected NodeMCU with the arrow in the top bar. It may still be necessary to install the C2102 driver for communication with the module, which can be downloaded from https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers, this is the first link `CP210x Universal Windows Driver`.
## Installation of valve head
Installation guide for valve head is available in video here: https://www.youtube.com/watch?v=3DRpOSUlF0c.
