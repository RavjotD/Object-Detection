# 4WD Smart Robotic Car using Raspberry Pi
## _Fall 2023 for INFO 3150_

## The purpose of this project is to demonstrate the following functionalities:
* Obstacle avoidance and detection
* Red ball tracking and following
* Human face detection

## Challenges
* Ball detection and tracking is not working
* Servos rotate too quickly to capture a clear picture of a face
* Not implementing nor cleaning classes or modules properly into one single file

|File|Function|Status|
|--|--|--|
|obstacle_avoidance.py|Avoids walls and obstacles|Working|
|ball_tracking.py|Tracks the red ball while performing obstacle detection and avoidance|Not working|
|human_detection.py|Detects faces at an upward angle of 120 degrees and rotates from 30 to 150 angles occasionally|Working|

## Future Improvements
* Clean the code
* Ball tracking
* Searching for a face while car moves

## Manual
* Python must be installed
* Download external remote program RealVNC(https://www.realvnc.com/en/connect/download/viewer/).
* Launch program by following the documentation (https://help.realvnc.com/hc/en-us/articles/360002249917-RealVNC-Connect-and-Raspberry-Pi#getting-connected-to-your-raspberry-pi-0-1)
* Connect through Local IP address on the same network and run following files: ball_tracking.py, human_faces.py, obstacle_avoidance.py
