from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    pkg_share = get_package_share_directory("mcrae_description")

    controller_config = os.path.join(
        pkg_share,
        "config",
        "diff_drive_controller.yaml"
    )

    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--param-file",
            controller_config
        ],
        output="screen"
    )

    diff_drive_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diff_drive_controller",
            "--param-file",
            controller_config
        ],
        output="screen"
    )

    return LaunchDescription([

        joint_state_broadcaster,

        RegisterEventHandler(
            OnProcessExit(
                target_action=joint_state_broadcaster,
                on_exit=[
                    diff_drive_controller
                ]
            )
        )

    ])