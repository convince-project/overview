cmake_minimum_required(VERSION 3.5)
project(monitor)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(ament_index_cpp REQUIRED)
find_package(python_cmake_module REQUIRED)
find_package(PythonExtra MODULE)

ament_python_install_package(${PROJECT_NAME})
set(SCRIPTS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/scripts)
file(GLOB_RECURSE py_execs RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${SCRIPTS_DIRECTORY}/*)
install(PROGRAMS
  ${py_execs}
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})

ament_package()
