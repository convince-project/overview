cmake_minimum_required(VERSION 3.5.0)
project(tutorial_homeservice)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(anchoring_process REQUIRED)

# Start of user code dependencies
# End of user code


# Install launch files.
install(DIRECTORY launch
	DESTINATION share/${PROJECT_NAME}/
)
ament_package()
