import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (AppendEnvironmentVariable, DeclareLaunchArgument,
                            IncludeLaunchDescription, OpaqueFunction, SetEnvironmentVariable)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _launch(context):
    pkg = get_package_share_directory('tb3_dynamic_world')
    gz_pkg = get_package_share_directory('ros_gz_sim')
    tb3_pkg = get_package_share_directory('turtlebot3_gazebo')
    world_name = LaunchConfiguration('world').perform(context)
    if world_name not in ('mapping_world', 'dynamic_navigation_world'):
        raise RuntimeError('world must be mapping_world or dynamic_navigation_world')
    world = os.path.join(pkg, 'worlds', world_name + '.sdf')
    bridge_config = os.path.join(pkg, 'config', 'waffle_bridge.yaml')
    return [
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'waffle'),
        AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.join(tb3_pkg, 'models')),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(gz_pkg, 'launch', 'gz_sim.launch.py')),
            launch_arguments={'gz_args': ['-r -v2 ', world], 'on_exit_shutdown': 'true'}.items()),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             name='robot_state_publisher', output='screen',
             parameters=[{'use_sim_time': True,
                          'robot_description': open(os.path.join(tb3_pkg, 'urdf',
                              'turtlebot3_waffle.urdf'), encoding='utf-8').read()}]),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg, 'launch', 'spawn_robot_no_bridge.launch.py')),
            launch_arguments={'x_pose': LaunchConfiguration('x_pose'),
                              'y_pose': LaunchConfiguration('y_pose')}.items()),
        Node(package='ros_gz_bridge', executable='parameter_bridge', name='ros_gz_bridge',
             arguments=['--ros-args', '-p', f'config_file:={bridge_config}'], output='screen'),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('world', default_value='mapping_world',
                              description='mapping_world or dynamic_navigation_world'),
        DeclareLaunchArgument('x_pose', default_value='-4.0'),
        DeclareLaunchArgument('y_pose', default_value='-2.8'),
        OpaqueFunction(function=_launch),
    ])
