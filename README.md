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
4. Using the LiDAR data, one can use other software/programs to map out the area in which data was recorded.

## About the Data:
**LiDAR variables:**\
angle_data: The angle at which LiDAR point data was taken.\
dist_data: Distance LiDAR point is from the sensor.\
time_data: Gives the time of recordings in Unix format.

**IMU Variables:**\
???


## References:
PyGame was used to grab input from the controller: https://www.pygame.org/docs/ \
RPLidar was used to get information from the LiDAR sensor: https://github.com/Roboticia/RPLidar \
IMU: ???


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
