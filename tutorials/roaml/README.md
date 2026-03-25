# Offline Verification

## Introduction

This folder contains increasingly complex RoAML models for the overarching tutorial.

Each RoAML model consists of an entry xml file (e.g. [main.xml](main.xml)), that in turns references to one or more ASCXML models (e.g. representing the environment, ROS nodes, or other executables), a BT policy and the models of the custom BT plugins (if any).

### Environments

For this tutorial, we prepared three environments, of increasing complexity. All models of the environment can be found in the [environment folder](environment).
- [world.ascxml](environment/world.ascxml): A simple, deterministic environment, with a single location where the robot can navigate and pick the object.
- [world_multiple_locations.ascxml](environment/world_multiple_locations.ascxml): Extends the basic environment by introducing multiple locations that the robot must navigate to find the object. All actions are deterministically successful.
- [world_multiple_locations_w_failures.ascxml](environment/world_multiple_locations_w_failures.ascxml): Builds on the multiple locations scenario by adding probabilistic failure modes and fault conditions that the system must handle.

### Policies

We developed different policies, to handle the increasingly hard environment the robot must deal with.
All policies are collected in the [policy folder](policy).

### BT Plugins

Finally, we developed a number of BT Plugins, to be used by the policies we implemented. They can be found in the [bt_plugins folder](bt_plugins).

## Tools usage

### Get the verifiable model by using AS2FM

This section contains general instructions for generating a verifiable model starting from a RoAML xml file.

For these instructions, let's assume we want to generate the model starting from the [main.xml file](main.xml).

To do that, the first step is to source the required ROS interfaces (located in the [ros_interfaces folder](../ros_interfaces)):

Assuming we are in the `roaml` folder, and the interface were already built, run the following:

```bash
source ../ros_interfaces/install/setup.bash
```

Now that the ROS interfaces are sourced, we are ready to generate the verifiable models.

The JANI model, required by SMC Storm, can be obtained by running:
```bash
as2fm_roaml_to_jani main.xml --jani-out-file main.jani
```
This commands generates a single file, `main.jani`, containing the complete model of the system and the properties to verify on it.

The SCXML models, required by SCAN, can be obtained by running:
```bash
as2fm_roaml_to_jani main.xml --scxml-out-dir scxml
```
This commands generates a folder with several SCXML files, that can be loaded and executed by SCAN for property verification.

#### Quick run guide (tested commands)

To avoid environment/path issues, use the commands below exactly as shown.

From the repository root:

```bash
cd examples/overarching_tutorial/roaml
source ../ros_interfaces/install/setup.bash
```

Generate SCXML models for SCAN:

```bash
as2fm_roaml_to_jani main.xml --scxml-out-dir new_folder
```

Generate JANI model for SMC Storm:

```bash
as2fm_roaml_to_jani main.xml --jani-out-file main.jani
```

You can replace `main.xml` with any other entry model in this folder, for example:

```bash
as2fm_roaml_to_jani main_locations.xml --scxml-out-dir scxml_main_locations
as2fm_roaml_to_jani main_locations_w_failures.xml --jani-out-file main_locations_w_failures.jani
```

### Verify the JANI model using SMC_STORM

Once we have a JANI model of the system, we can use SMC Storm to verify properties on it.

In particular, for this model we developed the property `snack_at_start`, already present in the JANI file, that reads as follows:
```
F((topic_object_loc_msg__ros_fields__x = 0) & ((topic_object_loc_msg__ros_fields__y = 0) & (topic_object_loc_msg__ros_fields__parent = 'world')))
```
and checks that, eventually, the snack object reaches the table (location (0, 0)).

We can verify this property using SMC Storm with the following command:

```bash
smc_storm --model main.jani --properties-names snack_at_start --disable-explored-states-caching --n-threads 10 --show-statistics --batch-size 5 --traces-folder smc_storm_traces
```

#### Introspect CSV traces using PlotJuggles

In order to visualize what is happening, we can use PlotJuggler to visualize the generated traces.

PlotJuggler can be started using the command:
```bash
ros2 run plotjuggler plotjuggler -d smc_storm_traces/trace_<id>.csv
```

