#pragma once

#include <algorithm>
#include <array>
#include <behaviortree_cpp/action_node.h>
#include <rclcpp/rclcpp.hpp>

namespace BT
{

class DecoratorGetNextLocation : public SyncActionNode
{
public:
  DecoratorGetNextLocation(const std::string& name, const NodeConfig& config,
                           rclcpp::Logger logger)
    : SyncActionNode(name, config), logger_(logger)
  {}

  static PortsList providedPorts()
  {
    return { OutputPort<std::string>("location", "The next location to visit.") };
  }

  NodeStatus tick() override
  {
    // Use location names that are valid in the tutorial_sim world model.
    static const std::array<std::string, 4> kSearchLocations = {
        "fridge", "table", "kitchen_table", "dining_table"};

    int search_index = 0;
    const bool has_search_index = config().blackboard->get("@next_location_idx", search_index);
    if(!has_search_index)
    {
      // On first tick, start from the BT-selected current location if available.
      std::string current_location;
      if(config().blackboard->get("@current_location", current_location))
      {
        const auto it = std::find(kSearchLocations.begin(), kSearchLocations.end(), current_location);
        if(it != kSearchLocations.end())
        {
          search_index = static_cast<int>(std::distance(kSearchLocations.begin(), it));
        }
      }
    }

    if(search_index < 0)
    {
      search_index = 0;
    }

    const int bounded_index = search_index % static_cast<int>(kSearchLocations.size());
    const std::string& next_location = kSearchLocations[bounded_index];

    config().blackboard->set("@next_location_idx",
                             (bounded_index + 1) % static_cast<int>(kSearchLocations.size()));

    setOutput("location", next_location);
    RCLCPP_INFO(logger_, "Next search location: %s", next_location.c_str());
    return NodeStatus::SUCCESS;
  }

private:
  rclcpp::Logger logger_;
};

}  // namespace BT
