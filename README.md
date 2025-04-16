<h2>ABOUT:</h2>
This is a set of Python scripts and object-oriented classes to allow an iRobot Create 2 to be controlled via a wired or wireless Xbox 360 controller using a Raspberry Pi 3B+.
<br><br>
This project was created by the Francis Marion University Association for Computing Machinery.<br>
Contributing Members: J. Alan Wallace, Cannon Miles, Tytrez Dixon
<br><br>
Please note this project is very specific to our use case. You are free to reference,download, and modify this code, but no warranty or fitness for purpose is given.
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
Your filepath may vary depending on your username and where you place the folder.)<br><br>
Shut down the Raspberry Pi, then plug in the iRobot cable. Reboot the Raspberry Pi, and while it's rebooting turn on the controller. Once the Pi has booted, plug in the controller and everything should work!


<h2>CONTROLLER LAYOUT:</h2>
Left Joystick: Pushing the stick left or right makes the robot turn.<br>
Right Joystick: Pushing the stick up or down makes the robot move linearly<br>
<br>
Y: Move Forward until button released <br>
B: Turn Right until button released<br>
A: Move Backwards until button releasedd<br>
X: Turn Left until button released<br>
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
Home: Nothing, reserved for future use<br>
<br>Any other buttons (back paddles, progressive triggers, etc.) are unused.
<br><br>A note on movement: Inputting multiple directions at once will produce a combination of those directions. See the updateMotion() method in PilotedRobot.py for more details.

<h2>DETAILED INSTRUCTIONS:</h2>
These instructions are mainly for other FMU ACM members with a similar use case (Raspberry Pi 3B+ and iRobot Create 2). <br><br>
Please Note: Any wireless controllers should be connected via a 2.4Ghz dongle. Device autoconnection at startup poses a challenge for using Bluetooth wireless controllers, so unless you want to tackle that challenge, use a 2.4Ghz wireless controller.<br><br>
<ol>
<li> Using the Raspberry Pi Imager (https://www.raspberrypi.com/software/), select Raspbian Lite, setup a user named 'roomba', and set up SSH to your preferred network. Note that FMU WiFi might not work for this because you have to authenticate before the network will allow you to connect.
<li> Connect to the Raspberry Pi via SSH (https://www.raspberrypi.com/documentation/computers/remote-access.html).
<li> Type the commands <code>sudo apt update</code> and <code>sudo apt full-upgrade</code>
<li> Newer versions of Raspbian don't have git installed by default. You can check via <code>git --version</code>. If git isn't found, install it via <code>sudo apt-get install git</code>
<li> Clone the repo with <code>git clone http://github.com/J-Alan-W/acm-piloted-robot</code>
<li> Python should be installed by default. Check the version with <code>python3 --version</code>
<li> Install the Python serial module for controlling the robot with <code>sudo apt-get install python3-serial</code>
<li> Create a new crontab job to run PilotRobot.py on startup with <code>crontab -e</code> (If you have multiple editors, choose the nano in-terminal editor).
<li> 
    Scroll down to the bottom of the file and type: 
    <code>@reboot python3 /home/roomba/acm-piloted-robot/PilotRobot.py</code>. 
    This assumes your username is roomba and you place it in the default folder.
<li> Hit CTRL-S and CTRL-X to save and exit
<li> Check everything wrote correctly using the <code>crontab -l</code> command.
</ol><br>
At this point, you should be ready to go. Connect the iRobot Create 2 to the Raspberry Pi, plug in the controller, and reboot the Pi. After reboot, it should work!
<br><br>
If you need to update the files on the Pi, simply SSH into it again, cd to the repo folder, and run the command <code>git pull https://github.com/J-Alan-W/acm-piloted-robot main</code>.
