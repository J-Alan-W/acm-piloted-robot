#!/usr/bin/env python
# coding: utf-8

# Authors: Tytrez Dixon, Cannon Miles, Alan Wallace
# Last Updated: 4/8/2025
# Purpose: Script to control an iRobot Create 2 to be driven via a wired or wireless Xbox360 gamepad (controller)
# We used a wireless 2.4Ghz PS3 Controller

# Import necessary libraries
# PilotedRobot is built off of code from CS330 Robotics, 
# Time is built-in, Gamepad is from https://github.com/piborg/Gamepad
import time
import Gamepad
from Controllers import Xbox360
from PilotedRobot import PilotedRobot

#----------------------------------------
# Start the robot
#----------------------------------------

# Initialize a new Robot and start it
# Our robot's name is BT-7274
bt7274: PilotedRobot = PilotedRobot("/dev/ttyUSB0") # Potential future work: Try different serial ports if USB0 not found?
bt7274.startSequence()
# Protocol 1: Link to Pilot
# Protocol 2: Uphold the Mission
# Protocol 3: Protect the Pilot
print('Controls transferred to Pilot.')

#----------------------------------------
# Start the gamepad
#----------------------------------------

# Set up gamepad
gamepadType = Xbox360

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad. Waiting', end='')
    while not Gamepad.available():
        # For debugging purposes, provide a visual to represent waiting for gamepad.
        print('.', end='')
        # Specify a time interval so we don't hog system resources by checking too often
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected. Welcome back Pilot.')

'''
This bit of code was only used for getting the numerical value of joystick magnitude
(e.g. LEFT-Y is currently at 45% pushed)
Currently, any push just toggles movement in that direction, so this is unused

# Set an inital state
linearSpeed = 0.0
turnSpeed = 0.0
'''


#----------------------------------------
# Handle gamepad updates
#----------------------------------------

# Handle gamepad updates one at a time (See polling examples in Gamepad library)
while gamepad.isConnected():
    # Wait for the next event
    eventType, control, value = gamepad.getNextEvent()

    # Determine the type
    if eventType == 'BUTTON':
        # This is a huge elif chain because it avoids checking one event multiple times.
        
        # Face buttons are used for making the robot move while pressed
        if control == 'Y':
            # Example of an event on press and release
            if value:
                bt7274.set_fwd_status(1)
                bt7274.update_motion()
            else:
                bt7274.set_fwd_status(0)
                bt7274.update_motion()
        elif control == 'B':
            if value:
                bt7274.set_right_status(1)
                bt7274.update_motion()
            else:
                bt7274.set_right_status(0)
                bt7274.update_motion()
        elif control == 'A':
            if value:
                bt7274.set_back_status(1)
                bt7274.update_motion()
            else:
                bt7274.set_back_status(0)
                bt7274.update_motion()
        elif control == 'X':
            if value:
                bt7274.set_left_status(1)
                bt7274.update_motion()
            else:
                bt7274.set_left_status(0)
                bt7274.update_motion()

        # D-Pad buttons are used for making the robot go the same distance on each press. 
        # This is useful for learn-to-code games like "Get the Mouse to the Cheese"
        # The button press is and'ed with value to make sure the action only triggers on the press, not the release.
        elif (control == 'RA') and value:
            bt7274.set_fwd_status(1)
            bt7274.update_motion()
            time.sleep(0.5)
            bt7274.set_fwd_status(0)
            bt7274.update_motion()
        elif (control == 'DPAD-RIGHT') and value:
            bt7274.set_right_status(1)
            bt7274.update_motion()
            time.sleep(0.5)
            bt7274.set_right_status(0)
            bt7274.update_motion()
        elif (control == 'LA') and value:
            bt7274.set_back_status(1)
            bt7274.update_motion()
            time.sleep(0.5)
            bt7274.set_back_status(0)
            bt7274.update_motion()
        elif (control == 'DPAD-LEFT') and value:
            bt7274.set_left_status(1)
            bt7274.update_motion()
            time.sleep(0.5)
            bt7274.set_left_status(0)
            bt7274.update_motion()

        # Triggers should change the color of the LEDs, and also what song should play.
        elif (control == 'LB') and value:
            bt7274.switchMode(3)
        # elif (control == 'L2') and value:
        #     bt7274.switchMode(1)
        elif (control == 'RB') and value:
            bt7274.switchMode(2)
        # elif (control == 'R2') and value:
        #     bt7274.switchMode(4)

        # Start, Select, and Home buttons have special effects
        elif (control == 'START') and value:
            # Play song if a song mode has been selected with the triggers
            bt7274.playSong()
        elif (control == 'BACK') and value:
            # Resets the robot
            bt7274.startSequence()
        elif (control == 'XBOX') and value:
            # XBox Home button
            # No effect right now, just an easter egg
            print('Protocol 1: Link to Pilot')
            print('Protocol 2: Uphold the Mission')
            print('Protocol 3: Protect the Pilot')

    elif eventType == 'AXIS':
        # On an Xbox360 controller, the triggers are treated as axes.
        if (control == 'RT'):
            bt7274.switchMode(1)
            #print('RT')
        if (control == 'LT'):
            bt7274.switchMode(4)
            #print('LT')
        
        # Joystick changed
        # Value is the magnitude of how far the joystick is away from center
        # Future work: Make robot speed proportional to how far the stick is pushed
        if (control == 'RIGHT-Y') and (value == 0):
            bt7274.set_fwd_status(0)
            bt7274.set_back_status(0)
            bt7274.update_motion()
        elif (control == 'RIGHT-Y') and (value > 0.1):
            # In these statements, the 0.1 or -0.1 just provides a barrier 
            # so the robot's movement isn't too sensitive to stick drift.
            bt7274.set_back_status(1)
            bt7274.update_motion()
        elif (control == 'RIGHT-Y') and (value < -0.1):
            bt7274.set_fwd_status(1)
            bt7274.update_motion()
        elif (control == 'LEFT-X') and (value == 0):
            bt7274.set_right_status(0)
            bt7274.set_left_status(0)
            bt7274.update_motion()
        elif (control == 'LEFT-X') and (value > 0.1):
            bt7274.set_right_status(1)
            bt7274.update_motion()
        elif (control == 'LEFT-X') and (value < -0.1):
            bt7274.set_left_status(1)
            bt7274.update_motion()
        # For testing and debugging joystick movement
        # print('%+.1f %% speed, %+.1f %% steering' % (linearSpeed * 100, turnSpeed * 100))

bt7274.stop() # If controller is unplugged, terminate the serial connection
