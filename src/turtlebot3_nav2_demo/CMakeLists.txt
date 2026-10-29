cmake_minimum_required(VERSION 3.8)
project(turtlebot3_nav2_demo)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch config maps worlds urdf meshes models
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
