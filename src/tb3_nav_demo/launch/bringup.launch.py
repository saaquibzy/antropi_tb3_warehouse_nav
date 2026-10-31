import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    dynamic_world_share = get_package_share_directory('tb3_dynamic_world')
    nav2_share = get_package_share_directory('nav2_bringup')
    demo_share = get_package_share_directory('tb3_nav_demo')

    world_launch = os.path.join(
        dynamic_world_share, 'launch', 'world_robot.launch.py')
    nav2_launch = os.path.join(
        nav2_share, 'launch', 'bringup_launch.py')
    map_yaml = os.path.join(demo_share, 'maps', 'warehouse_fresh.yaml')
    params_file = os.path.join(demo_share, 'config', 'nav2_params.yaml')
    rviz_config = os.path.join(demo_share, 'rviz', 'nav2_warehouse.rviz')

    world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(world_launch),
        launch_arguments={
            'world': LaunchConfiguration('world'),
        }.items(),
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_launch),
        launch_arguments={
            'map': map_yaml,
            'params_file': params_file,
            'use_sim_time': 'true',
            'autostart': 'true',
        }.items(),
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(LaunchConfiguration('rviz')),
        output='screen',
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world', default_value='mapping_world',
            description='Warehouse world: mapping_world or dynamic_navigation_world'),
        DeclareLaunchArgument(
            'rviz', default_value='true',
            description='Start RViz with the saved warehouse navigation config'),
        world,
        TimerAction(period=8.0, actions=[nav2]),
        TimerAction(period=13.0, actions=[rviz]),
    ])
