from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import (
    RegisterEventHandler,
    ExecuteProcess,
    DeclareLaunchArgument,
    TimerAction,
    EmitEvent
)
from launch.event_handlers import OnProcessStart, OnProcessExit
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    bt_executor_params = PathJoinSubstitution([
        FindPackageShare('semantic_reasoning_bringup'),
        'launch',
        'cfg',
        'params.yaml'
    ])

    target_tree = LaunchConfiguration('target_tree')

    target_tree_arg = DeclareLaunchArgument(
        'target_tree',
        default_value='SRBT2',
        description='Behavior tree name'
    )

    bt_executor = Node(
        package="bt_executor2",
        executable="bt_executor2",
        name="bt_executor2",
        output="screen",
        emulate_tty=True,
        parameters=[bt_executor_params],
    )

    send_goal_cmd = ExecuteProcess(
        cmd=[
            'ros2', 'action', 'send_goal',
            '/robot/executor/execute_behavior',
            'btcpp_ros2_interfaces/action/ExecuteTree',
            ['\"{target_tree: \'', target_tree, '\'}\"']
        ],
        shell=True,
        output='screen'
    )

    delayed_send_goal = TimerAction(
        period=2.0,
        actions=[send_goal_cmd],
    )

    trigger_after_start = RegisterEventHandler(
        OnProcessStart(
            target_action=bt_executor,
            on_start=[delayed_send_goal],
        )
    )

    # When send_goal finishes -> shutdown everything
    shutdown_on_goal_exit = RegisterEventHandler(
        OnProcessExit(
            target_action=send_goal_cmd,
            on_exit=[
                TimerAction(
                    period=1.0,
                    actions=[EmitEvent(event=Shutdown(reason='Behavior execution done'))]
                )
            ],
        )
    )

    return LaunchDescription([
        target_tree_arg,
        bt_executor,
        trigger_after_start,
        shutdown_on_goal_exit,
    ])

