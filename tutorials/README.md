# CONVINCE - Overarching tutorial

Within this folder, we are providing a tutorial to demonstrate the functionalities of the tools developed in the CONVINCE project.

In particular, we provide an exemplary environment (defined using both RoAML and PyRoboSim), and custom ROS interfaces used in this environment.

## Custom ROS interfaces

Those interfaces are used in the RoAML model for the communication between the BT plugins and the environment's model.
The are located in [ros_interfaces](ros_interfaces) and can be built using colcon:

```bash
cd ros_interfaces
source /opt/ros/<your-ros-distro>/setup.bash
colcon build
source install/setup.bash
cd ..
```

## Offline verification

The model for offline verification is located in the [roaml folder](roaml).

The instructions for generating a verifiable model using [AS2FM](https://github.com/convince-project/AS2FM) and verifying it using [SMC STORM](https://github.com/convince-project/smc_storm) and [SCAN](https://github.com/convince-project/scan) are provided in the [roaml folder's readme](roaml/README.md).

## Running the PyRoboSim simulation

The instructions for running the simulation in PyRoboSim can be found in the [simulation folder's readme](simulation/README.md).