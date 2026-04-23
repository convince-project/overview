from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, EmitEvent, RegisterEventHandler, TimerAction
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    policy_dir = DeclareLaunchArgument(
        "policy_dir",
        default_value="/convince_ws/src/tutorials/roaml/policy/",
        description="The folder where to load the policy from."
    )

    policy_name = DeclareLaunchArgument(
        "policy",
        default_value="bt_tree.xml",
        description="Behavior tree file path passed to bt_executor",
    )

    headless_arg = DeclareLaunchArgument(
        "headless",
        default_value="false",
        description="Start pyrobosim without GUI",
    )

    world_file = DeclareLaunchArgument(
        "world",
        default_value="world.yaml",
        description="Choose the world file",
    )

    auto_shutdown = DeclareLaunchArgument(
        'auto_shutdown',
        default_value='true',
        description='Enables automatic shutdown when bt_executor ends',
    )

    simulator = Node(
        package="tutorial_sim",
        executable="run",
        name="tutorial_sim",
        output="screen",
        emulate_tty=True,
        parameters=[
            {"headless": LaunchConfiguration("headless")},
            {"world": LaunchConfiguration("world")},
        ],
    )

    translator = Node(
        package="tutorial_sim",
        executable="translate_component",
        name="translate_component",
        output="screen",
        emulate_tty=True,
    )

    location_publisher = Node(
        package="tutorial_sim",
        executable="object_location_publisher",
        name="object_location_publisher",
        output="screen",
        emulate_tty=True,
    )

    place_object_skill = Node(
        package="place_object_skill",
        executable="place_object_skill",
        name="place_object_skill",
        output="screen",
        emulate_tty=True,
    )

    bt_executor = Node(
        package="bt_executor",
        executable="btcpp_executor",
        name="btcpp_executor",
        output="screen",
        emulate_tty=True,
        parameters=[{"tree": PathJoinSubstitution(
            [LaunchConfiguration("policy_dir"), LaunchConfiguration("policy")]
        )}],
        # prefix=['xterm -e gdb -ex=run --args'],
        # prefix=['gdbserver localhost:3000']
    )

    # Add a delay of 3 seconds, to make sure the launch test can catch the end state in time.
    shutdown_on_bt_exit = RegisterEventHandler(
        OnProcessExit(
            target_action=bt_executor,
            on_exit=[
                TimerAction(
                    period=3.0,
                    condition = IfCondition(
                        PythonExpression(["'", LaunchConfiguration('auto_shutdown'), "' == 'true'"])
                    ),
                    actions=[EmitEvent(event=Shutdown(reason="btcpp_executor finished"))]
                )],
        )
    )

    return LaunchDescription(
        [
            policy_dir,
            policy_name,
            headless_arg,
            world_file,
            auto_shutdown,
            simulator,
            translator,
            location_publisher,
            place_object_skill,
            bt_executor,
            shutdown_on_bt_exit,
        ]
    )