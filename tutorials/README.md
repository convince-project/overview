# Tutorial Introduction

## Prerequisites

To follow the tutorials using the provided Docker image, you need to have `docker` and `docker compose` installed on your machine.
Please refer to the [Docker installation instructions](https://docs.docker.com/engine/install/) for your operating system.

## Running the simulation

These tutorials are designed to give you a introduction to the tools that the CONVINCE toolbox provides by walking you through using them on a simple example.
The example that all the tutorials are based on is a fetch and carry task, where a mobile robot moves in a household environment, picks up an object, and delivers it to a target location.

To run the simulation for the tutorials, execute in the root of the repository:

```bash
docker compose pull
docker compose up -d
docker compose run base ros2 run tutorial_sim run 
```

You should see a GUI something like this:

![PyRoboSim GUI](imgs/pyrobosim.png)

## Explore the simulation

In the opened GUI, you can interact with the simulation by triggering actions of the robot.
For example

- Type `kitchen_table` in the `Goal query`-field
- Click `Navigate`
- Watch the robot navigate to the kitchen table
- Observer that now more actions are available, such as `Pick` and `Detect`
- We can see that there is an object `soda0` on the table
- Type `soda0` in the `Goal query`-field
- Click `Pick`
- Note that the robot may fail to pick the object with a certain probability, so you may have to try a few times until it succeeds

You may close the GUI, as it will be automatically started again in the next step.

## Control the simulation by executing a behavior tree

As an example of an autonomous system, the robot can be controlled by executing a behavior tree.
You can find one under `tutorials/roaml/policy/bt_tree.xml`.
In order to graphically examine this BT, run:

```bash
docker compose run base groot -f /convince_ws/src/tutorials/roaml/policy/bt_tree.xml
```

(You will have to click `OK` multiple times to get through the warnings about missing plugins.)

To run the simulation again and execute the behavior tree, run:

```bash
docker compose run base ros2 launch tutorial_run full_simulation.launch.py policy:=bt_tree.xml
```

## Next steps

Now choose one of the tutorials in the left sidebar to get a more detailed introduction to the tools that are used in the CONVINCE toolbox.
