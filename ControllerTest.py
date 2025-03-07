# Import necessary libraries
# PilotedRobot is built off of code from CS330 Robotics, 
# Time is built-in, Gamepad is from https://github.com/piborg/Gamepad
import time
import Gamepad
from Controllers import PS3

# Set up gamepad
gamepadType = PS3

#----------------------------------------
# Start the gamepad
#----------------------------------------

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad. Waiting')
    while not Gamepad.available():
        # For debugging purposes, provide a visual to represent waiting for gamepad.
        print('.', end='')
        # Specify a time interval so we don't hog system resources by checking too often
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

# Set an inital state
speed = 0.0
steering = 0.0

while gamepad.isConnected():
    # Wait for the next event
    eventType, control, value = gamepad.getNextEvent()

    if eventType == 'BUTTON':
        match control:
            case 'TRIANGLE':
                if value: print('Face Button Up pressed')
                else: print('Face Button Up released')
            case 'CIRCLE':
                if value: print('Face Button Right pressed')
                else: print('Face Button Right released')
            case 'CROSS':
                if value: print('Face Button Down pressed')
                else: print('Face Button Down released')
            case 'SQUARE':
                if value: print('Face Button Left pressed')
                else: print('Face Button Left released')
    elif eventType == 'AXIS':
        # Joystick changed
        if control == 'RIGHT-Y':
            # Speed control (inverted)
            speed = -value
        elif control == 'LEFT-X':
            # Steering control (not inverted)
            steering = value
        print('%+.1f %% speed, %+.1f %% steering' % (speed * 100, steering * 100))

    