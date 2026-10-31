# TurtleBot3 Warehouse Navigation

A ROS 2 Jazzy simulation project for a TurtleBot3 Waffle navigating a warehouse world in Gazebo Sim. It includes the warehouse worlds, a single Gazebo-to-ROS bridge, the official `warehouse_fresh` map, Nav2 with AMCL, and a saved RViz layout.

## Tested environment

- Ubuntu 24.04.5 LTS
- ROS 2 Jazzy
- Gazebo Sim 8.15.0 (Harmonic)
- TurtleBot3 Waffle model

## Install dependencies

```bash
sudo apt update
sudo apt install python3-colcon-common-extensions \
  ros-jazzy-navigation2 ros-jazzy-nav2-bringup \
  ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-gazebo \
  ros-jazzy-turtlebot3-msgs ros-jazzy-turtlebot3-teleop \
  ros-jazzy-slam-toolbox ros-jazzy-ros-gz
```

## Build

From the repository root:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
```

## Start the warehouse navigation demo

With the workspace built and sourced, run this one command:

```bash
ros2 launch tb3_nav_demo bringup.launch.py
```

The default world is `mapping_world`; RViz starts by default. To choose the other included world or omit RViz:

```bash
ros2 launch tb3_nav_demo bringup.launch.py world:=dynamic_navigation_world rviz:=false
```

## Send a navigation goal

In RViz, wait for the Navigation and Localization indicators to become active. Select **Nav2 Goal** in the top toolbar, then click and drag on a clear location in the map to set the target position and heading. The Navigation 2 panel shows goal feedback and completion state.

## Optional mission scripts

This repository currently contains no `delivery_mission.py` or `obstacle_sweep.py` scripts. Add one before using a corresponding mission command.

## Architecture

- `tb3_dynamic_world` starts Gazebo, spawns one Waffle, starts `robot_state_publisher`, and runs the single `ros_gz_bridge` instance.
- The bridge owns `/clock` and Gazebo odometry TF (`odom -> base_footprint`). `robot_state_publisher` publishes the robot link and sensor transforms.
- Nav2 bringup starts AMCL; AMCL owns `map -> odom` and initializes the robot at `(0, 0, 0)` in `map`.
- The navigation configuration uses `/scan` and `/odom`. No EKF or `robot_localization` node is configured.

## Troubleshooting

- **Gazebo reports that a server or GUI is already running:** check for stale `gz sim` processes from an earlier launch and stop that launch before starting another.
- **More than one `/clock` publisher appears:** check for a second bridge or an old simulation process. This bringup starts one bridge.
- **TF lookup errors or missing transforms:** confirm that `/clock`, `/scan`, `/odom`, `/tf`, and `/tf_static` are active; use `ros2 run tf2_tools view_frames` to inspect the frame tree. Allow a few seconds for simulation and lifecycle startup.
- **Robot does not localize:** ensure the official map is loaded, the robot is in the mapped room, and RViz uses the `map` fixed frame with `/scan` visible.

## Repository tree

```text
antropi_tb3_warehouse_nav/
├── docs/
│   ├── demo/README.md
│   └── FORM_NOTES.md
├── src/
│   ├── tb3_dynamic_world/
│   │   ├── config/waffle_bridge.yaml
│   │   ├── launch/
│   │   ├── worlds/
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   └── tb3_nav_demo/
│       ├── config/nav2_params.yaml
│       ├── launch/bringup.launch.py
│       ├── maps/warehouse_fresh.{yaml,pgm}
│       ├── resource/
│       ├── rviz/nav2_warehouse.rviz
│       ├── tb3_nav_demo/
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
├── .gitignore
└── README.md
```

## Demo video

[Demo video placeholder](docs/demo/)

## Future work

EKF sensor fusion.
