from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():

    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")

    robot_description = ParameterValue(
        Command([
            "ros2 run xacro xacro ",
            "src/mcrae_description/urdf/mcrae.urdf.xacro"
        ]),
        value_type=str
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_ros_gz_sim,
                "launch",
                "gz_sim.launch.py"
            )
        ),
        launch_arguments={
            "gz_args": "-r empty.sdf"
        }.items()
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description
            }
        ]
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            "mcrae",
            "-z",
            "0.1"
        ],
        output="screen"
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot
    ])