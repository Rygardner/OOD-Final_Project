FROM python:3.12

RUN set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    g++ gcc make sqlite3 time curl git nano dos2unix \
    net-tools iputils-ping iproute2 sudo gdb less \
    python3-dev build-essential \
    # SDL2 + image, mixer, ttf
    libsdl2-2.0-0 libsdl2-dev \
    libsdl2-image-2.0-0 libsdl2-image-dev \
    libsdl2-mixer-2.0-0 libsdl2-mixer-dev \
    libsdl2-ttf-2.0-0 libsdl2-ttf-dev \
    libfreetype6-dev libjpeg-dev libpng-dev \
    # Wayland + X11 client libs
    libwayland-client0 libxkbcommon0 \
    libx11-6 libxext6 libxrender1 libxrandr2 libxi6 libxcursor1 libxfixes3 libxinerama1 \
    # GL/EGL for rendering paths
    libgl1 libegl1 libgl1-mesa-dri \
  ; rm -rf /var/lib/apt/lists/*



# Install Java and Graphviz for plantuml
# RUN apt install default-jre graphviz -y

ARG USER=user
ARG UID=1000
ARG GID=1000

# Set environment variables
ENV USER=${USER}
ENV HOME=/home/${USER}

# Create user and setup permissions on /etc/sudoers
RUN useradd -m -s /bin/bash -N -u $UID $USER && \
  echo "${USER} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers && \
  chmod 0440 /etc/sudoers && \
  chmod g+w /etc/passwd 

USER user

WORKDIR ${HOME}

RUN pip install --upgrade pip

# install python packages from requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install zsh - use "Bira" theme with some customization. 
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
  -t bira \
  -p git \
  -p ssh-agent \
  -p https://github.com/zsh-users/zsh-autosuggestions \
  -p https://github.com/zsh-users/zsh-completions

ENV PATH="${HOME}/.local/bin:$PATH"
CMD zsh