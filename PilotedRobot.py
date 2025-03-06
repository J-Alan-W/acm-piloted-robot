# Authors: Tytrez Dixon, Cannon Miles, Alan Wallace
# Last Updated: 3/5/2025
# Purpose: Functions to enable the iRobot Create 2 to be controlled via a gamepad (controller)
# We used a wireless 2.4Ghz PS3 Controller

import serial 
import time
import struct

class PilotedRobot:
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

    # Mode variable, used to keep track of the current LED color and song is played
    # when the playSong() function is called
    songMode = 0

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

    def sendCommand(self, command):
        self.serial_connection.write(command)

    def read(self, howManyBytes):
        buttonState = self.serial_connection.read(howManyBytes)
        byte = struct.unpack('B', buttonState)[0]
        binary = '{0:08b}'.format(byte)
        return binary

    def flush(self):
        self.serial_connection.reset_input_buffer()
        time.sleep(0.5)

    def read_wall_sensor(self):
        self.sendCommand(self.sensors_cmd + self.wall_signal)

    def start(self):
        self.sendCommand(self.start_cmd)

    def startSequence(self):
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
        self.sendCommand(self.stop_cmd)
        print('Disconnected!') 

    def reset(self):
        self.sendCommand(self.reset_cmd)
        time.sleep(5)

    def safe(self):
        self.sendCommand(self.safe_cmd)

    def seekDock(self):
        self.sendCommand(self.seek_dock_cmd)   

    def drive(self, velocityHighByte, velocityLowByte, radiusHighByte, radiushLowByte):
        self.sendCommand(self.drive_cmd + velocityHighByte + velocityLowByte + radiusHighByte + radiushLowByte)

    def driveDirect(self, rightWheelHighByte, rightWheelLowByte, leftWheelHighByte, leftWheelLowByte):
        self.sendCommand(self.drive_direct_cmd + rightWheelHighByte + rightWheelLowByte + leftWheelHighByte + leftWheelLowByte)

    def leds_color(self, color: str):
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
        self.sendCommand(ledBits + powerColor + powerIntensity)        

    def digitLEDsASCII(self, digit3, digit2, digit1, digit0):
        try:
            self.sendCommand(self.ascii_digit_leds_cmd + digit3.encode("ascii") + digit2.encode("ascii") + digit1.encode("ascii") + digit0.encode("ascii"))
        except IndexError:
            print('LED display failed: Not enough numbers')

    def update_motion(self):
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
        self.status[0] = val

    def set_left_status(self, val: bool):
        self.status[1] = val

    def set_back_status(self, val: bool):
        self.status[2] = val

    def set_right_status(self, val: bool):
        self.status[3] = val

    def switchMode(self, mode: int):
        # Switches between four different 'modes' aka LED color
        # Each color has an associated song that goes with it
        match mode:
            case 1:
                self.leds_color('green')
                self.songMode = 1
            case 2:
                self.leds_color('orange')
                self.songMode = 2
            case 3:
                self.leds_color('yellow')
                self.songMode = 3
            case 4:
                self.leds_color('red')
                self.songMode = 4

    def playSong(self):
        match self.songMode:
            case 0: return
            case 1: self.playSongMode1()
            case 2: self.playSongMode2()
            case 3: self.playSongMode3()
            case 4: self.playSongMode4()

    def playSongMode1(self):
        # Tetris theme
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
        self.sendCommand(b'\x00\x0D') # song slot 0, length of 16 notes
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

    def playSongMode2(self):
        # Can be replaced by a different song in the future
        
        # Tetris theme part 2
        # BPM of music is ~150 BPM
        # Duration Constants
        HALF = (b'\x33') # Half note, 51/64 seconds
        QUAR = (b'\x1A') # Quarter note, 26/64 seconds
        EIGT = (b'\x0D') # Eighth note, 13/64 seconds
        # Note Constants
        A = (b'\x45') # Note 69
        B = (b'\x47') # Note 71
        C = (b'\x48') # Note 72
        D = (b'\x4A') # Note 74
        E = (b'\x4C') # Note 76
        F = (b'\x4D') # Note 77
        G = (b'\x4F') # Note 79
        AH = (b'\x51') # Note 81
        N = (b'\x00') # Null note for empty space

        time.sleep(1)
        self.sendCommand(b'\x8C') # 140 Song command
        time.sleep(1)
        self.sendCommand(b'\x01\x10') # song slot 1, length of 16 notes
        # Measure 3 continued
        self.sendCommand(E + QUAR)
        # Measure 4
        self.sendCommand(C + QUAR)
        self.sendCommand(A + QUAR)
        self.sendCommand(A + HALF)
        self.sendCommand(N + QUAR) # Null note to represent rest
        # Measure 5
        self.sendCommand(D + EIGT)
        self.sendCommand(D + EIGT)
        self.sendCommand(F + EIGT)
        self.sendCommand(AH + QUAR) # A from higher octave
        self.sendCommand(G + EIGT)
        self.sendCommand(F + EIGT)
        # Measure 6
        self.sendCommand(E + QUAR)
        self.sendCommand(C + EIGT)
        self.sendCommand(E + QUAR)
        self.sendCommand(D + EIGT)
        self.sendCommand(C + EIGT)
    
    def playSongMode3(self):
        # Can be replaced by a different song in the future
        
        # Tetris theme part 3
        # BPM of music is ~150 BPM
        # Duration Constants
        HALF = (b'\x33') # Half note, 51/64 seconds
        QUAR = (b'\x1A') # Quarter note, 26/64 seconds
        EIGT = (b'\x0D') # Eighth note, 13/64 seconds
        # Note Constants
        A = (b'\x45') # Note 69
        B = (b'\x47') # Note 71
        C = (b'\x48') # Note 72
        D = (b'\x4A') # Note 74
        E = (b'\x4C') # Note 76

        self.sendCommand(b'\x8C') # 140 Song command
        self.sendCommand(b'\x02\x0E') # song slot 2, length of 14 notes
        # Measure 7
        self.sendCommand(B + QUAR)
        self.sendCommand(B + EIGT)
        self.sendCommand(C + EIGT)
        self.sendCommand(D + QUAR)
        self.sendCommand(E + QUAR)
        # Measure 8
        self.sendCommand(C + QUAR)
        self.sendCommand(A + QUAR)
        self.sendCommand(A + HALF)
        # Measure 9
        self.sendCommand(E + QUAR)
        self.sendCommand(B + EIGT)
        self.sendCommand(C + EIGT)
        self.sendCommand(D + QUAR)
        self.sendCommand(C + EIGT)
        self.sendCommand(B + EIGT)


    
    def playSongMode4(self):
        # Can be replaced by a different song in the future
        
        # Tetris theme part 4
        # BPM of music is ~150 BPM
        # Duration Constants
        HALF = (b'\x33') # Half note, 51/64 seconds
        QUAR = (b'\x1A') # Quarter note, 26/64 seconds
        EIGT = (b'\x0D') # Eighth note, 13/64 seconds
        # Note Constants
        A = (b'\x45') # Note 69
        B = (b'\x47') # Note 71
        C = (b'\x48') # Note 72
        D = (b'\x4A') # Note 74
        E = (b'\x4C') # Note 76

        self.sendCommand(b'\x8C') # 140 Song command
        time.sleep(1)
        self.sendCommand(b'\x03\x0E') # song slot 3, length of 14 notes
        # Measure 10
        self.sendCommand(A + QUAR)
        self.sendCommand(A + EIGT)
        self.sendCommand(C + EIGT)
        self.sendCommand(E + QUAR)
        self.sendCommand(D + EIGT)
        self.sendCommand(C + EIGT)
        # Measure 11
        self.sendCommand(B + QUAR)
        self.sendCommand(B + EIGT)
        self.sendCommand(C + EIGT)
        self.sendCommand(D + QUAR)
        self.sendCommand(E + QUAR)
        # Measure 12
        self.sendCommand(C + QUAR)
        self.sendCommand(A + QUAR)
        self.sendCommand(A + HALF)