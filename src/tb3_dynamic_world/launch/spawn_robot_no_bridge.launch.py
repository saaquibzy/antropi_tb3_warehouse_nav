import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    model = os.environ.get('TURTLEBOT3_MODEL', 'waffle')
    sdf = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'models',
                       f'turtlebot3_{model}', 'model.sdf')
    return LaunchDescription([
        DeclareLaunchArgument('x_pose', default_value='-4.0'),
        DeclareLaunchArgument('y_pose', default_value='-2.8'),
        Node(package='ros_gz_sim', executable='create', name='spawn_waffle',
             arguments=['-name', 'turtlebot3_waffle', '-file', sdf,
                        '-x', LaunchConfiguration('x_pose'),
                        '-y', LaunchConfiguration('y_pose'), '-z', '0.01'],
             output='screen'),
    ])
