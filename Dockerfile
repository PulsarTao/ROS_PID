FROM ros:foxy
WORKDIR /workspace

RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    python3-numpy && \
    rm -rf /var/lib/apt/lists/*

COPY ./ ./

RUN . /opt/ros/foxy/setup.sh && \
    cd /workspace && \
    colcon build \

RUN echo ". /opt/ros/foxy/setup.bash" >> ~/.bashrc && \
    echo ". /workspace/my_ros_package/install/local_setup.bash" >> ~/.bashrc

CMD ["bash"]