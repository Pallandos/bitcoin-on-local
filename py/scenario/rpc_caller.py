import requests
import json
from typing import Any

# === Custom Exceptions ===
class BitcoinRPCError(Exception):
    """Custom exception for Bitcoin RPC errors"""
    pass

class BitcoinRPCConnectionError(BitcoinRPCError):
    """Exception raised when RPC connection fails"""
    pass

class BitcoinRPCMethodError(BitcoinRPCError):
    """Exception raised when RPC method returns an error"""
    pass

# ==========================

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
        
        response = requests.post(
            url, 
            data=json.dumps(payload), 
            headers={'content-type': 'application/json'},
            auth=(self.rpc_user, self.rpc_password)
        )
        
        if response.status_code != 200:
            raise BitcoinRPCConnectionError(f"RPC call failed: {response.status_code}")
        
        result = response.json()
        if result.get('error'):
            raise BitcoinRPCMethodError(f"RPC error: {result['error']}")
        
        return result.get('result')


if __name__ == "__main__":
    caller = BitcoinRPC(rpc_user="user", rpc_password="password")
    
    print(caller.call(node="node_4", method="getpeerinfo"))