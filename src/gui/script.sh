#!/bin/sh
apt-get update -y
apt-get install python3-pip -y
apt-get install python3-tk -y
pip3 install requests
pip3 install PySimpleGUI
python3 gui.py
