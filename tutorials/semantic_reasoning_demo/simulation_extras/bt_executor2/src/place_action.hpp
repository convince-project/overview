#include "behaviortree_ros2/bt_action_node.hpp"
#include "overarching_msgs/action/place.hpp"

using namespace BT;

class PlaceAction : public RosActionNode<overarching_msgs::action::Place>
{
public:
  PlaceAction(const std::string& name, const NodeConfig& conf,
              const RosNodeParams& params)
    : RosActionNode<overarching_msgs::action::Place>(name, conf, params)
  {}

  static BT::PortsList providedPorts()
  {
    return providedBasicPorts({});
  }

  bool setGoal(Goal& goal) override;

  void onHalt() override;

  BT::NodeStatus onResultReceived(const WrappedResult& wr) override;

  virtual BT::NodeStatus onFailure(ActionNodeErrorCode error) override;
};
