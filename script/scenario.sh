#!/bin/bash

# this script is used to deal with the scenario features

set -euo pipefail

# ==== Variables ====

ARG1="${1:-}"

# ==== Functions ====

function is_docker_running() {
    if [[ -n "$(docker compose -f ./docker/docker-compose.yml ps -q)" ]]; then
        return 0
    else
        return 1
    fi
}

# ==== Main Logic ====
case "$ARG1" in
    "run")
        if ! is_docker_running; then
            echo "[SCENARIO] Docker is not running. Please start the network first."
            exit 1
        fi
        python3 py/run_scenario.py "${@:1}"
        ;;
    *)
        # might raise an error (by run_scenario.py):
        python3 py/run_scenario.py "$ARG1"
        ;;
esac