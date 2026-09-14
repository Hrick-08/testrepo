# Sandbox image the agent runs its bash actions inside.
# Keeps generated code / test runs isolated from the Azure VM host.
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pytest

WORKDIR /repo
# The orchestrator mounts/clones the target repo into /repo at run time —
# see run_agent.py for how a fresh container is used per issue.
