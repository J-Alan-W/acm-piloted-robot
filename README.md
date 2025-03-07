<h2>ABOUT:</h2>
This is a set of Python scripts and object-oriented classes to allow an iRobot Create 2 to be controlled via a wired or wireless PS3 controller using a Raspberry Pi 3B+. Any wireless controllers should be connected via a 2.4Ghz dongle.
<br><br>
This project was created by the Francis Marion University Association for Computing Machinery.<br>
Contributing Members: J. Alan Wallace, Cannon Miles, Tytrez Dixon
<br><br>
This project also uses the <a href="https://github.com/piborg/Gamepad">PiBorg Gamepad library</a>. 
It is released under the MIT License (see GamepadLibraryLicense.txt).

<h2>USAGE:</h2>
No formal installation is needed, simply use the command 
<code>git clone https://github.com/J-Alan-W/acm-piloted-robot</code>
 to place the code in your desired directory, then create a crontab job to run PilotRobot.py on startup using
<code>crontab -e</code>.<br><br>
The crontab job should look something like this:<br>
<code>@reboot python3 /home/roomba/acm-piloted-robot/PilotRobot.py</code> <br><br>
(Assuming your username is roomba and you place it in the default folder.
Your filepath may vary depending on your username and where you place the folder.)

<h2>CONTROLLER LAYOUT:</h2>
Left Joystick: <br>
Right Joystick: <br>
<br>
Triangle/Top face button: Move Forward until button released <br>
Circle/Right face button: Turn Right until button released<br>
Cross/Bottom face button: Move Backwards until button releasedd<br>
Square/Left face button: Turn Left until button released<br>
<br>
D-Pad Up: Move Forward for 0.5 seconds<br>
D-Pad Right: Turn Right for 0.5 seconds<br>
D-Pad Down: Move Backwards for 0.5 seconds<br>
D-Pad Left: Turn Left for 0.5 seconds<br>

<br>
L1: Set LEDs to yellow and ready Song 3<br>
L2: Set LEDs to green and ready Song 1<br>
R1: Set LEDs to orange and ready Song 2<br>
R2: Set LEDs to red and ready Song 4<br>
<br>
Select: Reset the robot<br>
Start: Play Song (if a song mode has been selected)<br>
PS Button: Nothing, reserved for future use<br>
<br>Any other buttons (back paddles, progressive triggers, etc.) are unused
<br><br>A note on movement: Inputting multiple directions at once will produce a combination of those directions. See the updateMotion() method in PilotedRobot.py for more details.
