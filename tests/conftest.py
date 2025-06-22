import os
import shutil
import tempfile
from unittest.mock import patch

import pytest


@pytest.fixture(scope="session")
def temp_dir():
    """Fixture to create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_env_vars():
    """Fixture to mock environment variables."""

    env_vars = {
        "NODE_NUMBER": "5",
        "MAX_PEERS": "128",
        "NODE_BASE_RPC_PORT": "18443",
        "NODE_BASE_P2P_PORT": "18444",
        "NODE_BASE_NAME": "node",
        "RPC_USER": "user",
        "RPC_PASSWORD": "password",
        "LOGS_PATH": "./logs",
        "LOG_NET_ENABLED": "false",
        "LOG_MEMPOOL_ENABLED": "true",
        "SCENARIO_PATH": "./scenarios",
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars
