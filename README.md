# Base on ROS2 Foxy
## Build
```shell
colcon build --packages-select driver_msgs driver process
```
### Run driver node
```shell
ros2 run driver driver
```
### Run process node
```shell
ros2 run process process_node
```
# Run on docker
### Buiild docker image
```shell
docker build -f ./Dockerfile -t my_ros_pid:latest
```
### Run ros docker
```shell
docker run -v $(pwd):$(pwd) -name ros_pid
```
###  Change bash into docker
```angular2html
docker exec ros_pid -it /bin/bash
```
### Run driver node
```shell
ros2 run driver driver
```
### Run process node
```shell
ros2 run process process_node
```