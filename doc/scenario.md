# Scenario

- [Scenario](#scenario)
  - [Structure of a scenario](#structure-of-a-scenario)
    - [`[scenario]` - Description of the scenario](#scenario---description-of-the-scenario)
    - [`[config]` - General configuration](#config---general-configuration)
    - [`[steps]` - Scenario steps](#steps---scenario-steps)

A **scenario** is an automated sequence of actions designed to reproduce the exact same sequence of events on a Bitcoin network. The main goal of a scenario is to ensure that a specific situation can be replayed identically, making it possible to analyze, test, or demonstrate network behavior in a consistent and repeatable way.

Scenarios are written in a `.toml` file, and should be put in the `./scenario` folder. 

> See [TOML website](https://toml.io/en/) for documentation about TOML 

## Structure of a scenario

To be valide, a **scenario** file should have the three following elements :

- `[scenario]` - Describes the scenario
- `[config]` - General configuration of the scenario
- `[step]` - At least one step 

You can see the [`scenario.toml`](../scenarios/scenario.toml) example.

---

### `[scenario]` - Description of the scenario

The `[scenario]` section provides essential metadata about the scenario.

**Required fields:**

- `name` - Name of the scenario
  - **Type:** `string`
  - **Description:** A short, descriptive name for the scenario
- `description` - Detailed description of the scenario
  - **Type:** `string`
  - **Description:** Multi-line description explaining what the scenario does and its purpose
- `date` - Creation or last modification date
  - **Type:** `datetime`
  - **Format:** ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- `author` - Author of the scenario
  - **Type:** `string`
  - **Description:** Name or identifier of the scenario creator

**Example:**

```toml
[scenario]
name = "Basic Bitcoin Operations"
description = """\
                This scenario demonstrates basic Bitcoin operations \
                including wallet creation, address generation, and mining.\
                """
date = 2025-06-12T10:30:00
author = "Developer"
```

---

### `[config]` - General configuration

The `[config]` section defines default values and global settings that apply to all steps in the scenario unless overridden at the step level.

**Available options:**

- `default_node` - Default node identifier for all actions
  - **Type:** `string`
  - **Description:** Node identifier that will be used when no specific node is specified in a step
- `default_wait` - Default wait time between steps
  - **Type:** `number`
  - **Description:** Default wait time in seconds after each action execution
- `timeout` - Global timeout for RPC commands
  - **Type:** `number`
  - **Description:** Maximum time in seconds to wait for RPC command responses

**Example:**
```toml
[config]
default_node = "node_1"
default_wait = 2
timeout = 30
```

---

### `[steps]` - Scenario steps

The `[steps]` section contains all the actions that will be executed sequentially. Each step is defined as `[steps.step_name]` where `step_name` is a unique identifier for the step.

**Required fields for each step:**

- `name` - Human-readable name for the step
  - **Type:** `string`
  - **Description:** Descriptive name explaining what this step does
- `action` - Type of action to execute
  - **Type:** `string`
  - **Description:** Must match one of the available action types (see [Actions documentation](actions.md))

**Optional fields:**

- `node` - Node identifier for this specific step
  - **Type:** `string`
  - **Default:** Uses `config.default_node`
- `wait_after` - Wait time after this step
  - **Type:** `number`
  - **Default:** Uses `config.default_wait`
- `print` - Display action result in console
  - **Type:** `boolean`
  - **Default:** `false`
- `args` - Action-specific arguments
  - **Type:** `table`
  - **Description:** Contains all parameters required by the specific action type (see [Actions documentation](actions.md))

**Example:**
```toml
[steps.step1]
name = "Create wallet"
action = "create_wallet"
node = "node_1"
args.wallet_name = "wallet1"
wait_after = 4

[steps.step2]
name = "Create address"
action = "create_address"
node = "node_1"
args.store_result = "ADDRESS1"
print = true
```

> **Actions** are a very important part of a scenario. Make sure to reead the [Actions documentation](actions.md)