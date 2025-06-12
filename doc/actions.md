# Actions in Scenarios

- [Actions in Scenarios](#actions-in-scenarios)
  - [General structure](#general-structure)
  - [Available actions](#available-actions)
    - [`cmd` - RPC brut command](#cmd---rpc-brut-command)
    - [`create_wallet` - Create a new wallet](#create_wallet---create-a-new-wallet)
    - [`create_address` - Generate a new address](#create_address---generate-a-new-address)
    - [`send_to` - Send Bitcoin](#send_to---send-bitcoin)
    - [`mine` - Mine blocks](#mine---mine-blocks)
  - [Variables and result storage](#variables-and-result-storage)

Each step in a scenario is one and one only action. This documentation covers actions.

## General structure

Each action in this tool has the following structure :

```toml
[steps.step_name]
name = "Do some action"
action = "action_type"      # this is an action type
node = "node_i"             # default to config.default_node
args.param1 = "some param"  # arguments can be passed
args.parami = "more param"
wait_after = 1              # default to config.default_wait
print = true                # default to fault
```

Every *argument* describes in this documentation has to be passed under `.args` like `param1` in the example above.

The `action` parameter has to match one of the following available action. 

## Available actions

### `cmd` - RPC brut command

**Description :** Execute a direct RPC Bitcoin command to the specified node.

**Args :**

- `cmd` (required) : RPC command to execute
  - Type : `string`
  - Example : `"getbalance"`, `"getblockcount"`, `"listunspent 1 9999999"`
  
**Example :**
```toml
[steps.check_balance]
name = "check balance"
action = "cmd"
node = "node_1"
args.cmd = "getbalance"
print = true
```

---

### `create_wallet` - Create a new wallet

**Description :** Create a new Bitcoin wallet on the specified node.

**Args :**

- `wallet_name` (optional) : Name of the wallet to create
  - Type : `string`
  - Default : `"default_wallet"`
  
**Example :**
```toml
[steps.create_wallet]
name = "Create main wallet"
action = "create_wallet"
node = "node_1"
args.wallet_name = "main_wallet"
```

---

### `create_address` - Generate a new address

**Description :** Generate a new Bitcoin address on the specified node.

**Args :**

- `label` (optional) : Label for the address
  - Type : `string`
  - Default : `""` (empty string)
- `address_type` (optional) : Type of address to generate
  - Type : `string`
  - Default : `"bech32"`
  - Possible values : `"legacy"`, `"p2sh-segwit"`, `"bech32"`
  
**Example :**
```toml
[steps.create_address]
name = "Generate receiving address"
action = "create_address"
node = "node_1"
args.label = "receiving_addr"
args.address_type = "bech32"
args.store_result = "RECEIVE_ADDR"
```

---

### `send_to` - Send Bitcoin

**Description :** Send Bitcoin to a specified address from the node's wallet.

**Args :**

- `to` (required) : Destination address
  - Type : `string`
  - Can use variables : `"${VARIABLE_NAME}"`
  - Default : `""` (empty string) → will raise to an error
- `amount` (required) : Amount to send
  - Type : `number` or `string`
  - Unit : Bitcoin (not satoshis)
  - Default : `0.0`
  
**Example :**
```toml
[steps.send_payment]
name = "Send 5 BTC to address"
action = "send_to"
node = "node_1"
args.to = "${DESTINATION_ADDR}"
args.amount = 5.0
```

---

### `mine` - Mine blocks

**Description :** Mine Bitcoin blocks and assign the reward to a specified address.

**Args :**

- `amount` (optional) : Number of blocks to mine
  - Type : `number`
  - Default : `1`
- `address` (required) : Address that will receive mining rewards
  - Type : `string`
  - Can use variables : `"${VARIABLE_NAME}"`
  - Default : `None` → will raise an error
  
**Example :**
```toml
[steps.mine_blocks]
name = "Mine 101 blocks for coinbase maturity"
action = "mine"
node = "node_1"
args.amount = 101
args.address = "${MINER_ADDR}"
```

## Variables and result storage

Actions can store their results in variables for use in subsequent steps:

- **Storage :** Use `args.store_result = "VARIABLE_NAME"` in the action args
- **Usage :** Use `"${VARIABLE_NAME}"` in parameters of later steps

**Example chain :**
```toml
[steps.create_addr]
action = "create_address"
args.store_result = "MY_ADDRESS"

[steps.mine_to_addr]
action = "mine"
args.address = "${MY_ADDRESS}"
args.amount = 50
```