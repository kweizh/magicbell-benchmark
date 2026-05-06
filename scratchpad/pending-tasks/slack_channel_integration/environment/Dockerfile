FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Environment for creating a bash script to send a MagicBell broadcast with Slack overrides."

RUN mkdir -p /home/user/myproject && \
    chmod 0755 /home/user/myproject

# Container contents:
#   - curl installed for making API requests.
#   - /home/user/myproject  — empty project directory for the script.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]