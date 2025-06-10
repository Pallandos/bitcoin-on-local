#!/bin/bash

set -euo pipefail

# export var from .env
if [[ -f ./.env ]]; then
    set -a
    # shellcheck disable=SC1091
    source ./.env
    set +a
else
    echo "[ERROR] Environment file not found at ./.env."
    exit 1
fi

mkdir -p "$LOGS_PATH"

# ==== Functions ====

function get_docker_names() {
    # grab all docker names running 
    docker compose -f ./docker/docker-compose.yml ps --services --filter "status=running" 2>/dev/null
}

function start_logging() {
    docker_name="${1:-}"

    if [[ -z "$docker_name" ]]; then
        echo "[ERROR] No Docker container name provided."
        exit 1
    fi

    echo "[LOGS ] Starting logs for : $docker_name in $LOGS_PATH"
    docker logs "$docker_name" --follow > "${LOGS_PATH}/${docker_name}.log" 2>&1 &

}

# ==== Main Script ====

# get docker names
docker_names=$(get_docker_names)

if [[ -z "$docker_names" ]]; then
    echo "[ERROR] No Docker containers are running."
    exit 1
fi

# start logging for each docker name
echo "[LOGS ] Starting logging ..."
for docker_name in $docker_names; do
    start_logging "$docker_name"
done
