# Authors: Tytrez Dixon, Cannon Miles, Alan Wallace
# Last Updated: 3/5/2025
# Purpose: Functions to enable the iRobot Create 2 to be controlled by ControllerUI.py
# Version for controlling the robot using a gamepad

import serial 
import time
import struct

class PilotedRobot:
    """_summary_

    Returns:
        _type_: _description_
    """
    # commands definitions
    start_cmd               =  b'\x80' # 128
    safe_cmd                =  b'\x83' # 131
    sensors_cmd             =  b'\x8E' # 142
    reset_cmd               =  b'\x07' # 7
    stop_cmd                =  b'\xAD' # 173
    buttons_cmd	            =  b'\xA5' # 165
    drive_direct_cmd        =  b'\x91' # 145
    drive_cmd               =  b'\x89' # 137
    leds_cmd                =  b'\x8B' # 139
    digit_leds_cmd          =  b'\xA3' # 163
    ascii_digit_leds_cmd    =  b'\xA4' # 164
    seek_dock_cmd           =  b'\x8F' # 143

    # packet IDs definitions
    wall					 =  b'\x08'
    bumps_and_wheels	     =  b'\x07'
    cliff_left				 =  b'\x09'
    cliff_front_left		 =  b'\x0A'
    cliff_front_right		 =  b'\x0B'
    cliff_right				 =  b'\x0C'
    virtual_wall			 =  b'\x0D'
    buttons					 =  b'\x12'
    distance				 =  b'\x13'
    angle					 =  b'\x14'
    charging_state			 =  b'\x15'
    voltage					 =  b'\x16'
    temperature				 =  b'\x18'
    battery_charge			 =  b'\x19'
    wall_signal				 =  b'\x1B'
    cliff_left_signal		 =  b'\x1C'
    cliff_front_left_signal	 =  b'\x1D'
    cliff_front_right_signal =  b'\x1E'
    cliff_right_signal		 =  b'\x1F'

    # Status array used in the movement of the robot
    # Format:   W      A      S      D    is key pressed?
    status = [False, False, False, False]
    # Standard speeds are 200 mm/s forwards and backwards

    def __init__(self, port):
        try:
            self.serial_connection = serial.Serial(port, baudrate=115200, timeout=1)
            print ("Connected!")
        except serial.SerialException:
            print ("Connection failure!")
            return
        time.sleep(1)
        self.serial_connection.close()
        time.sleep(1)
        self.serial_connection.open()

    def sendCommand(self, input):
        """_summary_

        Args:
            input (_type_): _description_
        """
        self.serial_connection.write(input)

    def read(self, howManyBytes):
        """_summary_

        Args:
            howManyBytes (_type_): _description_

        Returns:
            _type_: _description_
        """
        buttonState = self.serial_connection.read(howManyBytes)
        byte = struct.unpack('B', buttonState)[0]
        binary = '{0:08b}'.format(byte)
        return binary

    def flush(self):
        """_summary_
        """
        self.serial_connection.reset_input_buffer()
        time.sleep(0.5)


    def read_wall_sensor(self):
        """_summary_
        """
        self.sendCommand(self.sensors_cmd + self.wall_signal)

    def start(self):
        """_summary_
        """
        self.sendCommand(self.start_cmd)

    def startSequence(self):
        """_summary_
        """
        # Function created by authors
        # Performs the entire startup sequence with one function call for convenience
        self.sendCommand(self.start_cmd)
        time.sleep(1)
        self.sendCommand(self.reset_cmd)
        time.sleep(5)
        self.sendCommand(self.start_cmd)
        time.sleep(1)
        self.sendCommand(self.safe_cmd)
        print('Startup sequence complete!')

    def stop(self):
        """_summary_
        """
        self.sendCommand(self.stop_cmd)
        print('Disconnected!') 

    def reset(self):
        """_summary_
        """
        self.sendCommand(self.reset_cmd)
        time.sleep(5)

    def safe(self):
        """_summary_
        """
        self.sendCommand(self.safe_cmd)

    def seekDock(self):
        """_summary_
        """
        self.sendCommand(self.seek_dock_cmd)   

    def drive(self, velocityHighByte, velocityLowByte, radiusHighByte, radiushLowByte):
        """_summary_

        Args:
            velocityHighByte (_type_): _description_
            velocityLowByte (_type_): _description_
            radiusHighByte (_type_): _description_
            radiushLowByte (_type_): _description_
        """
        self.sendCommand(self.drive_cmd + velocityHighByte + velocityLowByte + radiusHighByte + radiushLowByte)

    def driveDirect(self, rightWheelHighByte, rightWheelLowByte, leftWheelHighByte, leftWheelLowByte):
        """_summary_

        Args:
            rightWheelHighByte (_type_): _description_
            rightWheelLowByte (_type_): _description_
            leftWheelHighByte (_type_): _description_
            leftWheelLowByte (_type_): _description_
        """
        self.sendCommand(self.drive_direct_cmd + rightWheelHighByte + rightWheelLowByte + leftWheelHighByte + leftWheelLowByte)

    def leds_color(self, color: str):
        """_summary_

        Args:
            color (str): _description_
        """
        # Added by authors, allows the Controller to pass in a color rather than series of arguments for the leds() method
        match color:
            case "green":
                # 139 0 0 255
                self.sendCommand(self.leds_cmd + b'\x00' + b'\x00' + b'\xFF')
            case "yellow":
                # 139 0 16 255
                self.sendCommand(self.leds_cmd + b'\x00' + b'\x10' + b'\xFF')
            case "orange":
                # 139 0 64 255
                self.sendCommand(self.leds_cmd + b'\x00' + b'\x40' + b'\xFF')
            case "red":
                # 139 0 255 255
                self.sendCommand(self.leds_cmd + b'\x00' + b'\xFF' + b'\xFF')

    def leds(self, ledBits, powerColor, powerIntensity):
        """_summary_

        Args:
            ledBits (_type_): _description_
            powerColor (_type_): _description_
            powerIntensity (_type_): _description_
        """
        self.sendCommand(ledBits + powerColor + powerIntensity)        

    def digitLEDsASCII(self, digit3, digit2, digit1, digit0):
        """_summary_

        Args:
            digit3 (_type_): _description_
            digit2 (_type_): _description_
            digit1 (_type_): _description_
            digit0 (_type_): _description_
        """
        try:
            self.sendCommand(self.ascii_digit_leds_cmd + digit3.encode("ascii") + digit2.encode("ascii") + digit1.encode("ascii") + digit0.encode("ascii"))
        except IndexError:
            print('LED display failed: Not enough numbers')

    def update_motion(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        # This function adjusts the movement of the robot, after the status register has been updated.
        # For example, to make the robot go forward, you would use set_fwd_status(true) then update_motion()

        # Velocity  = 200mm/s (this is the same speed we use elsewhere, assume turning velocity is the same as straight velocity)
        # T = 15s (this means the robot should complete a full circle every 15 seconds)
        # Turn radius = 478mm (Derived from the formula v=(2*pi*r)/T )
        # This translates to \x01\xDE or \xFE\x22
       
        # This treats the values in the status array as a binary number
        # and converts it into a decimal value for easy comparison within the switch case
        place_value = 1
        status_num = 0
        for bit in reversed(self.status):
            status_num = status_num + (bit*place_value)
            place_value *= 2
      
        match status_num:
            case 0:
                self.drive(b'\x00', b'\x00', b'\x00', b'\x00') # Stop
            case 1:
                self.drive(b'\x00', b'\x65', b'\xFF', b'\xFF') # Turn Right (Clockwise) in Place
            case 2:
                self.drive(b'\xFF', b'\x38', b'\x00', b'\x00') # Backwards
            case 3:
                self.drive(b'\xFF', b'\x38', b'\xFE', b'\x22') # Backwards While Veering Right
            case 4:
                self.drive(b'\x00', b'\x65', b'\x00', b'\x01') # Turn Left (Counterclockwise) in Place
            case 5:
                self.drive(b'\x00', b'\x00', b'\x00', b'\x00') # Stop (No Rotation)
            case 6:
                self.drive(b'\xFF', b'\x38', b'\x01', b'\xDE') # Backwards While Veering Left
            case 7:
                self.drive(b'\xFF', b'\x38', b'\x00', b'\x00') # Backwards
            case 8:
                self.drive(b'\x00', b'\xCB', b'\x00', b'\x00') # Forward
            case 9:
                self.drive(b'\x00', b'\xCB', b'\xFE', b'\x22') # Forward While Veering Right
            case 10:
                self.drive(b'\x00', b'\x00', b'\x00', b'\x00') # Stop
            case 11:
                self.drive(b'\x00', b'\x65', b'\xFF', b'\xFF') # Turn Right (Clockwise) in Place
            case 12:
                self.drive(b'\x00', b'\xCB', b'\x01', b'\xDE') # Forward While Veering Left
            case 13:
                self.drive(b'\x00', b'\xCB', b'\x00', b'\x00') # Forward
            case 14:
                self.drive(b'\x00', b'\x65', b'\x00', b'\x01') # Turn Left (Counterclockwise) in Place
            case 15:
                self.drive(b'\x00', b'\x00', b'\x00', b'\x00') # Stop
            case _:
                # Default case
                self.drive(b'\x00', b'\x00', b'\x00', b'\x00') # Stop
            
        return status_num

    def set_fwd_status(self, val: bool):
        """_summary_

        Args:
            val (bool): _description_
        """
        self.status[0] = val

    def set_left_status(self, val: bool):
        """_summary_

        Args:
            val (bool): _description_
        """
        self.status[1] = val

    def set_back_status(self, val: bool):
        """_summary_

        Args:
            val (bool): _description_
        """
        self.status[2] = val

    def set_right_status(self, val: bool):
        """_summary_

        Args:
            val (bool): _description_
        """
        self.status[3] = val

    def playSong(self):
        """_summary_
        """
        # Added by authors, loads and plays part of the Tetris theme
        # This code was adapted from our song.py file

        # BPM of music is ~150 BPM
        # Duration Constants
        QUAR = (b'\x1A') # Quarter note, 26/64 seconds
        EIGT = (b'\x0D') # Eighth note, 13/64 seconds

        # Note Constants
        A = (b'\x45') # Note 69
        B = (b'\x47') # Note 71
        C = (b'\x48') # Note 72
        D = (b'\x4A') # Note 74
        E = (b'\x4C') # Note 76

        #Start of Song 0
        self.sendCommand(b'\x8C') # 140 Song command
        self.sendCommand(b'\x00\x0D') # song 0, length of 16 notes
        # Measure 1
        self.sendCommand(E + QUAR)
        self.sendCommand(B + EIGT)
        self.sendCommand(C + EIGT)
        self.sendCommand(D + QUAR)
        self.sendCommand(C + EIGT)
        self.sendCommand(B + EIGT)
        # Measure 2
        self.sendCommand(A + QUAR)
        self.sendCommand(A + EIGT)
        self.sendCommand(C + EIGT)
        self.sendCommand(E + QUAR)
        self.sendCommand(D + EIGT)
        self.sendCommand(C + EIGT)
        #Measure 3
        self.sendCommand(B + QUAR)

        self.sendCommand(b'\x8D\x00') # Play song 0
