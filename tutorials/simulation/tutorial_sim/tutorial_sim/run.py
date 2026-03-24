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
    node = WorldROSWrapper(state_pub_rate=5.0, dynamics_rate=0.01)
    
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


def _reset_world_and_planners(node) -> None:
    """Best-effort reset of world and planners before process exit."""
    world = getattr(node, "world", None)
    if world is None:
        return

    try:
        world.reset()
    except Exception as exc:
        print(f"[tutorial_sim] world reset failed during shutdown: {exc}")

    robots = getattr(world, "robots", [])
    if isinstance(robots, dict):
        robots = robots.values()

    for robot in robots:
        planner = getattr(robot, "path_planner", None)
        if planner is not None and hasattr(planner, "reset"):
            try:
                planner.reset()
            except Exception as exc:
                print(f"[tutorial_sim] planner reset failed during shutdown: {exc}")


def _shutdown_ros_node(node) -> None:
    """Stop ROS wrapper cleanly if the wrapper exposes stop/shutdown hooks."""
    for method_name in ("shutdown", "stop", "destroy_node"):
        method = getattr(node, method_name, None)
        if callable(method):
            try:
                method()
            except Exception as exc:
                print(f"[tutorial_sim] {method_name} failed during shutdown: {exc}")


def main():
    node = create_ros_node()

    # Start ROS node in separate thread
    ros_thread = threading.Thread(target=lambda: node.start(wait_for_gui=True))
    ros_thread.start()

    try:
        # Start GUI in main thread
        start_gui(node.world)
    except KeyboardInterrupt:
        pass
    finally:
        _reset_world_and_planners(node)
        _shutdown_ros_node(node)
        if rclpy.ok():
            rclpy.shutdown()

        # Avoid hanging on exit if ROS thread is still unwinding.
        ros_thread.join(timeout=2.0)


if __name__ == "__main__":
    main()
