# How to use the simulation

The simulation represents a fetch and carry task, where a mobile robot moves in a household environment.
It can pick and place objects.

## Usage

Firstly, start the simulation and explore what is can do.

Run `docker compose run base ros2 run tutorial_sim run`

Then, for example:

- Type `fridge` into the `Goal query` box.
- Click `Navigate`.
- Click `Open`. (Notice that all these may fail with some porbability. If nothing changes, just try again.)
- Click `Detect`.
- Type `butter0` into the `Goal query` box.
- Click `Pick`.
- Type `table` into the `Goal query` box.
- Click `Navigate`.
- Click `Place`.

## Controlling the robot with a Behavior Tree

The tutorial comes with a bt_executor node that can execute a behavior tree to control the robot.
One example tree is provided in `tutorials/roaml/policy/bt_tree.xml`.
To run the bt_executor with this tree, execute

```bash
docker compose run base ros2 launch tutorial_run full_simulation.launch.py policy:=bt_tree.xml
```

Observe how the robot first navigates to the fridge, then opens it, detects the butter, picks it up, navigates to the table, and places it there.
