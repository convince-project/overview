cmake_minimum_required(VERSION 3.16)
project(bt_executor2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


find_package(ament_cmake REQUIRED)
find_package(behaviortree_ros2 REQUIRED)
find_package(overarching_msgs REQUIRED)

set(THIS_PACKAGE_DEPS
    behaviortree_ros2::behaviortree_ros2
    ${overarching_msgs_TARGETS} )

######################################################
# Implem that uses and customizes the BtExecutionServer
add_executable(bt_executor2 src/bt_executor2.cpp)
target_link_libraries(bt_executor2 ${THIS_PACKAGE_DEPS})

######################################################
# Actions (Plugins)

add_library(pick_plugin SHARED src/pick_action.cpp)
target_compile_definitions(pick_plugin PRIVATE  BT_PLUGIN_EXPORT )
target_link_libraries(pick_plugin ${THIS_PACKAGE_DEPS})
add_library(place_plugin SHARED src/place_action.cpp)
target_compile_definitions(place_plugin PRIVATE  BT_PLUGIN_EXPORT )
target_link_libraries(place_plugin ${THIS_PACKAGE_DEPS})
add_library(navigate_plugin SHARED src/navigate_action.cpp)
target_compile_definitions(navigate_plugin PRIVATE  BT_PLUGIN_EXPORT )
target_link_libraries(navigate_plugin ${THIS_PACKAGE_DEPS})


######################################################
# INSTALL

install(TARGETS
  pick_plugin
  place_plugin
  navigate_plugin
  bt_executor2
  DESTINATION lib/${PROJECT_NAME}
  )

######################################################
# INSTALL plugins for other packages to load

install(TARGETS
  pick_plugin
  place_plugin
  navigate_plugin
  LIBRARY DESTINATION share/${PROJECT_NAME}/bt_plugins
  ARCHIVE DESTINATION share/${PROJECT_NAME}/bt_plugins
  RUNTIME DESTINATION share/${PROJECT_NAME}/bt_plugins
  )

######################################################
# INSTALL Behavior.xml's

install(DIRECTORY
    behavior_trees
    DESTINATION share/${PROJECT_NAME}/
    )

ament_export_dependencies(behaviortree_ros2 overarching_msgs)

ament_package()
