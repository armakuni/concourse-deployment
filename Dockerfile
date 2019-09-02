FROM debian:stable-slim
LABEL maintainer=sulabh.chaturvedi@outlook.com

RUN apt-get update && \
    apt-get install -y wget && \
    apt-get install -y build-essential zlibc zlib1g-dev ruby ruby-dev openssl libxslt1-dev libxml2-dev libssl-dev libreadline7 libreadline-dev libyaml-dev libsqlite3-dev sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

ARG CONTROL_TOWER_VERSION=0.8.1
RUN wget -qO control-tower https://github.com/EngineerBetter/control-tower/releases/download/${CONTROL_TOWER_VERSION}/control-tower-linux-amd64 && \
    mv control-tower /usr/local/bin && \
    chmod +x /usr/local/bin/control-tower

# Your IAAS provider AWS or GCP (are the ones only supported ATM)
ARG CLOUD_PROVIDER
ENV CLOUD_PROVIDER=${CLOUD_PROVIDER}

# Get Info of, Deploy or Destroy Concourse
ARG CONCOURSE_ACTION 
ENV CONCOURSE_ACTION=${CONCOURSE_ACTION}

ENTRYPOINT control-tower $CONCOURSE_ACTION --iaas $CLOUD_PROVIDER deploy-concourse-ci
