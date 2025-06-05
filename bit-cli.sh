#!/bin/bash

# This is a modified bitocin-cli to interract easily with the bitcoin network on a local machine

set -euo pipefail

# export var from .env
if [[ -f ./.env ]]; then
    set -a
    # shellcheck disable=SC1091
    source ./.env
    set +a
    if [[ -z "${RPC_USER:-}" || -z "${RPC_PASSWORD:-}" ]]; then
        echo "[ERROR] RPC_USER and RPC_PASSWORD must be set in .env file."
        exit 1
    fi
else
    echo "[ERROR] Environment file not found at ./.env."
    exit 1
fi

# export all ports from docker/.env.rpc_ports
if [[ -f ./docker/.env.rpc_ports ]]; then
    set -a
    # shellcheck disable=SC1091
    source ./docker/.env.rpc_ports
    set +a
else
    echo "[ERROR] RPC ports file not found at ./docker/.env.rpc_ports."
    exit 1
fi

# ==== functions ====
function help() {
    echo "bit-cli is a modified bitcoin-cli script to interact with a Bitcoin node running in Docker."
    echo "It requires the node name as the first argument and any bitcoin-cli arguments after that."
    echo ""
    echo "Usage: $0 <node_name> <bitcoin-cli-args>"
    echo "Example: $0 node1 getblockchaininfo"
    exit 0
}

# ==== get args ====:
if [[ "${1:-}" == "help" ]] ; then
    help
fi

node_name="${1:-}"

if [[ -z "$node_name" ]]; then
    echo "[ERROR] Node name is required as the first argument."
    echo "[INFO ] See '$0 help' for usage."
    exit 1
fi

# all other args are passed to bitcoin-cli
shift || true
if [[ -z "$*" ]]; then
    echo "[ERROR] No arguments provided for bitcoin-cli."
    echo "[INFO ] See '$0 help' for usage."
    exit 1
fi
args=("$@") # all remaining arguments

# ==== Main logic ====
var_name="${node_name^^}_RPC_PORT"
rpc_port="${!var_name}"

docker exec \
    "$node_name" \
    bitcoin-cli \
    -rpcport="$rpc_port" \
    -regtest \
    -rpcuser="$RPC_USER" \
    -rpcpassword="$RPC_PASSWORD" \
    "${args[@]}"
