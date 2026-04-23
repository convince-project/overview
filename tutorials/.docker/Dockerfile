FROM ros:jazzy-ros-base
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root


# Install apt dependencies.
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    apt-utils curl fuse3 libfuse2 gdb nano \
    terminator dbus-x11 \
    libegl1 libgl1-mesa-dev libglu1-mesa-dev '^libxcb.*-dev' libx11-xcb-dev \
    libxi-dev libxkbcommon-dev libxkbcommon-x11-dev libxrender-dev \
    libnss3 libasound2t64 libxkbfile1 \
    python3-pip python3-tk python3-wrapt python3-inflection \
    ros-jazzy-example-interfaces ros-jazzy-rqt-service-caller ros-jazzy-plotjuggler ros-jazzy-plotjuggler-ros \
    libczmq-dev ros-jazzy-zmqpp-vendor-dbgsym ros-jazzy-zmqpp-vendor libczmq-dev libczmq4 \
    qt6-scxml* rustup tmux libboost-all-dev libcairo2-dev

# Create a ROS 2 workspace.
RUN mkdir -p /convince_ws/src/
WORKDIR /convince_ws

# Install external dependencies.
# (pip)
COPY tutorials/requirements.txt /convince_ws
RUN pip3 install --break-system-packages -r requirements.txt

# (pyrobosim)
RUN git clone -b 4.3.4 https://github.com/sea-bass/pyrobosim.git src/pyrobosim

# (bt_executor)
# `behaviortree_ros2` from source since it is not released for Jazzy
RUN git clone --depth 1 https://github.com/BehaviorTree/BehaviorTree.ROS2.git src/behaviortree_ros2
RUN source /opt/ros/jazzy/setup.bash && \
    rosdep install --from-paths src -y --ignore-src
RUN curl -O -L https://pub-32cef6782a9e411e82222dee82af193e.r2.dev/Groot2-v1.9.0-x86_64.AppImage
RUN chmod +x Groot2-v1.9.0-x86_64.AppImage && \
    mv Groot2-v1.9.0-x86_64.AppImage /usr/local/bin/groot

# (ros)
COPY tutorials/ /convince_ws/src/tutorials/
RUN rosdep update && \
    rosdep install --from-paths src -y --ignore-src
RUN source /opt/ros/jazzy/setup.bash && \
    colcon build --symlink-install && \
    source install/setup.bash

# (smc_storm)
RUN mkdir /smc_storm
WORKDIR /smc_storm
RUN curl -O -L https://github.com/convince-project/smc_storm/releases/download/0.1.8/smc_storm_executable.tar.gz && \
    tar -xzf smc_storm_executable.tar.gz && \
    ./install.sh --install-dependencies && \
    ln -s /smc_storm/bin/smc_storm /usr/local/bin/smc_storm

# (AS2FM)
WORKDIR /
RUN git clone https://github.com/convince-project/AS2FM.git
RUN pip3 install --break-system-packages /AS2FM

# (SCAN)
RUN rustup default stable
RUN cargo install smc_scan --version 0.2.0 --locked
RUN echo "PATH=$PATH:~/.cargo/bin" >> ~/.bashrc

# (MOON)
WORKDIR /
RUN git clone https://github.com/convince-project/MOON.git
RUN pip install -e /MOON --break-system-packages

# Install REFINE-PLAN
RUN git clone https://github.com/convince-project/refine-plan.git src/refine-plan
RUN cd src/refine-plan; pip3 install --break-system-packages -r requirements.txt
RUN cd src/refine-plan; pip3 install --break-system-packages .
RUN rm -r src/refine-plan

# Set back the workdir to be the convince_ws
WORKDIR /convince_ws
# Set up the entrypoint.
COPY tutorials/.docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
RUN echo "source /entrypoint.sh && print_ros_variables" >> ~/.bashrc