Afterwards, topics can be plotted to see their evolution along the trace.

### Verify the SCXML model using SCAN

TODO

## The tutorial

This section guide you through the different RoAML models, and describe what can be done using verification.

### Part 1: the simple world

For this part, we refer to the [main.xml file](main.xml).

To be able to operate in this world, we need a simple BT Sequence, as the one described in [this BT](policy/bt_tree.xml).

We can verify the property using SMC Storm (or SCAN), and see that it results in the property being always verified (Result = 1.0), meaning that the object always ends up in the desired location.

### Part 2: the world with multiple locations

For this part, we refer to the [main_locations.xml file](main_locations.xml).

In this scenario, the world becomes more complex: the object now spawns each time in a different location. This means the robot can no longer rely on a simple sequence: it must visit multiple locations until it finds the object.

To handle this, we developed a new BT policy described in [bt_tree_locations.xml](policy/bt_tree_locations.xml), which uses a `RetryUntilSuccessful` node that iterates through locations until the object is detected. The key to this approach is the introduction of a new BT Plugin called `GetNextLocation` (see [get_next_location.ascxml](bt_plugins/get_next_location.ascxml)).

The GetNextLocation plugin maintains an internal counter and returns a different location each time it is called, cycling through: `table`, `fridge`, `bin`, and finally back to `start`. This allows the robot to systematically search each location in turn.

Even with this increased complexity and non-determinism in object placement, the actions from the robot in the world succeed deterministically.
For this reason, the result from verifying the property using SMC Storm (or SCAN) still holds with Result = 1.0, meaning that the object always ends up in the desired location regardless of where it initially spawns.

### Part 3: The world with multiple locations and failures

In this final part, we introduce the most challenging scenario: a world where the robot's actions can fail probabilistically. The environment model [world_multiple_locations_w_failures.ascxml](environment/world_multiple_locations_w_failures.ascxml) introduces failure modes for navigation (10% failure rate), object detection (20% failure rate), and object picking (20% failure rate). This reflects real-world conditions where sensors, actuators, and planning algorithms don't always succeed on the first attempt.

#### Part 3.1: Unhandled failures

We first examine what happens when we use the policy from Part 2 in this failure-prone environment. This configuration is captured in [main_locations_failures_unhandled.xml](main_locations_failures_unhandled.xml), which combines the [bt_tree_locations.xml](policy/bt_tree_locations.xml) policy with the probabilistic failure environment.

Since the policy from Part 2 was designed for a deterministic world, it lacks proper failure handling mechanisms. The `RetryUntilSuccessful` node is configured with only 3 attempts to find the object across locations, and there are no retries for individual actions like navigation, detection, or picking.

When we verify the property using SMC Storm (or SCAN) on this model, we observe that the property verification fails in most cases (Result 0.25), describing that the robot fails to complete its task 75% of the times.

#### Part 3.2: Handling failures with retries

To address the failures, we developed a more robust BT policy: [bt_tree_locations_handle_failures.xml](policy/bt_tree_locations_handle_failures.xml). This policy is used in the [main_locations_w_failures.xml](main_locations_w_failures.xml) model.

The new policy introduces multiple layers of retry logic to handle probabilistic failures:
- **Navigation retries**: Each `NavigateToLocation` action is wrapped in a `RetryUntilSuccessful` node with 4 attempts, handling the 10% navigation failure rate
- **Detection retries**: The `DetectObject` action has 3 retry attempts to overcome the 20% detection failure rate
- **Pick retries**: The `PickObject` action also gets 3 retry attempts to handle the 20% pick failure rate
- **Location search loop**: The `Repeat` node with 3 cycles ensures the robot can iterate through multiple locations even if some attempts fail

This layered retry strategy significantly improves the robot's resilience. When we verify the property using SMC Storm (or SCAN), we see that despite the probabilistic failures in the environment, the property holds with a much higher success rate (Result 0.98), demonstrating that proper failure handling in the BT policy enables the robot to reliably complete its task even in uncertain conditions.
