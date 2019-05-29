# UR5 REALSENSE GRIP

## Calibration

### Install easy_handeye

  * install dependence packages:
```
$ sudo apt-get install ros-kinetic-visp
```

```
git clone https://github.com/portgasray/ur5_ros_grab.git --recursive
cd ~/catkin_ws/src

catkin_make
```

create [ur5_realsense_handeyecalibration.launch](https://github.com/portgasray/easy_handeye/blob/dev/easy_handeye/launch/ur5_realsense_handeyecalibration.launch) under easy_handeye/launch


* Run calibration program
