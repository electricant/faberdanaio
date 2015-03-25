#!/usr/bin/python
#
# Module used to play a sound chosen randomly from the sound directory.
# Inspired by 'playwav.py' from alsaaudio python module.
# SEE: https://searchcode.com/codesearch/view/18790052/
# Filenames must be in the form EFFECT_NAME + number, where number ranges from
# 0 to EFFECT_NUMBER. See getFile for details.
#
# This code is distributed under the GNU GPL v3
# Copyright (C) 2015 - Electric Ant <electrican@anche.no>
# 

import random
import wave
import alsaaudio

#
# TUNABLES
#
# soundcard to be used
SOUNDCARD='default'
# mumber of frames per period
PERIOD_SIZE=320
# directory where audio files are stored (trailing / needed)
AUDIO_DIR='audio/'
# all audio effects files begin with this token
EFFECT_NAME='grazie'
# There is this number of audio files, starting from 0
EFFECT_NUMBER=11

# Play a wave file. The 'dummy' argument is given for bind() method within tkinter
def sayThanks(dummy):
	f = getFile()
	device = alsaaudio.PCM(card='default')
	# Set attributes
	device.setchannels(f.getnchannels())
	device.setrate(f.getframerate())
	device.setperiodsize(PERIOD_SIZE)

	if f.getsampwidth() == 1: # 8bit is unsigned in wav files
		device.setformat(alsaaudio.PCM_FORMAT_U8)
	elif f.getsampwidth() == 2: # Otherwise assume signed data, little endian
		device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	elif f.getsampwidth() == 3:
		device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
	elif f.getsampwidth() == 4:
		device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
	else:
		raise ValueError('Unsupported format')
	# Read data and send it to the device
	data = f.readframes(PERIOD_SIZE)
	while data:
		device.write(data)
		data = f.readframes(PERIOD_SIZE)
	f.close()

# Return a wave file chosen randomly (beware: easter eggs are hardcoded)
def getFile():
	filename = AUDIO_DIR
	effectType = random.randint(1, 10); # 1/10 easter egg probability
	if (effectType == 10): # easter egg
		eggNum = random.randint(0, 2)
		if (eggNum == 0):
			filename += "burp.wav"
		elif (eggNum == 1):
			filename += "hasta-la-vista-baby.wav"
		elif (eggNum == 2):
			filename += "R2D2-yeah.wav"
	else:
		num = random.randint(0, EFFECT_NUMBER);
		filename += "%s%u.wav" % (EFFECT_NAME, num);

	return wave.open(filename, 'rb')