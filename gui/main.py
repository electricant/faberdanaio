#!/usr/bin/python
#
# Entry point for the program to interface with faberdanaio. It displays a
# counter and a simple animation
#
# This code is distributed under the GNU GPL v3
# Copyright (C) 2015 - Electric Ant <electrican@anche.no>
#

import Tkinter # requires python-tk/python-tkinter package
from PIL import ImageTk, Image # requires python-pil.imagetk/py-Pillow
import random
import sys		# for parsing the command line

import serio	# see serio.py in this directory	

#
# TUNABLES
#
REFRESH_RATE_MS = 30 # ~30 fps
ANI_WIDTH_RATIO = 0.2 # of screen width for the animated image

#
# Global variabes
#
speedX = 1
speedY = 1
MAX_X = 0		# Maximum x location for the bouncy image
MAX_Y = 0		# Maximum y location for the bouncy image
MIN_X = 0
MIN_Y = 0
offers = 0		# offers received
bouncyLabel = 0	# Label to which the bounce effect is applied
offerLabel = 0	# Label counting offers number

# Update what is shown on the screen
def update_view(root):
	global bouncyLabel, offerLabel
	global speedX, speedY
	global MAX_X, MIN_X
	global MAX_Y, MIN_Y
	global offers

	posX = bouncyLabel.winfo_x() + speedX
	posY = bouncyLabel.winfo_y() + speedY

	if (posX >= MAX_X):
		speedX = speedX * -1
		posX = MAX_X - 1
	if (posX <= MIN_X):
		speedX = speedX * -1 # Reverse!
		posX = MIN_X + 1
	if (posY >= MAX_Y):
		speedY = speedY * -1
		posY = MAX_Y - 1
	if (posY <= MIN_Y):
		speedY = speedY * -1 # Reverse!
		posY = MIN_Y + 1
	bouncyLabel.place(x = posX, y = posY)
	
	offers = offers + serio.getPending()
	offerLabel.config(text = "Offerte oggi: %u" % offers)
	
	root.after(REFRESH_RATE_MS, update_view, root) # reschedule
#
# Main
#
serial_port = True
if (len(sys.argv) == 2):
	if (sys.argv[1] == "noserial"):
		serial_port = False

if (serial_port):
	serio.init()

root = Tkinter.Tk();
root.attributes("-fullscreen", True)
root.bind("<Escape>", exit) # listen to <ESC> key press and exit
root.config(bg="white")

# resize image keeping aspect ratio. The reference is the screen size in order
# to be consistent on every screen resolution and size
bouncyImage = Image.open("pig.png")
newWidth = ANI_WIDTH_RATIO * root.winfo_screenwidth()
ratio = newWidth / bouncyImage.size[0]
newHeight = bouncyImage.size[1] * ratio
bouncyImage = bouncyImage.resize((int(newWidth), int(newHeight)), Image.ANTIALIAS)

bImage = ImageTk.PhotoImage(bouncyImage)
bouncyLabel = Tkinter.Label(root, image = bImage, bg="white")
bouncyLabel.pack()

# place "Faberlibertatis" logo top center
logoImg = Image.open("logo_faber.png")
lImage = ImageTk.PhotoImage(logoImg)
logoLabel = Tkinter.Label(root, image = lImage, bg="white")
logoLabel.pack(side = "top")

# place a label that counts the number of offers received so far
offerLabel = Tkinter.Label(root, text="Offerte oggi: %u" % offers, fg="blue",
				   font=("Sans Serif", 32), bg="white")
offerLabel.pack(side = "bottom")
# done placing things. Update the view
root.update()
# The bouncy image must not go under the logo so take that into account
MAX_X = root.winfo_screenwidth() - bouncyLabel.winfo_width()
MAX_Y = root.winfo_screenheight() - bouncyLabel.winfo_height()
MIN_Y = logoLabel.winfo_height()
# Add a bit of randomness in the choiche of the speed
speedX = random.randint(1,4)
speedY = random.randint(1,4)
print("speedX = %u, speedY = %u" % (speedX, speedY))
# Start the animation
root.after(REFRESH_RATE_MS, update_view, root)

root.mainloop();
