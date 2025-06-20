# Parse and load the config file

import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()

if dotenv_path:
    load_dotenv(dotenv_path, override=True)
else:
    print("No .env file found")
    
# ===== network =====
NODE_NUMBER = int(os.getenv("NODE_NUMBER", 0))
MAX_PEERS = int(os.getenv("MAX_PEERS", 0))

NODE_BASE_RPC_PORT = int(os.getenv("NODE_BASE_RPC_PORT", 18443))
NODE_BASE_P2P_PORT = int(os.getenv("NODE_BASE_P2P_PORT", 18444))

# ==== names ====
NODE_BASE_NAME = os.getenv("NODE_BASE_NAME", "node")

# ==== login ====
RPC_USER = os.getenv("RPC_USER", "user")
RPC_PASSWORD = os.getenv("RPC_PASSWORD", "password")

# ==== data ====
LOGS_PATH = os.getenv("LOGS_PATH", "./logs")

LOG_NET_ENABLED = os.getenv("LOG_NET_ENABLED", "true").lower() == "true"
LOG_MEMPOOL_ENABLED = os.getenv("LOG_MEMPOOL_ENABLED", "true").lower() == "true"

# ==== Scenarios ====
SCENARIO_PATH = os.getenv("SCENARIO_PATH", "./scenarios")