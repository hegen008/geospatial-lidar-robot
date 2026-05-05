# Geospatial LiDAR Robot

**Class Project for GEOG 5545, Spring 2026, University of Minnesota**

Arlan Hegenbarth, Max Kortebein, Alec Olson, Luka Pearson, Will Weatherhead

## Project Description:
This project is an attempt at creating a robot that can map out the area it's in while moving around. We accomplish this by combining a driveable robot, LiDAR system, and IMU module. 

## Contents:
**imu_integration.py:** Calculates the velocity and position from the start to get relative position.\
**imu_logger.py:** Collects the IMU data as the robot moves.\
**lidar.py:** Collects and process LiDAR data from the robot.\
**robot_controller.py:** Controls robot movement and calls other programs to records IMU and LiDAR data.

## How to Use:
*This assumes that both the LiDAR and IMU sensors are attaches to the robot.*
1. **Connect a controller:** We connected an XBox wireless controller to drive the robot. You can do this by clicking the bluetooth symbol in the top right of the Raspberry Pi's home screen, and then click "Connect Device". From there make sure your remote is in pairing mmode, and follow the given instructions.
2. **Start robot_controller.py:** In the terminal, cd into `robot_controller.py`'s parent directory. Then, run `robot_controller.py` as a python script (`python3 -m robot_controller.py`).
3. **Control the robot:** The top left joystick controls movement of the robot. The X button starts and stops LiDAR recording. The Y button exits `robot_controller.py`.
4. **Wait for post-processing:** After pressing the Y button to stop the robot, it may take a few mintues until all of the data is saved, processed, and plotted. Do not turn off the robot. Wait until the program ends to run any commands or exit the python interpreter or terminal.
5. Using the LiDAR data, one can use other software/programs to map out the area in which data was recorded.

**Note:** Data file and plots are deleted and dynamically created each time robot_controller.py is run. If you would like to permenantly save your data, copy and save it elsewhere manually.

## About the Data:
**LiDAR variables:**
- angle_data: The angle at which LiDAR point data was taken.
- dist_data: Distance LiDAR point is from the sensor.
- time_data: Gives the time of recordings in Unix format.

**IMU Variables:**
- ax, ay, az: Acceleration, as measured by the accelerometer, in the x, y, and z directions in meters/second^2. Only ax and ay are used.
- gx, gy, gz: Angular velocity, as measured by the gyroscope, around the x, y, and z axes in radians/second. Only rotation around the z axis is measured.

## References:
- PyGame was used to grab input from the controller: https://www.pygame.org/docs/ 
- RPLidar was used to get information from the LiDAR sensor: https://github.com/Roboticia/RPLidar 
- The following GitHub repository was used to set up the IMU hardware and software: https://github.com/sparkfun/SparkFun_VR_IMU_Breakout_BNO086_QWIIC
- The following Github repository was used to create the IMU's Arduino code: https://github.com/sparkfun/SparkFun_BNO08x_Arduino_Library

## Hardware:
- Robot and RaspberryPi: Yahboom's Raspbot V2 kit
- LiDAR: Slamtec's RPLIDAR A1M8
- IMU: SparkFun's VR IMU Breakout - BNO086 (Qwiic)
- Microcontroller (for IMU): DFRobot's Beetle ESP32-C6

## Note Regarding The Git Profile on the Robot's Raspberry Pi
We are currently unable to push changes made on the Raspberry Pi to GitHub because of a user called CaptRad who we cannot seem to log out. We have tried editing the Git config username and password, and this has not worked. When we edited code on the Raspberry Pi, our workaround solution to this problem was to manually upload these files to the GitHub repo in a browser. If someone in the future can figure out how to logout CaptRad and get it working to push files to the repo directly from the Raspberry Pi, that would be great.

## Common Errors:

