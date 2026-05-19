#include "navigate_action.hpp"
#include "behaviortree_ros2/plugins.hpp"

bool NavigateAction::setGoal(RosActionNode::Goal& goal)
{
  auto location_id = getInput<std::string>("location_id");
  goal.location_id = location_id.value();
  return true;
}

NodeStatus NavigateAction::onResultReceived(const RosActionNode::WrappedResult& wr)
{
  return NodeStatus::SUCCESS;
}

NodeStatus NavigateAction::onFailure(ActionNodeErrorCode error)
{
  RCLCPP_ERROR(logger(), "%s: onFailure with error: %s", name().c_str(), toStr(error));
  return NodeStatus::FAILURE;
}

void NavigateAction::onHalt()
{
  RCLCPP_INFO(logger(), "%s: onHalt", name().c_str());
}

// Plugin registration.
// The class NavigateAction will self register with name  "NavigateToLocation".
CreateRosNodePlugin(NavigateAction, "NavigateToLocation");
