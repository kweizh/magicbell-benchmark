FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Environment for MagicBell REST API task using curl."

RUN mkdir -p /home/user/project && \
    chmod 0755 /home/user/project

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - /home/user/project: base directory for the task

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
