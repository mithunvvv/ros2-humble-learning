FROM osrf/ros:humble-desktop

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install common utilities
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    git \
    curl \
    wget \
    build-essential \
    lsb-release \
    net-tools \
    iputils-ping \
    sudo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | apt-key add - \
    && sh -c 'echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list' \
    && apt-get update && apt-get install -y \
    ros-humble-pcl-ros \
    ros-humble-tf2-eigen \
    ros-humble-rviz2 \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y \       
    build-essential \        
    libeigen3-dev \
    libjsoncpp-dev \
    libspdlog-dev \
    libcurl4-openssl-dev \
    libpcap-dev \
    libtins-dev \
    cmake \
    python3-colcon-common-extensions \ 
    && rm -rf /var/lib/apt/lists/*


# Create a non-root user (e.g., devuser)
ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    usermod -aG sudo $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


    # Append lines to bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> /home/devuser/.bashrc && \
    echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> /home/devuser/.bashrc

# Switch to non-root user by default
USER $USERNAME

# Set working directory
WORKDIR /home/$USERNAME