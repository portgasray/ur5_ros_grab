# UR5 REALSENSE GRAB

### Download form repo

```
cd ~/catkin_ws/src
git clone https://github.com/portgasray/ur5_ros_grab.git --recursive
cd ~/catkin_ws
catkin_make
```

### simulate 

```
roslaunch ur5_moveit_config ur5_moveit_planning_execution.launch sim:=true limited:=true
roslaunch ur5_moveit_config moveit_rviz.launch config:=true
```
Under ur_ws/src, there are two folders: one is the official universal_robot, and the other is ur5_ROS-Gazebo. Open file ur5_joint_limited_robot.urdf.xacro under ur_ws/src/universal_robot/ur_description/urdf/, and make the following change to the joint limit:
```
shoulder_pan_lower_limit="${-2*pi}" shoulder_pan_upper_limit="${2*pi}"
```


In the same directory`universal_robot/ur_description/urdf/`, make a copy of common.gazebo.xacro and ur5.urdf.xacro in case of any malfunction.
```
mkdir backups
cp common.gazebo.xacro ur5.urdf.xacro backups/.
```
These two default files do not include camera and vacuum gripper modules. So we would replace these two files with customized files. Under directory src/ur5_ROS-Gazebo/src/ur_description/, copy common.gazebo.xacro and ur5.urdf.xacro to src/universal_robot/ur_description/urdf/.
