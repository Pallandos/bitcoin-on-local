import requests
import json
from typing import Any

class BitcoinRPCError(Exception):
    """Custom exception for Bitcoin RPC errors."""
    pass

class RPCUnexpectedResponseError(Exception):
    """Custom exception for unexpected responses from Bitcoin RPC."""
    pass

class BitcoinRPC:
    """A class to handle RPC calls to Bitcoin nodes.
    """
    def __init__(self, rpc_user: str, rpc_password: str, base_port: int = 18443):
        """Initialize the BitcoinRPC class with RPC user, password, and base port.
        
        All inputs should match the configuration of the Bitcoin nodes.

        Args:
            rpc_user (str): RPC username
            rpc_password (str): RPC password
            base_port (int, optional): base port. Defaults to 18443.
        """
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.base_port = base_port
        
    def call(self, node: str, method: str, params: list = None) -> Any:
        """Make RPC call to Bitcoin node"""
        if params is None:
            params = []
            
        # Extract node number and calculate port
        node_num = int(node.split('_')[-1])
        port = self.base_port + (node_num - 1) * 2
        url = f"http://localhost:{port}"
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        
        try:
            response = requests.post(
                url, 
                data=json.dumps(payload), 
                headers={'content-type': 'application/json'},
                auth=(self.rpc_user, self.rpc_password),
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Check for RPC errors
            if 'error' in result and result['error'] is not None:
                raise BitcoinRPCError(f"RPC error on {node}: {result['error']}")
                
            return result.get('result', None)
            
        except requests.ConnectionError as e:
            raise requests.ConnectionError(f"Connection failed to {node}") from e
        except requests.Timeout as e:
            raise requests.Timeout(f"Timeout for {node}") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON response from {node}") from e
        except Exception as e:
            raise RPCUnexpectedResponseError(f"Unexpected response from {node}: {str(e)}") from e

