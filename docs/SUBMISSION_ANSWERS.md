# Submission answers

## Approach
I set up a TurtleBot3 Waffle in a custom 10 x 8 m warehouse (walls, four shelves,
static obstacles, dock and goal markers) in Gazebo Harmonic on ROS 2 Jazzy.
I mapped the world once with SLAM Toolbox using keyboard teleop, saved the map,
then ran Nav2 with map_server and AMCL on that saved map. A single launch file
(ros2 launch tb3_nav_demo bringup.launch.py) starts Gazebo, the robot, one
ros_gz bridge, Nav2, AMCL and RViz, with the initial pose set automatically.
I used existing packages only and kept the original wheel odometry.

## Challenges
- Duplicate publishers: competing /clock publishers and a second bridge caused
  timing and TF problems. I fixed it with one bridge process and one owner per
  transform (bridge: odom->base_footprint, robot_state_publisher: fixed links,
  AMCL: map->odom).
- Stale processes: leftover Gazebo and RViz sessions gave duplicate worlds and
  clocks, so I checked running processes before every launch.
- A mapping session was lost because the map was never saved, so I switched to
  checkpoint saves and verified the files before shutting SLAM down.
- Localization drift in one recording: the laptop was in Power Saver mode, which
  likely slowed the simulation. I switched power mode, checked the scan against
  the map walls and re-recorded.
- Gazebo Harmonic's launcher sometimes hangs on Ctrl+C, so I stop leftover
  processes by exact PID.

## Learnings
- How SLAM Toolbox (mapping) and AMCL (localization on a saved map) divide work.
- Why every TF transform needs exactly one publisher.
- Nav2 lifecycle startup, costmap and inflation tuning.
- Verifying behaviour with evidence (topic rates, publisher counts, saved files)
  instead of assuming a running node means a working system.

## Next steps
- EKF fusion of wheel odometry and IMU (not implemented in this version).
- A warehouse delivery mission using Nav2 waypoint following.
- Frontier-based autonomous exploration.
