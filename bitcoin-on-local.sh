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
    # check if a docker is already running
    if [[ -n "$(docker compose -f ./docker/docker-compose.yml ps -q)" ]] ; then
        echo "[WARNING] Docker is already running. Stopping existing containers..."
        docker compose -f ./docker/docker-compose.yml down -v --remove-orphans
    fi
    echo "Starting Bitcoin network..."
    docker compose -f ./docker/docker-compose.yml up -d 
}

function stop_network() {
    echo "Stopping Bitcoin network..."
    docker compose -f ./docker/docker-compose.yml down -v --remove-orphans
}

function generate_config() {
    echo "Generating compose file..."
    if [[ -f ./py/generate_compose.py ]]; then
        python3 ./py/generate_compose.py
    else
        echo "[ERROR] Configuration generation script not found."
        exit 1
    fi 
}

# ==== Main logic ====
case "$ARG1" in
    "start")
        echo "[INFO ] Start Bitcoin network with current configuration"
        start_network
        ;;
    "stop")
        stop_network
        ;;
    "renew")
        echo "[INFO ] Recreate configuration and restart Bitcoin network"
        generate_config
        start_network
        ;;
    *)
        echo "Usage: $0 {start|stop|renew}"
        exit 1
        ;;
esac