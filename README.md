# ros2-humble-learning

## Terms 

### ROS2 Node: 

A ROS2 program the communicates with ROS2 communications and tools 
ROS2 nodes are organized in packages, ex. packages for camera driver, navigation
Each package will have nodes

```
docker run -it --platform linux/amd64 osrf/ros:humble-desktop
```
this is bc I have an M1 chip mac (arm 64 ISA), setting the amd64 flag uses an emulation 

```
docker run -it \
  --name ros2_container \
  --env="DISPLAY=host.docker.internal:0" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  -v ~/ros2-humble-learning:/root/ros2-humble-learning \
  --platform linux/amd64 \
  osrf/ros:humble-desktop
```

```
docker run -p 6080:80 \
  --security-opt seccomp=unconfined \
  --volume="/Users/mithunvanniasinghe/ros2-humble-learning:/home/ubuntu" \
  --shm-size=512m \
  ghcr.io/tiryoh/ros2-desktop-vnc:humble 

```

https://github.com/Tiryoh/docker-ros2-desktop-vnc

```http://127.0.0.1:6080/```
https://medium.com/@arohanaday/how-i-set-up-ros-2-on-my-macbook-using-docker-without-losing-my-sanity-fe6e55857cc2 

```
run package-name node-name
ros2 run demo_nodes_cpp talker 
```

Note: can only run 1 ros2 command per docker container 
- why?? 

To get GUI:
```
xhost + 127.0.0.1  
docker run -it \ 
  --platform linux/amd64 \
  -e DISPLAY=host.docker.internal:0 \
  osrf/ros:humble-desktop
```

### ROS2 Workspace

```
sudo apt install python3-colcon-common-extensions 
```
`source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash`
add to bashrc to have colcon be available in cli for every new shell created 

colcon build is a command-line tool used in ROS 2 (and other similar environments) to build software packages.

` source ~/ros2_ws/install/setup.bash  ` in order to use the node you created 
code for the node goes into the `src` folder 
add this line to the bashrc file so that node is always avail for use 

create a package: 
```ros2 pkg create my_robot_controller
```
```
ros2 pkg create my_robot_controller --build-type ament_
ament_cmake   ament_python 
```
use ament_python bc we are using the colcon (python based) build system 


After creating a new node:
1. rebuild: `colcon build` in workspace directory
2. need to source bashrc after creating a new node to register the new node in the terminal
3. add executable name into the setup.py entrypoints in the node's package 

3 names:
1. file name where the node lives 
2. the nodes name (when you inherit from the superclass, you can give the node a name)
3. the exectuable name (what you call the node when you use the CLI)

```colcon build --symlink-install ```
this symlink prevents you from having to rebuild each time you make a change
activate it for the first time by sourcing the bashrc file 


### Topics

Nodes can either publish or subscribe to a topic
topic are mid-point between nodes that wanna communicate with one another

Nodes don't direct to each other 

Topics have a data type 
- can inspect with `ros2 interface show <name of type>`


### Topic Publisher 

### Topic Subscriber 