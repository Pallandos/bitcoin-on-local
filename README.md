<p align="center">
  <a href="https://www.codefactor.io/repository/github/pallandos/bitcoin-on-local"><img src="https://www.codefactor.io/repository/github/pallandos/bitcoin-on-local/badge" alt="CodeFactor" /></a>
  <a href="https://app.deepsource.com/gh/Pallandos/bitcoin-on-local/" target="_blank"><img alt="DeepSource" title="DeepSource" src="https://app.deepsource.com/gh/Pallandos/bitcoin-on-local.svg/?label=active+issues&token=kKD53qXxyNJvHRShZndumcGp"/></a>
</p>

# Bitcoin-on-local

- [Bitcoin-on-local](#bitcoin-on-local)
	- [Usage](#usage)
	- [Installation](#installation)
		- [Requirements](#requirements)
		- [Install](#install)
	- [Features](#features)
		- [`bit-cli` : built-in easy client](#bit-cli--built-in-easy-client)
		- [Scenario runner](#scenario-runner)
		- [Network visualisation](#network-visualisation)
		- [Logging](#logging)


This is a tool to deploy a Bitcoin network on your local machine to do some regtest.

Documentation is beeing written. See [scenario documentation](./doc/scenario.md) and [action documentation](./doc/actions.md)

## Usage

First thing you need to do is defining your network in `.env`. You can configure evrything in there to match your needs. 

> [!NOTE]
> See [configuration doc](./doc/config.md) for complete informations network configuration.


Then, you need to generate the compose of the network with :

```sh
./bitcoin-on-local.sh renew
```

This will create a `docker-compose.yml` in `./docker/` folder. You can edit it if you are not happy with the result, this file will **not** be overwritten by any run. 

To start the network, hit : 

```sh
./bitcoin-on-local.sh start
```

## Installation

### Requirements

This tool requires :

- Docker (compose v2)
- Python (>=3.12)[^1]

[^1]: The tool may works on older versions bit has not been tested on it. 

All other dependencies will be installed with pip. See [requirements.txt](./requirements.txt).

### Install

1. First, clone or download the repository. 
2. Grant the execution rights to `install.sh` : 

		chmod +x ./install.sh

3. Run the install script :

		./install.sh

4. If installation is successful, you should see the usage of `./bitcoin-on-local.sh`.

## Features

### `bit-cli` : built-in easy client

### Scenario runner

### Network visualisation

### Logging