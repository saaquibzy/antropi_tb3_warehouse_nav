# TurtleBot3 Waffle Warehouse Navigation (Gazebo Harmonic + Nav2)

Autonomous navigation of a TurtleBot3 Waffle in a custom 10 x 8 m warehouse
simulated in Gazebo Harmonic, using ROS 2 Jazzy, Nav2 and AMCL on a map built
with SLAM Toolbox. The whole system starts from a single launch command.

Built for the Antropi Robotics Software Intern assignment.

**Demo video:** TBD (link will be added here)

## Features

- Custom warehouse world: walls, four shelves, static obstacles, dock and goal markers
- Optional world variant with two controllable dynamic obstacles
- Map built once with SLAM Toolbox and saved in the repo (`warehouse_fresh`)
- Localization with AMCL on the saved map, initial pose set automatically
- Nav2 path planning and obstacle avoidance (costmaps, planner, controller)
- One-command bringup: Gazebo, robot, bridge, Nav2, AMCL and RViz

## Tested environment

| Item | Version |
|---|---|
| OS | Ubuntu 24.04 |
| ROS 2 | Jazzy |
| Simulator | Gazebo Sim 8 (Harmonic) |
| Robot | TurtleBot3 Waffle |
| Navigation | Nav2, AMCL, SLAM Toolbox |

## Install

```bash
sudo apt update
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup \
  ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-gazebo \
  ros-jazzy-slam-toolbox ros-jazzy-ros-gz python3-colcon-common-extensions
```

## Build

```bash
git clone https://github.com/saaquibzy/antropi_tb3_warehouse_nav.git
cd antropi_tb3_warehouse_nav
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
```

## Run

```bash
ros2 launch tb3_nav_demo bringup.launch.py
```

This starts Gazebo with the warehouse, spawns one Waffle at (-4.0, -2.8),
starts the ROS-Gazebo bridge, Nav2 with the saved map, AMCL, and RViz.
The initial pose is set automatically; wait for the particle cloud to converge
around the robot.

### Launch arguments

| Argument | Default | Meaning |
|---|---|---|
| `world` | `mapping_world` | `mapping_world` or `dynamic_navigation_world` |
| `rviz` | `true` | Start RViz with the saved config |
| `x_pose`, `y_pose` | `-4.0`, `-2.8` | Robot spawn position |

### Send a goal

1. In RViz, click **2D Goal Pose** in the toolbar.
2. Click a free spot on the map and drag to set the heading.
3. The planned path appears and the robot drives to the goal, avoiding obstacles.

## Architecture

```
Gazebo Harmonic -> ros_gz_bridge -> /scan, /odom, /imu, /joint_states, /clock, /tf
                                          |
                          map_server + AMCL (map -> odom)
                                          |
                                         Nav2
                                          |
                                      /cmd_vel -> Gazebo robot
```

Design rules that keep the system stable:

- **One `/clock` publisher:** the single `ros_gz_bridge` process.
- **One owner per transform:**
  - `odom -> base_footprint`: the Gazebo diff-drive plugin, via the bridge
  - fixed links (`base_link`, sensors, wheels): `robot_state_publisher`
  - `map -> odom`: AMCL during navigation (SLAM Toolbox during mapping, never both)
- **Original wheel odometry**; no sensor-fusion filter is used.
- `use_sim_time` is `true` for every node.

## Mapping (how the map was made)

The map in `src/tb3_nav_demo/maps/` was built once by running SLAM Toolbox
(online async) while driving the robot with keyboard teleop at about
0.1 to 0.15 m/s along every wall and around each shelf, then saved with
`nav2_map_server map_saver_cli`. It is 203 x 166 cells at 0.05 m/cell.

## Repository layout

```
src/
|-- tb3_dynamic_world/
|   |-- config/waffle_bridge.yaml
|   |-- launch/{world_robot,spawn_robot_no_bridge}.launch.py
|   `-- worlds/{mapping_world,dynamic_navigation_world}.sdf
`-- tb3_nav_demo/
    |-- config/nav2_params.yaml
    |-- launch/bringup.launch.py
    |-- maps/warehouse_fresh.{yaml,pgm}
    `-- rviz/nav2_warehouse.rviz
docs/
```

## Troubleshooting

- **Robot does not move or Nav2 will not activate:** check that there is exactly
  one `/clock` publisher: `ros2 topic info /clock --verbose`.
- **Transform errors:** inspect the tree with `ros2 run tf2_tools view_frames`.
  Each transform must have a single publisher.
- **Two robots or two worlds:** an old Gazebo is still running. Check
  `ps aux | grep -E "gz|rviz|parameter_bridge"` and stop the stale processes
  before relaunching.
- **Particles do not converge:** confirm the robot spawned at (-4.0, -2.8) with
  yaw 0, which matches the AMCL initial pose of (0, 0, 0) in the map frame.

## Future work

- EKF sensor fusion of wheel odometry and IMU (not implemented in this version)
- Warehouse delivery mission using Nav2 waypoint following
- Frontier-based autonomous exploration
- Driving the dynamic obstacles during a run to demonstrate live replanning
