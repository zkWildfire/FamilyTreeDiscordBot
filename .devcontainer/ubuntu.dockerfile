FROM ubuntu:jammy
USER root

ARG USERNAME
ARG USER_UID
ARG USER_GID

ARG PYTHON_VERSION=3.11

# Install apt packages
RUN apt-get update -y && \
	apt-get install -y \
		curl \
		git \
		pkg-config \
		python${PYTHON_VERSION} \
		python3-pip \
		ssh \
		sudo \
		tar \
		tree \
		unzip \
		vim \
		zip && \
	update-alternatives --install \
		/usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 3

# Install pip packages
# COPY requirements.txt /tmp/kagamii/requirements.txt
# RUN python3 -m pip install -r /tmp/kagamii/requirements.txt

# Create the user
RUN groupadd --gid $USER_GID $USERNAME && \
	useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash && \
	echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
	chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME
