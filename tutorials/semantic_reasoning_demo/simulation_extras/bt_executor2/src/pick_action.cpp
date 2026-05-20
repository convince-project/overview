#include "pick_action.hpp"
#include "behaviortree_ros2/plugins.hpp"

bool PickAction::setGoal(RosActionNode::Goal& goal)
{
  auto object_id = getInput<unsigned>("object_id");
  goal.object_id = object_id.value();
  return true;
}

NodeStatus PickAction::onResultReceived(const RosActionNode::WrappedResult& wr)
{
  return NodeStatus::SUCCESS;
}

NodeStatus PickAction::onFailure(ActionNodeErrorCode error)
{
  RCLCPP_ERROR(logger(), "%s: onFailure with error: %s", name().c_str(), toStr(error));
  return NodeStatus::FAILURE;
}

void PickAction::onHalt()
{
  RCLCPP_INFO(logger(), "%s: onHalt", name().c_str());
}

// Plugin registration.
// The class PickAction will self register with name  "PickObject".
CreateRosNodePlugin(PickAction, "PickObject");
