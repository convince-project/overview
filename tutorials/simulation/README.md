# How to use the simulation

> [!WARNING]
> You must be in the `data-model/examples/overarching_tutorial/simulation` folder for this to work.

## Build

```bash
docker build -t convince_tutorial -f .docker/Dockerfile .
```

## Run

```bash
docker run -it --rm\
    --name convince_tutorial\
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw\
    -v ${XAUTHORITY:-$HOME/.Xauthority}:/root/.Xauthority\
    -v ./tutorial_sim:/convince_ws/src/tutorial_sim\
    -v ./.docker/build:/convince_ws/build\
    -e DISPLAY\
    -e QT_X11_NO_MITSHM=1\
    convince_tutorial\
    bash 
```

Inside the docker container, run

```bash
ros2 run tutorial_sim run
```

## Usage

For example:

- Type `fridge` into the `Goal query` box.
- Click `Navigate`.
- Click `Open`. (Notice that all these may fail with some porbability. If nothing changes, just try again.)
- Click `Detect`.
- Type `soda0` into the `Goal query` box.
- Click `Pick`.
- Type `desk` into the `Goal query` box.
- Click `Navigate`.
- Click `Place`.

You must charge before you run out of battery.
But the door to the room with the charger is closed.

- Type `hall_office_closet` into `Goal query` box.
- Click `Navigate`.
- Click `Open`.
- Type `charger` into `Goal query` box.
- Click `Navigate`.
- Notice the battery jumpng to `100%`.

## ROS Integration

All the steps abover could be triggered by ROS actions.
While pyrobosim is running in the other terminal, connect to the same docker:

```bash
docker exec -it convince_tutorial bash
```

And run:

```bash
ros2 action send_goal /execute_action pyrobosim_msgs/action/ExecuteTaskAction action:\ \{robot:\ \'robot\'\,\ type:\ \'\navigate\'\,\ target_location:\ \'office\'\}
```
