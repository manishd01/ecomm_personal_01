FROM jenkins/jenkins:lts

USER root

# Docker CLI + curl
RUN apt-get update \
    && apt-get install -y docker.io curl \
    && rm -rf /var/lib/apt/lists/*

# Docker Compose
RUN mkdir -p /usr/local/lib/docker/cli-plugins \
    && curl -fL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
       -o /usr/local/lib/docker/cli-plugins/docker-compose \
    && chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Docker Buildx
RUN mkdir -p /usr/local/lib/docker/cli-plugins \
    && BUILDX_VERSION=$(curl -s https://api.github.com/repos/docker/buildx/releases/latest | grep '"tag_name":' | head -1 | cut -d '"' -f4) \
    && curl -fL "https://github.com/docker/buildx/releases/download/${BUILDX_VERSION}/buildx-${BUILDX_VERSION}.linux-amd64" \
       -o /usr/local/lib/docker/cli-plugins/docker-buildx \
    && chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx

USER jenkins