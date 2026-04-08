#!/bin/bash
# Starts up the refine plan demo

SESSION=refine_plan_demo
POLICY_EXECUTOR_MODE=$1
MONGO_CONNECTION_STRING=$2


tmux -2 new-session -d -s $SESSION
tmux rename-window -t $SESSION 'pyrobosim'
tmux new-window -t $SESSION -n 'policy-executor'

tmux select-window -t $SESSION:pyrobosim
tmux send-keys "ros2 run tutorial_sim run --ros-args -p detect_succ_prob:=1.0" C-m

tmux select-window -t $SESSION:policy-executor
tmux send-keys "ros2 launch refine_plan_demo policy_executor.launch.py db_collection:=demo-$POLICY_EXECUTOR_MODE mode:=$POLICY_EXECUTOR_MODE db_connection_string:=$MONGO_CONNECTION_STRING" C-m