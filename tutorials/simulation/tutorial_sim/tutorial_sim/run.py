#!/usr/bin/env python3

"""
Runner for the tutorial world.
"""

import os
import rclpy
import threading

from pyrobosim.core import WorldYamlLoader
from pyrobosim.gui import start_gui
from pyrobosim_ros.ros_interface import WorldROSWrapper
from ament_index_python.packages import get_package_share_directory


def create_ros_node():
    """Initializes ROS node"""
    rclpy.init()
    node = WorldROSWrapper(state_pub_rate=0.1, dynamics_rate=0.01)
    
    world_file = os.path.join(
        get_package_share_directory("tutorial_sim"),
        "worlds",
        "world.yaml",
    )
    world = WorldYamlLoader().from_file(world_file)
    # world.reset(seed=0)
    world.reset()  # This randomizes the world.
    node.set_world(world)

    return node


def main():
    node = create_ros_node()

    # Start ROS node in separate thread
    ros_thread = threading.Thread(target=lambda: node.start(wait_for_gui=True))
    ros_thread.start()

    # Start GUI in main thread
    start_gui(node.world)


if __name__ == "__main__":
    main()
