#!/usr/bin/env python3

"""
Integration test: checks that butter is placed on a table after the BT completes.

Run with:
    colcon test --packages-select tutorial_run
or inside the container:
    docker compose run base colcon test --packages-select tutorial_run
"""

import os
import threading
import time
import unittest

import launch
import launch_ros.actions
import launch_testing
import launch_testing.actions
import launch_testing.markers
import pytest

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from pyrobosim_msgs.srv import RequestWorldState


# Absolute path inside the Docker container where tutorials are mounted.
TREE_PATH = os.environ.get(
    "BT_TREE_PATH",
    "/convince_ws/src/tutorials/roaml/policy/bt_tree.xml",
)

# How long to poll the world state before declaring failure.
BT_TIMEOUT_SEC = 180

# Interval between world state polls.
POLL_INTERVAL_SEC = 2.0


@pytest.mark.launch_test
@launch_testing.markers.keep_alive
def generate_test_description():
    simulator = launch_ros.actions.Node(
        package="tutorial_sim",
        executable="run",
        name="tutorial_sim",
        output="screen",
        parameters=[{"headless": True}],
    )

    translator = launch_ros.actions.Node(
        package="tutorial_sim",
        executable="translate_component",
        name="translate_component",
        output="screen",
    )

    place_object_skill = launch_ros.actions.Node(
        package="place_object_skill",
        executable="place_object_skill",
        name="place_object_skill",
        output="screen",
    )

    bt_executor = launch_ros.actions.Node(
        package="bt_executor",
        executable="btcpp_executor",
        name="btcpp_executor",
        output="screen",
        parameters=[{"tree": TREE_PATH}],
    )

    return launch.LaunchDescription(
        [
            simulator,
            translator,
            place_object_skill,
            bt_executor,
            launch_testing.actions.ReadyToTest(),
        ]
    )


class TestButterPlacedOnTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = Node("test_butter_placed_on_table")
        cls._executor = SingleThreadedExecutor()
        cls._executor.add_node(cls.node)
        cls._spin_thread = threading.Thread(target=cls._executor.spin, daemon=True)
        cls._spin_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls._executor.shutdown(timeout_sec=2.0)
        cls.node.destroy_node()
        rclpy.shutdown()

    def _get_world_state(self):
        """Call /request_world_state and return the WorldState message, or None on failure."""
        client = self.node.create_client(RequestWorldState, "/request_world_state")
        if not client.wait_for_service(timeout_sec=5.0):
            return None
        future = client.call_async(RequestWorldState.Request())
        deadline = time.monotonic() + 5.0
        while not future.done():
            if time.monotonic() > deadline:
                return None
            time.sleep(0.05)
        return future.result().state

    def _butter_is_on_table(self, world_state):
        """Return True if every butter object's parent contains 'table'."""
        butter_objects = [o for o in world_state.objects if o.category == "butter"]
        if not butter_objects:
            return False
        return all("table" in o.parent for o in butter_objects)

    def test_butter_on_table(self, proc_output):
        deadline = time.monotonic() + BT_TIMEOUT_SEC
        while time.monotonic() < deadline:
            world_state = self._get_world_state()
            if world_state is not None and self._butter_is_on_table(world_state):
                print("Butter is on the table!")
                return  # test passes
            time.sleep(POLL_INTERVAL_SEC)

        # Final check with a failure message showing the last known state.
        world_state = self._get_world_state()
        self.assertIsNotNone(world_state, "/request_world_state service unavailable")
        self.assertTrue(
            self._butter_is_on_table(world_state),
            f"butter not on table after {BT_TIMEOUT_SEC}s;"
        )
