#!/usr/bin/python
#
# Module used to interface with the hardware through a serial port.
#
# This code is distributed under the GNU GPL v3
# Copyright (C) 2015 - Electric Ant <electrican@anche.no>
#

import serial	# requires python-serial
import os
import re
import thread

#
# Global variables
#
BAUD_RATE = 9600
pending = 0
serPort = 0

# Scan all serial ports searching for the faberdanaio hardware
# when it receives a v it will answer with its version in the form vX.X
# This function returns the serial port if something is found, 0 otherwise.
def autoscan():
	ser = 0
	files = os.listdir("/dev/")
	for filename in files:
		matched = re.search('tty.+', filename)
		if (matched):
			port = "/dev/" + matched.group(0)
			print("Opening: %s" % port)
			rec = ""
			try:
				ser = serial.Serial(port, BAUD_RATE, timeout=1)
				ser.write("v");
				rec = ser.read(4);
			except serial.serialutil.SerialException:
				continue
			if (re.search('v[0-9]\.[0-9]', rec)):
				print("Faberdanaio " + rec + " on port: " + port)
				ser.timeout = None # disable timeout. Not needed anymore
				break
			if (ser != 0):
				ser.close()
			ser = 0
	return ser

# initialize this module
# It requires the serial port to read, otherwise it will search automatically
def init(port = ""):
	global serPort
	
	if (port == ""): # serial port are in the form tty*
		print("No serial port specified. Trying autoscan...")
		serPort = autoscan()
	else:
		try:
			serPort = serial.Serial(port, BAUD_RATE)
		except serial.serialutil.SerialException:
			serPort = 0
	# verify the connectivity was succesful otherwise exit
	if (serPort == 0):
		print("Faberdanaio not found. Check connectivity.")
		exit()
	# read serial port in a separate thread
	thread.start_new_thread(serRead, (None,))

# return the number of pending coins and clear the counter
def getPending():
	global pending
	oldPending = pending
	pending = 0
	return oldPending

# Function that reads the serial port continuously waiting for '!'
# When a coin is detected increment pending
def serRead(arg):
	global pending
	while True:
		if (serPort.read() == '!'):
			pending = pending + 1
