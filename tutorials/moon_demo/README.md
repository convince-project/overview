# MOON Tutorial

## Introduction

This tutorial shows the application of MOON, the run-time verification tool, to the pick and place demo.
The objective is to show the complementarity of online monitoring and offline verification, by demonstrating the usefulness of monitoring in bridging the reality gap that stems from the models of the world.

## Tools usage

### Start the Docker container

For this tutorial, the provided Docker container in this repository is used:

```bash
cd overview
docker compose run --rm base /bin/bash
```

Multiple terminals (4 in total, thus 3 additional) are also needed; you can either use `tmux`, which is provided inside the container, or attach from the host system to the container just created by finding its name with `docker container list` and then
```bash
docker exec -it overview-base-run-<container-id> /bin/bash
```

### Generate the monitor

First we need to generate the monitors. This is achieved in two steps: at first, we generate the monitor configuration and the MTL property starting from the XML property pattern definition, which is found in the `roaml/properties` directory.
```xml
<properties>
  <ports>
    <ros_topic topic_name="object_loc" type="overarching_msgs/msg/Location" event="publish">
      <state_var id="x" field="x" type="float32" expr="100"/>
      <state_var id="y" field="y" type="float32" expr="100"/>
      <state_var id="parent" field="parent" type="string" expr="''"/>
    </ros_topic>
  </ports>

  <guarantees>
    <property id="snack_on_table" pattern="existence">
      <event>x &lt;= -3.0 &amp;&amp; y &lt;= -4.0 &amp;&amp; parent == 'kitchen_table_tabletop'</event>
      <scope type="globally"/>
      <time_interval time="15" time_unit="s"/>
    </property>
  </guarantees>

</properties>
```
The property checks that the object whose data is published on the `object_loc` topic is found eventually at its target location. It is the same property that is checked in the offline verification tutorial, albeit slightly different: as it is checked in real time, until the object reaches its correct location, the property would not be satisfied; thus there is the need of introducing a time out.

To generate the required files, run:
```bash
cd /MOON
moon_config --property-file /convince_ws/src/tutorials/roaml/properties/properties_moon.xml --monitor-workspace /convince_ws/src
```
This will generate a YAML file, containing the configuration of the monitor to be generated, and a Python file, containing the MTL property.

Now we generate the monitor ROS package:
```bash
moon_generator --config-file snack_on_table_monitor_config.yaml
```

Now we need to build the package:
```bash
cd /convince_ws
colcon build
```

### Check the property

Now we verify the property: this is the step where multiple terminals are needed.
First, we need to run the oracle server, which will receive the message of the monitor and provide the evaluation of the property.
```bash
cd /MOON
moon_oracle --dense --online --port 8080 --property snack_on_table.py
```
Then, we run the monitor in another terminal.
```bash
cd /convince_ws
source install/setup.bash
ros2 run monitor snack_on_table_monitor
```
The monitor should now be connected to the oracle and ready to intercept the messages.

We can then use a third terminal to check the monitor verdict more clearly.
```bash
ros2 topic echo /snack_on_table_monitor/monitor_verdict std_msgs/msg/String
```

Finally, in a fourth terminal we run the simulation tutorial:
```bash
ros2 launch tutorial_run full_simulation.launch.py policy:=bt_tree.xml
```
If the execution runs without errors, the monitor does not detect any violation, and the property is thus verified.

In order to repeat the execution, you must kill both oracle and monitor and execute them again.

#### Introducing reality gap

In order to simulate a shortcoming in the model of the system, a different world configuration has been provided, where the doors in the house are closed. This is not covered by offline verification, as it is not modeled in the world.

After running both oracle and monitor, we run the system with the new world configuration with
```bash
ros2 launch tutorial_run full_simulation.launch.py policy:=bt_tree.xml closed_doors_world:=true auto_shutdown:=false
```

You are going to see the robot fail to plan a path to the object, as the doors are closed, thus triggering the violation of the property after the defined timeout.
