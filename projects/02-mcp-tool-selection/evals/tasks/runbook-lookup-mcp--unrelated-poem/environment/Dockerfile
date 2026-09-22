FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# AGENCY_EVAL_NEW_ANCHOR

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python-is-python3 \
    && python -m pip install --no-cache-dir mcp==1.30.0 \
    && rm -rf /var/lib/apt/lists/*
