#!/usr/bin/env python3

from scenario import ScenarioRunner
from config import (
    RPC_USER,
    RPC_PASSWORD,
    NODE_BASE_RPC_PORT,
)

# TESTING FOR NOW

scenario = "scenario"

runner = ScenarioRunner(
    rpc_user=RPC_USER,
    rpc_password=RPC_PASSWORD,
    base_port=NODE_BASE_RPC_PORT,
)

runner.load_scenario(scenario)
runner.run_scenario()