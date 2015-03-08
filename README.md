# faberdanaio
Offer box for my local hackerspace (Faber Libertatis, Padova, Italy).
The goal of this project is repurposing an old PC to act as a money box.
In this repository there are the software and hardware needed to achieve such goal.

The device is made up of a sensor based on a PIC12F509 which sends a '!' through
the serial port each time a coin is inserted. The detection is fairly simple.
The microcontroller generates a square wave at 6kHz which drives an LED.
The light beam is collected by a photoresistor and converted back into a pulse.
A simple circuit with an opamp then works as an amplifier, high-pass filter
(to avoid triggering on ambient light) and detector.

This repository holds the source code for the firmware and for the application
that runs on the PC. Also the schematic and the board layout will be added in
the future.