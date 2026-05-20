#include "place_action.hpp"
#include "behaviortree_ros2/plugins.hpp"

bool PlaceAction::setGoal(RosActionNode::Goal& goal)
{
  return true;
}

NodeStatus PlaceAction::onResultReceived(const RosActionNode::WrappedResult& wr)
{
  return NodeStatus::SUCCESS;
}

NodeStatus PlaceAction::onFailure(ActionNodeErrorCode error)
{
  RCLCPP_ERROR(logger(), "%s: onFailure with error: %s", name().c_str(), toStr(error));
  return NodeStatus::FAILURE;
}

void PlaceAction::onHalt()
{
  RCLCPP_INFO(logger(), "%s: onHalt", name().c_str());
}

// Plugin registration.
// The class PlaceAction will self register with name  "PlaceObject".
CreateRosNodePlugin(PlaceAction, "PlaceObject");
