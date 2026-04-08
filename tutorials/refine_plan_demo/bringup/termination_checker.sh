#!/bin/bash
# Checks for termination and then ensures everything is killed properly

NODE=$(ros2 node list | grep /policy_executor)
while [ ! -z "${NODE}" ]
do 
    echo "Policy Executor still running..."
    sleep 5s
    NODE=$(ros2 node list | grep /policy_executor)
done

echo "Policy Executor Finished, Terminating." 
# Kill absolutely everything and be extra sure
tmux kill-server
pkill -9 ros

# Confirm that the node list is not empty
NODE_LIST=$(ros2 node list)
while [ ! -z "${NODE_LIST}" ]
do
    echo "Node List not empty yet..."
    sleep 5s
    NODE_LIST=$(ros2 node list)
done
echo "Node List Empty, one last sleep to be safe."
sleep 10s


