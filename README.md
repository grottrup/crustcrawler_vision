Within ROS workspace named catkin_ws run the following:

``` bash
source devel/setup.bash
catkin_make
```

Test that ROS works:

``` bash
roscore
```

Go to `catkin_ws/src` and create a new package. This package can be initialized as a github repository if you want it backed up.

```
catkin_create_pkg crustcrawler_vision message_generation rospy cv2
```

Add messages, update package.xml and CMakeList.txt to have the needed dependencies.

---

``` bash
~/catkin_ws$ source devel/setup.bash
~/catkin_ws$ catkin_make
~/catkin_ws$ roscore
~/catkin_ws/src/crustcrawler_vision/src$ rosrun crustcrawler_vision vision_xy_node.py
```
