from launch import LaunchDescription

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    demo_params = PathJoinSubstitution([
        FindPackageShare('tutorial_homeservice'),
        'launch',
        'cfg',
        'params.yaml'
    ])

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('anchoring_process'),
                    'launch',
                    'anchoring_process.launch.py'
                ])
            ),
            launch_arguments={
                'params_file': demo_params,
                'knowledge_domain': 'SkrawlMoMa',
                'instances_setup': '/tmp/dt/setup.json'
            }.items()
        )
    ])

