from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    package_share = FindPackageShare("turtlebot3_nav2_demo")
    sim_share = FindPackageShare("nav2_minimal_tb3_sim")
    bringup_share = FindPackageShare("nav2_bringup")

    default_world = PathJoinSubstitution(
        [package_share, "worlds", "tb3_sandbox.sdf.xacro"]
    )
    default_map = PathJoinSubstitution(
        [package_share, "maps", "tb3_sandbox.yaml"]
    )
    default_params = PathJoinSubstitution(
        [package_share, "config", "nav2_params.yaml"]
    )
    explore_params = PathJoinSubstitution(
        [package_share, "config", "explore_lite.yaml"]
    )
    default_rviz_config = PathJoinSubstitution(
        [package_share, "config", "maze_view.rviz"]
    )
    robot_description_file = PathJoinSubstitution(
        [package_share, "urdf", "turtlebot3_waffle.urdf"]
    )
    robot_sdf = PathJoinSubstitution(
        [sim_share, "urdf", "gz_waffle.sdf.xacro"]
    )
    nav2_simulation = PathJoinSubstitution(
        [bringup_share, "launch", "tb3_simulation_launch.py"]
    )

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_simulation),
        launch_arguments={
            "slam": LaunchConfiguration("slam"),
            "map": LaunchConfiguration("map"),
            "params_file": LaunchConfiguration("params_file"),
            "world": LaunchConfiguration("world"),
            "robot_name": "turtlebot3_waffle",
            "robot_sdf": robot_sdf,
            "use_robot_state_pub": "False",
            "use_sim_time": "true",
            "use_rviz": LaunchConfiguration("use_rviz"),
            "rviz_config_file": LaunchConfiguration("rviz_config_file"),
            "headless": LaunchConfiguration("headless"),
            "autostart": "true",
            "use_composition": "False",
            "x_pose": LaunchConfiguration("x_pose"),
            "y_pose": LaunchConfiguration("y_pose"),
            "z_pose": "0.01",
            "yaw": LaunchConfiguration("yaw"),
        }.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "use_sim_time": True,
                "robot_description": ParameterValue(
                    Command(["cat ", robot_description_file]), value_type=str
                ),
            }
        ],
        remappings=[("/tf", "tf"), ("/tf_static", "tf_static")],
    )

    frontier_explorer = TimerAction(
        period=20.0,
        actions=[
            Node(
                package="explore_lite",
                executable="explore",
                name="explore",
                output="screen",
                parameters=[explore_params, {"use_sim_time": True}],
                remappings=[("map", "/map"), ("map_updates", "/map_updates")],
            )
        ],
        condition=IfCondition(
            PythonExpression(
                [
                    "'",
                    LaunchConfiguration("slam"),
                    "'.lower() == 'true' and '",
                    LaunchConfiguration("frontier_exploration"),
                    "'.lower() == 'true'",
                ]
            )
        ),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("world", default_value=default_world),
            DeclareLaunchArgument("map", default_value=default_map),
            DeclareLaunchArgument("params_file", default_value=default_params),
            DeclareLaunchArgument("slam", default_value="False"),
            DeclareLaunchArgument("frontier_exploration", default_value="True"),
            DeclareLaunchArgument("headless", default_value="False"),
            DeclareLaunchArgument("use_rviz", default_value="True"),
            DeclareLaunchArgument(
                "rviz_config_file", default_value=default_rviz_config
            ),
            DeclareLaunchArgument("x_pose", default_value="0.0"),
            DeclareLaunchArgument("y_pose", default_value="0.0"),
            DeclareLaunchArgument("yaw", default_value="0.0"),
            AppendEnvironmentVariable(
                "GZ_SIM_RESOURCE_PATH",
                PathJoinSubstitution([package_share, "models"]),
            ),
            simulation,
            robot_state_publisher,
            frontier_explorer,
        ]
    )
