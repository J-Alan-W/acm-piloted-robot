#!/usr/bin/env python
# coding: utf-8

# Import necessary libraries
# PilotedRobot is built off of code from CS330 Robotics, 
# Time is built-in, Gamepad is from https://github.com/piborg/Gamepad
import time
import Gamepad
from Controllers import PS3
from PilotedRobot import PilotedRobot

# Set up gamepad
gamepadType = PS3
# Face Buttons (FB)
FB_Up       = 'TRIANGLE'
FB_Down     = 'CROSS'
FB_Left     = 'SQUARE'
FB_Right    = 'CIRCLE'
# D-Pad Buttons (DP)
DP_Up       = 'DPAD-UP'
DP_Down     = 'DPAD-DOWN'
DP_Left     = 'DPAD-LEFT'
DP_Right    = 'DPAD-RIGHT'
# Triggers (TR)
TR_L1 = 'L1'
TR_L2 = 'L2'
TR_R1 = 'R1'
TR_R2 = 'R2'
# Special Buttons (SB)
SB_PS = 'PS' # Playstation Logo button
SB_Start = 'START'
SB_Select = 'SELECT'
# Joystick Left (JL)
joystickSteering = 'LEFT-X'
# Joystick Right (JR)
joystickSpeed = 'RIGHT-Y'

#----------------------------------------
# Start the robot
#----------------------------------------

# Initialize a new Robot and start it
# Our robot's name is BT-7274
bt7274: PilotedRobot = PilotedRobot("/dev/ttyUSB0")
bt7274.startSequence()
# Protocol 1: Link to Pilot
# Protocol 2: Uphold the Mission
# Protocol 3: Protect the Pilot
print('Controls transferred to Pilot.')

#----------------------------------------
# Start the gamepad
#----------------------------------------

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

# Set an inital state
speed = 0.0
steering = 0.0

#----------------------------------------
# Handle gamepad updates
#----------------------------------------

# Handle gamepad updates one at a time
while gamepad.isConnected():
    # Wait for the next event
    eventType, control, value = gamepad.getNextEvent()

    # Determine the type
    if eventType == 'BUTTON':
        # Why is this a huge elif chain? It avoids checking one impulse multiple times.
        
        # Face buttons are used for making the robot move while pressed
        if control == FB_Up:
            # Example of an event on press and release)
            if value:
                bt7274.set_fwd_status(1)
                bt7274.update_motion()
            else:
                bt7274.set_fwd_status(0)
                bt7274.update_motion()
        elif control == FB_Down:
            if value:
                bt7274.set_back_status(1)
                bt7274.update_motion()
            else:
                bt7274.set_back_status(0)
                bt7274.update_motion()
        elif control == FB_Left:
            if value:
                bt7274.set_left_status(1)
                bt7274.update_motion()
            else:
                bt7274.set_left_status(0)
                bt7274.update_motion()
        elif control == FB_Right:
            if value:
                bt7274.set_right_status(1)
                bt7274.update_motion()
            else:
                bt7274.set_right_status(0)
                bt7274.update_motion()

        # D-Pad buttons are used for making the robot go the same distance on each press. 
        # This is useful for learn-to-code games like "Get the Mouse to the Cheese"
        # The button press is and'ed with value to make sure the action only triggers on the press, not the release.
        elif (control == DP_Up) and value:
            bt7274.set_fwd_status(True)
            bt7274.update_motion()
            time.sleep(0.5)
            bt7274.set_fwd_status(False)
            bt7274.update_motion()
        elif (control == DP_Down) and value:
            bt7274.set_back_status(True)
            bt7274.update_motion()
            time.sleep(0.5)
            bt7274.set_back_status(False)
            bt7274.update_motion()
        elif (control == DP_Left) and value:
            bt7274.set_left_status(True)
            bt7274.update_motion()
            time.sleep(0.5)
            bt7274.set_left_status(False)
            bt7274.update_motion()
        elif (control == DP_Right) and value:
            bt7274.set_right_status(True)
            bt7274.update_motion()
            time.sleep(0.5)
            bt7274.set_right_status(False)
            bt7274.update_motion()

        # Triggers should change the color of the LEDs
        # and also what song should play.
        elif control == TR_L1:
            # Example of an event on press only
            if value:
                bt7274.switchMode(3)
        elif control == TR_L2:
            if value:
                bt7274.switchMode(1)
        elif control == TR_R1:
            if value:
                bt7274.switchMode(2)
        elif control == TR_R2:
            if value:
                bt7274.switchMode(4)

        elif (control == SB_Start) and value:
            bt7274.playSong()
        elif (control == SB_Select) and value:
            bt7274.reset()
            bt7274.startSequence()
        elif (control == SB_PS) and value:
            print('Protocol 1: Link to Pilot')
            print('Protocol 2: Uphold the Mission')
            print('Protocol 3: Protect the Pilot')

    elif eventType == 'AXIS':
        # Joystick changed
        if control == joystickSpeed:
            # Speed control (inverted)
            speed = -value
        elif control == joystickSteering:
            # Steering control (not inverted)
            steering = value
        print('%+.1f %% speed, %+.1f %% steering' % (speed * 100, steering * 100))