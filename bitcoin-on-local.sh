#!/bin/bash

# This script is used to run a Bitcoin network on a local machine

set -euo pipefail

# get args:
ARG1="${1:-}"

# ==== Functions ====

function start_network() {
    if [[ ! -f ./docker/docker-compose.yml ]]; then
        echo "[ERROR] Docker Compose file not found. Please ensure you have the correct path."
        exit 1
    fi
    echo "Starting Bitcoin network..."
    docker compose -f ./docker/docker-compose.yml up -d
}

function stop_network() {
    echo "Stopping Bitcoin network..."
    docker compose -f ./docker/docker-compose.yml down -v --remove-orphans
}

# ==== Main logic ====
case "$ARG1" in
    "start")
        start_network
        ;;
    "stop")
        stop_network
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac