# Network configuration 

- [Network configuration](#network-configuration)
  - [Parameters](#parameters)
    - [`NODE_NUMBER`](#node_number)
    - [`MAX_PEERS`](#max_peers)
    - [`NODE_BASE_RPC_PORT`](#node_base_rpc_port)
    - [`NODE_BASE_P2P_PORT`](#node_base_p2p_port)
    - [`NODE_BASE_NAME`](#node_base_name)
    - [`RPC_USER` and `RPC_PASSWORD`](#rpc_user-and-rpc_password)
    - [`LOGS_PATH`](#logs_path)
    - [Logs options](#logs-options)
    - [`SCENARIO_PATH`](#scenario_path)
  - [Example](#example)

The `.env` file is used to configure your bitcoin network.

> [!WARNING]
> The syntax of `.env` is pretty strict : do not use any spaces before or after the `=`.

## Parameters 

### `NODE_NUMBER`

- **Description :** The number of Bitcoin nodes in your local network.
- **Type :** `int`
- **Default value :**  `0`

> [!IMPORTANT]
> Remember that each node will be compute by your machine. Even if the image is pretty small you should take in account the power of your machine. 

---

### `MAX_PEERS`

- **Description :** Max number of peers for each node
- **Type :** `int`
- **Default value :** `0`

> [!NOTE]
> This parameter should not be fixed under ~11. For obscure reasons if set under, nodes will refuse every connections and you network will be empty.

---

### `NODE_BASE_RPC_PORT`

- **Description :** The base port for RPC protocol
- **Type :** `int`
- **Default value :** `18443`

Each node will be placed in a docker conteneur. To avoid conlicts with port when interracting from the outside, the ports will be spaced following this formula : $`rpc\_port_{i} = 18443 + (i-1)\times2`$. By doing so, port wont collide. If you have Bitcoin Core running on regtest on your computer, consider changing `NODE_BASE_RPC_PORT` in your config.

---

### `NODE_BASE_P2P_PORT`

- **Description :** The base port for P2P port 
- **Type :** `int`
- **Default value :** `18444`

Same as [`NODE_BASE_RPC_PORT`](#node_base_rpc_port)

---

### `NODE_BASE_NAME`

- **Description :** The preffix of all node names. 
- **Type :** `string`
- **Default value :** `node`

All node will be named like : `BASE_NAME_i` where `i` is the number of the node (starting from `1`).

---

### `RPC_USER` and `RPC_PASSWORD`

- **Description :** Username and password for RPC protocol in each node. 
- **Type :** `string`
- **Default value :** `user` and `password`

`bit-cli` and other scripts will use this value to interract with the node. Because this is only a local regtest version ,there is no need to pass a complicated password. 

---

### `LOGS_PATH`

- **Description :** Path of the logs output
- **Type :** `string` (relative of absolute path)
- **Default value :** `./logs`

---

### Logs options 

- **Description :** Which logs are reported to the log output
- **Type :** `booolean`
- **Default value :**
  - `LOG_NET_ENABLED` : `true`
  - `LOG_TX_ENABLED` : `true`
  - `LOG_MEMPOOL_ENABLED` : `true`

The categories above are categories from the valid debug logging categories (see [bitcoin Core doc](https://developer.bitcoin.org/reference/rpc/logging.html)).

---

### `SCENARIO_PATH`

- **Description :** Path of the scenarios files.
- **Type :** `string` (relative of absolute path)
- **Default value :** `./scenarios` 

Scenario file will be read from this folder. There is no need to change it, you should rather move files to the `./scenarios` folder.

## Example 

```.env
# This is the configuration file

# ==== network ====
NODE_NUMBER=5
MAX_PEERS=128
# WARNING : set this value high (don't know why, but if it's
# under ~11 , a node will refuse all connections)

NODE_BASE_RPC_PORT=18443
NODE_BASE_P2P_PORT=18444

# ==== names ====
NODE_BASE_NAME=node

# ==== login ====
RPC_USER=user
RPC_PASSWORD=password

# ==== data ====
LOGS_PATH=./logs

# the following options describe which logs you want to print (boolean)
LOG_NET_ENABLED=false
LOG_TX_ENABLED=true
LOG_MEMPOOL_ENABLED=true

# ==== Scenarios ====
SCENARIO_PATH=./scenarios
```