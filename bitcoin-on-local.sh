#!/bin/bash

# This script is used to run a Bitcoin network on a local machine

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

# get args:
ARG1="${1:-}"

# ==== Functions ====

function activate_venv() {
    if [[ -d "./.venv" ]]; then
        # shellcheck disable=SC1091
        source ./.venv/bin/activate
    else
        echo "[ERROR] Virtual environment not found. Please create it first."
        exit 1
    fi
}

function is_docker_running() {
    if [[ -n "$(docker compose -f ./docker/docker-compose.yml ps -q)" ]]; then
        return 0
    else
        return 1
    fi
}

function start_network() {
    if [[ ! -f ./docker/docker-compose.yml ]]; then
        echo "[ERROR] Docker Compose file not found. Please ensure you have the correct path."
        exit 1
    fi
    # check if a docker is already running
    if is_docker_running; then
        echo "[WARNING] Docker is already running. Stopping existing containers..."
        docker compose -f ./docker/docker-compose.yml down -v --remove-orphans
    fi
    echo "Starting Bitcoin network..."
    docker compose -f ./docker/docker-compose.yml up -d
}

function stop_network() {
    # check if a docker is running
    if ! is_docker_running; then
        echo "[ERROR] No Docker containers are running."
        return 1
    else
        docker compose -f ./docker/docker-compose.yml down -v --remove-orphans
    fi

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

function draw_network() {
    # check if docker is running
    if ! is_docker_running; then
        echo "[ERROR] Docker is not running. Please start the network first."
        exit 1
    fi

    if [[ -f ./py/draw_network.py ]]; then
        python3 ./py/draw_network.py "$1"
    else
        echo "[ERROR] Network drawing script not found."
        exit 1
    fi
}

function print_help() {
    echo "Usage: $0 start|stop|renew|draw|scenario|draw [output_file]"
    echo "  start: Start the Bitcoin network with the current configuration."
    echo "  stop: Stop the Bitcoin network."
    echo "  renew: Generate a new Docker Compose file."
    echo "  restart: Restart the Bitcoin network."
    echo "  scenario [args]: Use scenario features (see $0 scenario -h for details)."
    echo "  draw [output_file]: Draw the network topology and save it to output_file (default: img/bitcoin_network_map.png)."
}

# ==== Main logic ====

activate_venv

case "$ARG1" in
"start")
    echo "[INFO ] Start Bitcoin network with current configuration"
    start_network
    ./script/bit-logs.sh
    ;;
"stop")
    echo "[INFO ] Stopping Bitcoin network..."
    stop_network
    ;;
"renew")
    echo "[INFO ] Generating new compose file"
    generate_config
    echo "[INFO ] You can now start the network with $0 start"
    ;;
"draw")
    echo "[INFO ] Drawing network topology"
    if [[ -z "${2:-}" ]]; then
        draw_network "img/bitcoin_network_map.png"
    else
        draw_network "$2"
    fi
    ;;
"restart")
    echo "[INFO ] Restarting Bitcoin network..."
    docker compose -f ./docker/docker-compose.yml restart
    ;;
"scenario")
    echo "[INFO ] Using scenario features"
    ./script/scenario.sh "${@:2}"
    ;;
"help")
    print_help
    ;;
*)
    echo "[ERROR] Invalid argument: $ARG1"
    echo "Use '$0 help' for usage information."
    exit 1
    ;;
esac
