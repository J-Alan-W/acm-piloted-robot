
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
# Joystick Left (JL)
# Joystick Right (JR)
joystickSpeed = 'LEFT-Y'
joystickSteering = 'RIGHT-X'

#----------------------------------------
# Start the controller
#----------------------------------------

# Initialize a new Robot and start it
gundam: PilotedRobot = PilotedRobot("/dev/ttyUSB1")
gundam.startSequence()
print('Wall-E started!')


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

# Handle joystick updates one at a time
while gamepad.isConnected():
    # Wait for the next event
    eventType, control, value = gamepad.getNextEvent()

    # Determine the type
    if eventType == 'BUTTON':
        # Button changed
        if control == FB_Up:
            # (event on press and release)
            if value:
                gundam.set_fwd_status(1)
                gundam.update_motion()
            else:
                gundam.set_fwd_status(0)
                gundam.update_motion()
        elif control == FB_Down:
            # (event on press)
            if value:
                print('Moving Down')
            else:
                print('Stopped')
        elif control == FB_Left:
            # (event on press)
            if value:
                print('Moving Left')
            else:
                print('Stopped')
        elif control == FB_Right:
            # (event on press)
            if value:
                print('Moving Right')
            else:
                print('Stopped')
        #elif control == buttonExit:
        #    # Exit button (event on press)
        #    if value:
        #        print('EXIT')
        #        break
    elif eventType == 'AXIS':
        # Joystick changed
        if control == joystickSpeed:
            # Speed control (inverted)
            speed = -value
        elif control == joystickSteering:
            # Steering control (not inverted)
            steering = value
        print('%+.1f %% speed, %+.1f %% steering' % (speed * 100, steering * 100))