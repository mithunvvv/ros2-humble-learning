https://docs.ros.org/en/humble/How-To-Guides/Run-2-nodes-in-single-or-separate-docker-containers.html

these have instructions on how to run with container

* might need to do this before ```newgrp docker```

1. ```docker pull osrf/ros:humble-desktop```
2. 

```
docker build \
  --build-arg USER_UID=$(id -u) \
  --build-arg USER_GID=$(id -g) \
  -t ros2-dev .
```

```
xhost +local:docker
docker run -it \
  --env="DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --volume="/home/mva/ros2-humble-learning:/home/devuser/ros2-humble-learning" \
    ros2-dev:v3   
    
```

Next:
1. allow for ros2 autocomplete:
add the following to the bashrc file 
```
/opt/ros/humble/setup.bash
```

when making a new workspace:
1. make the workspace

2. mkdir src in the pkg 

```
colcon build
```

3. 
```
ros2 pkg create my_robot_controller --build-type ament_python --dependencies rcply
```
create the package under the src folder of the workspace 
each package corresponds to a different component of the robot
all the nodes in a package are relevant to that robot component 

4. add the following to the bashrc file in order to use custom ros2 nodes 

```
source /home/ros2-humble-learning/ros2_ws/install/setup.bash
```

```
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
``` 
allows for colcon to do autocompletions (cli tool to build ros2 workspaces)

5. build the package(s)

go back to the workspace folder and run

```
colcon build 
```

6. 

## Creating Service

Topics send data from one point to another but they don't send a response

Service can act like a client and server
used for a computation or change of setting 

Topics used to send data without expecting an answer, ex, command vel
