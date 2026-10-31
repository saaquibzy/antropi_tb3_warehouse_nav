# Form notes

- S0 confirmed Ubuntu 24.04.5, ROS 2 Jazzy, Gazebo Sim 8.15.0, and installed TurtleBot3/Nav2/SLAM Toolbox/ros_gz packages.
- The fresh workspace did not exist at audit time. The requested `/home/kyro/ros2_ws/src/warehouse_nav/maps/` directory was empty.
- During S0, Gazebo server PID 24587, Gazebo GUI PID 24588, and keyboard teleop PID 26620 were present; `ros2 node list` later showed no active ROS nodes. They have not been stopped.
- S1 created the two package skeletons, copied the static and dynamic warehouse worlds, and configured one bridge without EKF or robot_localization. Runtime topic/frame behavior still needs launch verification in the next stage.

- S2 startup: SLAM Toolbox online async activated with sim time. Startup warned its 20.0 m configured max lidar range exceeds the Waffle lidar's 3.5 m range; mapping is active, but the parameter should be aligned before relying on distant returns.
- S2 diagnostics: `ros2 topic echo /map --field` does not accept a composite field expression; using `--field info` returned map metadata. A custom `rclpy` probe incorrectly assumed subscription callbacks receive publisher metadata; it failed and did not affect ROS nodes.
- S2 TF check: `view_frames` shows `map -> odom` at about 10.2 Hz and `/map` has one publisher (`slam_toolbox`). `ros2 topic info /tf --verbose` lists two publisher endpoints under `/slam_toolbox`; exact per-transform endpoint attribution remains unverified.
- S2 final map saved as `src/tb3_nav_demo/maps/warehouse_fresh.{yaml,pgm}` after the user completed teleop. Both files were verified non-empty before SLAM Toolbox was stopped. Map is 203 x 166 cells at 0.05 m/cell; origin is [-1.130, -1.412, 0].
- PGM inspection: perimeter walls are closed and no large doubled/parallel edges are apparent. Four shelf footprints are outlined, but their interiors are mostly unknown gray rather than occupied black; there is minor isolated speckle near several obstacles.
- SLAM Toolbox stopped cleanly after map file verification; Gazebo and RViz were left running.
- S3 first Nav2 bringup: map_server remained unconfigured because the installed Jazzy Waffle params contained a node-specific `yaml_filename: map.yaml`, which took precedence over Nav2 bringup's `map:=warehouse_fresh.yaml` override. Removed that stale filename from the fresh params so the launch map argument supplies the official map.
- During S3 preparation, a broad textual replacement also changed `always_reset_initial_pose` unintentionally; corrected it to false and verified `set_initial_pose` remains true at x=0, y=0, yaw=0.

## Warehouse station coordinates

The saved map uses map = world + (4.0, 2.8), matching the robot's initial world pose (-4.0, -2.8) to map pose (0, 0).

| Station | World (x, y) | Map (x, y) |
|---|---:|---:|
| DOCK | (-3.8, 2.8) | (0.2, 5.6) |
| PICK_A | (-3.0, 2.8) | (1.0, 5.6) |
| PICK_B | (1.8, 0.8) | (5.8, 3.6) |
| PICK_C | (3.8, 0.0) | (7.8, 2.8) |
| PACK | (3.8, 3.2) | (7.8, 6.0) |

- S3 goal attempts: the first controlled DOCK command was preempted by another RViz goal; a retry was also aborted while additional RViz goals arrived. Nav2 logs include a separate goal success and one follow_path action-server timeout, so these are not counted as five controlled station tests.
