#include <behaviortree_ros2/tree_execution_server.hpp>
#include <behaviortree_cpp/loggers/bt_cout_logger.h>
#include <rclcpp/rclcpp.hpp>

class TreeExecutionServerWhStdCoutLogger : public BT::TreeExecutionServer
{
public:
  TreeExecutionServerWhStdCoutLogger(const rclcpp::NodeOptions& options)
    : TreeExecutionServer(options)
  {}

  void onTreeCreated(BT::Tree& tree) override
  {
    logger_cout_ = std::make_unique<BT::StdCoutLogger>(tree);
  }

  std::optional<std::string> onTreeExecutionCompleted(
      BT::NodeStatus /*status*/,
      bool /*was_cancelled*/) override
  {
    cleanup();
    return std::nullopt;
  }

  ~TreeExecutionServerWhStdCoutLogger()
  {
    cleanup();
  }

  void cleanup()
  {
    if (logger_cout_) {
      logger_cout_.reset();
    }
  }

private:
  std::unique_ptr<BT::StdCoutLogger> logger_cout_;
};

int main(int argc, char* argv[])
{
  rclcpp::init(argc, argv);

  rclcpp::NodeOptions options;
  auto action_server =
      std::make_shared<TreeExecutionServerWhStdCoutLogger>(options);

  // Executor (same as your original)
  rclcpp::executors::MultiThreadedExecutor exec(
      rclcpp::ExecutorOptions(), 0, false,
      std::chrono::milliseconds(250));

  exec.add_node(action_server->node());

  // shutdown hook
  rclcpp::on_shutdown([action_server]() {
    action_server->cleanup();
  });

  exec.spin();

  exec.remove_node(action_server->node());

  rclcpp::shutdown();
  return 0;
}
