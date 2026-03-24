# tutorial_sim

## Place Translator Component

This package includes a ROS 2 bridge node that translates the tutorial `Place` action into the pyrobosim `ExecuteTaskAction`.

The input interface definition used by this node is the `Place.action` file in:
- `examples/overarching_tutorial/ros_interfaces/src/overarching_msgs/action/Place.action`

Implementation file:
- `tutorial_sim/translate_component.py`

Compatibility wrapper:
- `../component/translate_component.py`

### What it does

The translator exposes an action server for:
- Input action: `/PlaceComponet/Place`
- Input type: `overarching_msgs/action/Place`

When a goal is received, it forwards a new goal to pyrobosim:
- Output action: `/execute_action`
- Output type: `pyrobosim_msgs/action/ExecuteTaskAction`

Forwarded fields are mapped as:
- `action.robot` <- `robot_id` parameter (default: `robot`)
- `action.type` <- `"place"`
- `action.object` <- resolved object to place

Object resolution order:
1. `RobotState.manipulated_object` (when available)
2. `default_object` parameter
3. Last seen non-empty `RobotState.manipulated_object`
4. If still empty, the request is forwarded with an empty object and downstream behavior decides the outcome

If no object is immediately available, the node waits briefly for `RobotState` updates
before falling back to empty object forwarding (configurable timeout below).

### Behavior difference vs previous version

- Forwarded `action.object` remains the resolved object name/instance.
- `run.py` now uses a higher `RobotState` publication rate to improve timing alignment with `Place` translation.
- Additional logs now show resolved object name, inferred type, and source (`robot_state`, `default_object`, or `last_seen_robot_state`).
- The translator waits up to `wait_for_object_timeout_sec` (default `0.5`) for dynamic updates before sending an empty object.

### Why this change was needed

During BT execution, the object to place is decided dynamically and may arrive slightly later on `/robot/robot_state`.
With low state publication frequency, the translator could miss that update and forward `object=''`.

This package now addresses it by combining:

- higher simulator state publication rate in `tutorial_sim run`,
- short wait window in the translator,
- fallback to last seen non-empty `manipulated_object`.

### Result handling

The bridge waits for pyrobosim action completion and maps the result back to the original `Place` goal:
- `ExecutionResult.SUCCESS` -> `Place` goal succeeds
- Any other status -> `Place` goal aborts

The goal is aborted if:
- `/execute_action` is not available,
- pyrobosim rejects the forwarded goal,
- no result is returned.

### ROS parameters

- `input_action_name` (default: `/PlaceComponet/Place`)
- `output_action_name` (default: `/execute_action`)
- `robot_state_topic` (default: `/robot/robot_state`)
- `robot_id` (default: `robot`)
- `default_object` (default: empty string)
- `wait_for_object_timeout_sec` (default: `0.5`)
- `wait_server_timeout_sec` (default: `5.0`)

### Run

After building and sourcing your workspace:

```bash
ros2 run tutorial_sim translate_component
```

For reliable dynamic object resolution in `translate_component`, run the simulator (`tutorial_sim run`) from this package version: it publishes `RobotState` at a higher rate (`state_pub_rate=5.0`), so `manipulated_object` updates are visible in time for `Place` translation.

Example with custom parameters:

```bash
ros2 run tutorial_sim translate_component --ros-args \
  -p input_action_name:=/PlaceComponet/Place \
  -p output_action_name:=/execute_action \
  -p robot_id:=robot
```

To see which object is being placed, run the translator and check its logs when a `Place` goal arrives:

```bash
ros2 run tutorial_sim translate_component
```

You will see log lines like:
- `Resolved object 'butter0' (type='butter', source='robot_state').`
- `Forwarding Place -> ExecuteTaskAction(type='place', robot='robot', object='butter0')`

If you want strict behavior (no wait), set:

```bash
ros2 run tutorial_sim translate_component --ros-args \
  -p wait_for_object_timeout_sec:=0.0
```

### Send commands after startup

Once `translate_component` is running, send a `Place` request to the new action endpoint:

```bash
ros2 action send_goal /PlaceComponet/Place overarching_msgs/action/Place "{}"
```
otherwise bypassing the bridger/translator:

```bash
ros2 action send_goal /execute_action pyrobosim_msgs/action/ExecuteTaskAction "{action: {robot: robot, type: place, object: butter}, realtime_factor: 1.0}"
```


Useful checks:

```bash
ros2 action list
ros2 action info /PlaceComponet/Place
ros2 action info /execute_action
```

If the robot is not currently holding an object (`/robot/robot_state`) and `default_object` is empty,
the translator still forwards the request with an empty object. If your downstream requires an explicit
object name, launch the translator with a fallback object:

```bash
ros2 run tutorial_sim translate_component --ros-args -p default_object:=butter
```
