FROM jenkins/jenkins:lts

USER root

RUN apt-get update \
    && apt-get install -y docker.io curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/local/lib/docker/cli-plugins \
    && curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
       -o /usr/local/lib/docker/cli-plugins/docker-compose \
    && chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

RUN mkdir -p /usr/libexec/docker/cli-plugins \
    && curl -SL https://github.com/docker/buildx/releases/latest/download/buildx-linux-amd64 \
       -o /usr/libexec/docker/cli-plugins/docker-buildx \
    && chmod +x /usr/libexec/docker/cli-plugins/docker-buildx

USER jenkins