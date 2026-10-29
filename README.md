# TurtleBot3 Nav2 Navigation Demo

This ROS 2 Jazzy project runs a TurtleBot3 Waffle in a closed, square maze with nine 2 m cells. In SLAM mode it starts `explore_lite` frontier exploration, which sends Nav2 goals to map the maze autonomously.

## Requirements

- Ubuntu 24.04 with ROS 2 Jazzy
- Gazebo Sim and the ROS-Gazebo bridge
- Nav2, TurtleBot3 simulation assets, RViz, and `colcon`
- Frontier exploration sources (`explore_lite` and `explore_lite_msgs`) are included under `src/` from the ROS 2 m-explore port

Install the ROS packages if they are not already present:

```bash
sudo apt update
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup \
  ros-jazzy-nav2-minimal-tb3-sim ros-jazzy-robot-state-publisher \
  ros-jazzy-xacro python3-colcon-common-extensions
```

## Build

From this repository root:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --base-paths src
source install/setup.bash
```

## Run the navigation demo

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch turtlebot3_nav2_demo demo.launch.py
```

Gazebo and RViz open with the Waffle inside the closed maze. The launch loads the matching saved map, starts AMCL with the center spawn pose, and autostarts Nav2. In RViz, use **Nav2 Goal** to choose a reachable point in an open cell. Use **2D Pose Estimate** if localization is visibly off.

For headless simulation:

```bash
ros2 launch turtlebot3_nav2_demo demo.launch.py headless:=True use_rviz:=False
```

## Create or update the map

Start SLAM instead of loading the saved map:

```bash
ros2 launch turtlebot3_nav2_demo demo.launch.py slam:=True
```

Frontier exploration starts automatically in SLAM mode after Nav2 starts. To map manually instead, set `frontier_exploration:=False`. The frontier markers are published on `explore/frontiers`. After exploration finishes, save the map from another sourced terminal:

```bash
ros2 run nav2_map_server map_saver_cli -f src/turtlebot3_nav2_demo/maps/my_map
```

The frontier trial map saved in this project is `src/turtlebot3_nav2_demo/maps/maze_frontier.yaml`. To use it for localization, pass `map:=/absolute/path/to/maze_frontier.yaml` when launching without SLAM.

The Waffle spawns at the center of the maze (`x=0`, `y=0`). To use another map, pass its YAML path with `map:=/absolute/path/to/map.yaml` and set the robot's spawn and AMCL initial pose to matching coordinates in `config/nav2_params.yaml`.

## Project layout

- `src/turtlebot3_nav2_demo/launch/demo.launch.py` — Gazebo, Nav2, RViz, and corrected Waffle robot description
- `src/turtlebot3_nav2_demo/maps/` — occupancy map paired with the 3×3 maze
- `src/turtlebot3_nav2_demo/config/nav2_params.yaml` — Nav2 defaults plus the AMCL initial pose
- `src/turtlebot3_nav2_demo/config/explore_lite.yaml` — frontier selection and SLAM-time settings
- `src/turtlebot3_nav2_demo/worlds/` — Gazebo world with nine connected cells and a sealed perimeter
- `src/turtlebot3_nav2_demo/urdf/` and `meshes/` — RViz robot model and its mesh assets
- `src/explore_lite/` and `src/explore_lite_msgs/` — bundled ROS 2 frontier exploration packages

The frontier packages are from [robo-friends/m-explore-ros2](https://github.com/robo-friends/m-explore-ros2) and retain their BSD license in `src/THIRD_PARTY_LICENSE_m-explore-BSD.txt`. The simulated Waffle description comes from the ROS 2 Jazzy Nav2 TurtleBot3 simulation package. Mesh URIs in the RViz URDF point to this package's installed mesh files.

## Demo recording

Show Gazebo and RViz together for 1–2 minutes. In SLAM mode, capture the robot selecting frontiers and mapping the connected maze cells; optionally finish with a Nav2 goal and arrival feedback.
