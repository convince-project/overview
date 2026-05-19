from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Declare launch argument for world file
    world_file_arg = DeclareLaunchArgument(
        'world_file',
        default_value=os.path.join(
            get_package_share_directory("tutorial_skill_executor"),
            "worlds",
            "world.yaml",
        ),
        description='Path to the world file for pyrobosim'
    )
    
    # Get the world file launch configuration
    world_file = LaunchConfiguration('world_file')
    
    # Include the pyrobosim_ros demo launch file
    pyrobosim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('pyrobosim_ros'),
                'launch',
                'demo.launch.py'
            ])
        ]),
        launch_arguments={
            'world_file': world_file
        }.items()
    )
    
    # Run the tutorial_skill_executor node in the default domain
    tutorial_skill_executor_node = Node(
        package='tutorial_skill_executor',
        executable='run',
        name='tutorial_skill_executor',
        output='screen'
    )
    
    return LaunchDescription([
        world_file_arg,
        pyrobosim_launch,
        tutorial_skill_executor_node
    ])
