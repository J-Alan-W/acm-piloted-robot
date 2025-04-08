import time
import Gamepad
from Controllers import Xbox360

#----------------------------------------
# Start the gamepad
#----------------------------------------

# Set up gamepad
gamepadType =Xbox360

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
                print('Y pressed')
            else:
                print('Y released')
        elif control == 'B':
            if value:
                print('B pressed')
            else:
                print('B released')
        elif control == 'A':
            if value:
                print('A pressed')
            else:
                print('A released')
        elif control == 'X':
            if value:
                print('X pressed')
            else:
                print('X released')

        # D-Pad buttons are used for making the robot go the same distance on each press. 
        # This is useful for learn-to-code games like "Get the Mouse to the Cheese"
        # The button press is and'ed with value to make sure the action only triggers on the press, not the release.
        elif (control == 'DPAD-UP') and value:
            print('DPAD-UP pressed')
        elif (control == 'DPAD-RIGHT') and value:
            print('DPAD-RIGHT pressed')
        elif (control == 'DPAD-DOWN') and value:
            print('DPAD-DOWN pressed')
        elif (control == 'DPAD-LEFT') and value:
            print('DPAD-LEFT pressed')

        # Triggers should change the color of the LEDs, and also what song should play.
        elif (control == 'LB') and value:
            print('Left Bumper pressed')
        elif (control == 'LA') and value:
            print('Left Trigger pressed')
        elif (control == 'RB') and value:
            print('Right Bumper pressed')
        elif (control == 'RA') and value:
            print('Right Trigger pressed')

        # Start, Select, and PS have special effects
        elif (control == 'START') and value:
            print('START pressed')
        elif (control == 'BACK') and value:
            print('BACK pressed')
        elif (control == 'XBOX') and value:
            print('XBOX pressed')

    elif eventType == 'AXIS':
        # Joystick changed
        # Value is the magnitude of how far the joystick is away from center
        # Future work: Make robot speed proportional to how far the stick is pushed
        if (control == 'RIGHT-Y') and (value == 0):
            print('RIGHT-Y zero')
        elif (control == 'RIGHT-Y') and (value > 0.1):
            print('RIGHT-Y positive')
        elif (control == 'RIGHT-Y') and (value < -0.1):
            print('RIGHT-Y negative')
        elif (control == 'LEFT-X') and (value == 0):
            print('LEFT-X zero')
        elif (control == 'LEFT-X') and (value > 0.1):
            print('LEFT-X positive')
        elif (control == 'LEFT-X') and (value < -0.1):
            print('LEFT-X negative')
        # For testing and debugging joystick movement
        # print('%+.1f %% speed, %+.1f %% steering' % (linearSpeed * 100, turnSpeed * 100))

        if (control == 'RT'):
            print('RT')
        if (control == 'LT'):
            print('LT')