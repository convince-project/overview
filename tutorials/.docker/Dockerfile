FROM ros:jazzy-ros-base
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install apt dependencies.
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    apt-utils curl fuse3 libfuse2 gdb nano \
    libegl1 libgl1-mesa-dev libglu1-mesa-dev '^libxcb.*-dev' libx11-xcb-dev \
    libxi-dev libxkbcommon-dev libxkbcommon-x11-dev libxrender-dev \
    libnss3 libasound2t64 libxkbfile1 \
    python3-pip python3-tk python3-wrapt python3-inflection \
    ros-jazzy-example-interfaces ros-jazzy-rqt-service-caller

# Create a ROS 2 workspace.
RUN mkdir -p /convince_ws/src/
WORKDIR /convince_ws

# Install external dependencies.
# (pip)
COPY requirements.txt /convince_ws
RUN pip3 install --break-system-packages -r requirements.txt
# COPY dependencies src/dependencies
# RUN source /opt/ros/jazzy/setup.bash && \
#     rosdep install --from-paths src -y --ignore-src
# (pyrobosim)
RUN git clone -b 4.3.3 https://github.com/sea-bass/pyrobosim.git src/pyrobosim

# # (smc_storm)
# RUN curl -O -L https://github.com/convince-project/smc_storm/releases/download/0.0.6/smc_storm_executable.tar.gz && \
#     tar -xzf smc_storm_executable.tar.gz && \
#     ./install.sh --install-dependencies && \
#     ln -s /convince_ws/bin/smc_storm /usr/local/bin/smc_storm
# # (AS2FM)
# RUN cd src/dependencies/convince/AS2FM && \
#     pip3 install --break-system-packages . && \
#     pip3 uninstall -y --break-system-packages js2py && \
#     pip3 install --break-system-packages git+https://github.com/felixonmars/Js2Py.git@py3.12  # Temporary fix for js2py && \
#     pip3 uninstall -y --break-system-packages matplotlib  # Temporary fix for MatPlotLib conflict

# # Remove MatPlotLib display warnings.
# RUN mkdir /tmp/runtime-root
# ENV XDG_RUNTIME_DIR "/tmp/runtime-root"
# RUN chmod -R 0700 /tmp/runtime-root
# ENV NO_AT_BRIDGE 1

# Set up the entrypoint.
CMD /bin/bash
COPY .docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
RUN echo "source /entrypoint.sh && print_ros_variables" >> ~/.bashrc
