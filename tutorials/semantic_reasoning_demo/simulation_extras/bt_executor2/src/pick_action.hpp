#include "behaviortree_ros2/bt_action_node.hpp"
#include "overarching_msgs/action/pick.hpp"

using namespace BT;

class PickAction : public RosActionNode<overarching_msgs::action::Pick>
{
public:
  PickAction(const std::string& name, const NodeConfig& conf,
              const RosNodeParams& params)
    : RosActionNode<overarching_msgs::action::Pick>(name, conf, params)
  {}

  static BT::PortsList providedPorts()
  {
    return providedBasicPorts({ InputPort<unsigned>("object_id") });
  }

  bool setGoal(Goal& goal) override;

  void onHalt() override;

  BT::NodeStatus onResultReceived(const WrappedResult& wr) override;

  virtual BT::NodeStatus onFailure(ActionNodeErrorCode error) override;
};
