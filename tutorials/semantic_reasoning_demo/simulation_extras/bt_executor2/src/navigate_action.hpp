#include "behaviortree_ros2/bt_action_node.hpp"
#include "overarching_msgs/action/navigate.hpp"

using namespace BT;

class NavigateAction : public RosActionNode<overarching_msgs::action::Navigate>
{
public:
  NavigateAction(const std::string& name, const NodeConfig& conf,
              const RosNodeParams& params)
    : RosActionNode<overarching_msgs::action::Navigate>(name, conf, params)
  {}

  static BT::PortsList providedPorts()
  {
    return providedBasicPorts({ InputPort<std::string>("location_id") });
  }

  bool setGoal(Goal& goal) override;

  void onHalt() override;

  BT::NodeStatus onResultReceived(const WrappedResult& wr) override;

  virtual BT::NodeStatus onFailure(ActionNodeErrorCode error) override;
};
