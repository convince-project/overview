#pragma once

#include <behaviortree_ros2/bt_action_node.hpp>
#include <pyrobosim_msgs/action/detect_objects.hpp>
#include <rclcpp_action/rclcpp_action.hpp>

namespace BT
{

class DetectObject : public RosActionNode<pyrobosim_msgs::action::DetectObjects>
{
public:
  DetectObject(
    const std::string & name, const NodeConfig & conf,
    const RosNodeParams & params)
  : RosActionNode<pyrobosim_msgs::action::DetectObjects>(name, conf, params)
  {}

  // specify the ports offered by this node
  static BT::PortsList providedPorts()
  {
    return ExecuteTaskNode::appendProvidedPorts({BT::OutputPort<std::string>(
                 "object_id")});
  }

  // Implement the method that sends the goal
  bool setGoal(Goal & goal) override
  {
    return true;
  }

  // Implement the method that processes the result
  BT::NodeStatus onResultReceived(const WrappedResult & w_result) override
  {
    if (w_result.code == rclcpp_action::ResultCode::SUCCEEDED) {
      setOutput("object_id", w_result.result->detected_objects[0].name);
      return BT::NodeStatus::SUCCESS;
    } else {
      return BT::NodeStatus::FAILURE;
    }
  }

};

}  // namespace BT
