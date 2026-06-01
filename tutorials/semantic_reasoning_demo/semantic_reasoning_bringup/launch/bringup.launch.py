from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    ExecuteProcess,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # simulated world, skill executor and its digital twin
    # ====================================================
    skill_executor_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('tutorial_skill_executor'),
                'launch',
                'tutorial_skill_executor.launch.py'
            ])
        ])
    )

    dt = Node(
        package="tutorial_dt",
        executable="run",
        name="tutorial_dt",
        output="screen",
        emulate_tty=True,
    )

    # moon
    # ====
    moon_oracle = ExecuteProcess(
        # moon_oracle --online --property /semantic_reasoning_demo/config/moon/place_test-prop1.py --port 8080 --dense
		    cmd = [
			    'moon_oracle',
			    '--online',
			    '--property',
			    '/convince_ws/src/tutorials/semantic_reasoning_demo/misc/moon/place_test-prop1.py',
			    '--port',
			    '8080',
			    '--dense'
			    ],
        shell=True,
        output='screen'
    )

    place_monitor = Node(
        package="monitor",
        executable="place_monitor",
        name="monitor",
        output="screen",
        emulate_tty=True,
    )

    monitor_anchoring_params = PathJoinSubstitution([
        FindPackageShare('monitors_anchoring_interface'),
        'launch',
        'cfg',
        'params.yaml'
    ])

    monitors_anchoring_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('monitors_anchoring_interface'),
                'launch',
                'monitors_anchoring_interface.launch.py'
            ])
        ),
        launch_arguments={
            'params_file': monitor_anchoring_params
        }.items()
    )

    # force-data inspection
    # =====================
    plotjuggler = ExecuteProcess(
        cmd = [
          'ros2',
          'run',
          'plotjuggler',
          'plotjuggler',
          '--nosplash',
          '--buffer_size',
          '999'
          ],
        shell=True,
        output='screen'
	  )

    # semantic anchoring and reasoner
    # ===============================
    anchoring_params = PathJoinSubstitution([
        FindPackageShare('tutorial_homeservice'),
        'launch',
        'cfg',
        'params.yaml'
    ])

    anchoring_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('anchoring_process'),
                'launch',
                'anchoring_process.launch.py'
            ])
        ),
        launch_arguments={
            'params_file': anchoring_params,
            'knowledge_domain': 'SkrawlMoMa',
            'instances_setup': '/convince_ws/src/tutorials/semantic_reasoning_demo/misc/anchoring/dt/setup.json'
        }.items()
    )

    return LaunchDescription(
        [
            skill_executor_launch,
            dt,
            moon_oracle,
            place_monitor,
            monitors_anchoring_launch,
            plotjuggler,
            anchoring_launch,
        ]
    )