### Joystick Error:
~~~
/home/pi/.local/lib/python3.11/site-packages/matplotlib/projections/__init__.py:63: UserWarning: Unable to import Axes3D. This may be due to multiple versions of Matplotlib being installed (e.g. as a system package and as a pip package). As a result, the 3D projection is not available.
  warnings.warn("Unable to import Axes3D. This may be due to multiple versions of "
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/pi/Desktop/geospatial-lidar-robot/robot_controller.py", line 20, in <module>
    joystick = joysticks[0]
               ~~~~~~~~~^^^
IndexError: list index out of range
~~~

#### To fix this error:
1. Make sure the joystick is connected via Bluetooth to the robot.
2. Exit out of the interactive Python mode in the terminal.
3. Rerun the `python3 -m robot_controller.py` command.
4. This normally fixes the issue.

### Matplotlib Error:
~~~
/home/pi/.local/lib/python3.11/site-packages/matplotlib/projections/__init__.py:63: UserWarning: Unable to import Axes3D. This may be due to multiple versions of Matplotlib being installed (e.g. as a system package and as a pip package). As a result, the 3D projection is not available.
  warnings.warn("Unable to import Axes3D. This may be due to multiple versions of "
~~~

#### To fix this error:
1. You can ignore this error.

### Filepath Permissions Error:
~~~
QStandardPaths: wrong permissions on runtime directory /run/user/1000, 0770 instead of 0700
~~~

#### To fix this error:
1. You can ignore this error.

### USB Port Not Found:
~~~
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/serial/serialposix.py", line 322, in open
    self.fd = os.open(self.portstr, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/dev/ttyUSB0'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/pi/.local/lib/python3.11/site-packages/rplidar.py", line 126, in connect
    self._serial_port = serial.Serial(
                        ^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/serial/serialutil.py", line 244, in __init__
    self.open()
  File "/usr/lib/python3/dist-packages/serial/serialposix.py", line 325, in open
    raise SerialException(msg.errno, "could not open port {}: {}".format(self._port, msg))
serial.serialutil.SerialException: [Errno 2] could not open port /dev/ttyUSB0: [Errno 2] No such file or directory: '/dev/ttyUSB0'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/pi/Desktop/geospatial-lidar-robot/robot_controller.py", line 35, in <module>
    lidar_inst = LidarRecording()
                 ^^^^^^^^^^^^^^^^
  File "/home/pi/Desktop/geospatial-lidar-robot/lidar.py", line 24, in __init__
    self.lidar = RPLidar(self.port)
                 ^^^^^^^^^^^^^^^^^^
  File "/home/pi/.local/lib/python3.11/site-packages/rplidar.py", line 117, in __init__
    self.connect()
  File "/home/pi/.local/lib/python3.11/site-packages/rplidar.py", line 131, in connect
    raise RPLidarException('Failed to connect to the sensor '
rplidar.RPLidarException: Failed to connect to the sensor due to: [Errno 2] could not open port /dev/ttyUSB0: [Errno 2] No such file or directory: '/dev/ttyUSB0'
~~~

#### To fix this error:
1. Turn the robot off and back on again.

### Input from Keyboard/Mouse/Sensor Connected via USB Not Registering:

Sometimes input from a keyboard or mouse plugged into the robot's USB ports won't register. When this happens, we generally notice that it is the top right USB port on the back of the robot.

#### To fix this error:
1. Refrain from using that port and/or turn the robot off and back on again.

### Raspberry Pi OS Not Initializing
~~~
error code
~~~

#### To fix this error:
1. Turn the robot off and back on again until it works.

### No Serial Output from the ESP32 Microcontroller:
Lack of serial output can be determined from the Arduino IDE or from lack of data in the IMU files.

### To fix this error:
1. Open the Arduino IDE.
2. Plug the IMU microcontroller into your computer via a USB port.
3. From the menu bar at the top of the screen, click 'Tools' and navigate to 'USB CDC On Boot:' in the dropdown and change it to 'Enabled'.
4. Compile and upload your .ino code to the microcontroller.
