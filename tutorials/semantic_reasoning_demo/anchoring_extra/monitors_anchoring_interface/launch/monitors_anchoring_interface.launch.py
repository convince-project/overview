from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

share_dir = get_package_share_directory('monitors_anchoring_interface')

def generate_launch_description():

  # Create and declare entities
  monitors_anchoring_interface_node = Node(
    name='monitors_anchoring_interface',
    package='monitors_anchoring_interface', executable='run',
    namespace='',
    remappings=[
		],
    parameters=[share_dir+'/launch/cfg/params.yaml'],
    output='screen',
    emulate_tty=True  # assure that RCLCPP output gets flushed
  )

  # Launch Description
  ld = LaunchDescription()
  ld.add_entity(monitors_anchoring_interface_node)

  return ld
