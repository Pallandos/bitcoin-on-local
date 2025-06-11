from .rpc_caller import BitcoinRPC
from typing import Dict, Any

class ActionExecutor:
    """ActionExecutor class to handle actions on Bitcoin nodes.
    This class provides a method to execute various actions on Bitcoin nodes using RPC calls.
    It uses the BitcoinRPC class to make the actual RPC calls to the nodes.
    """
    
    def __init__(self, rpc: BitcoinRPC):
        """Initialize the ActionExecutor with a BitcoinRPC instance.

        Args:
            rpc (BitcoinRPC): An instance of the BitcoinRPC class to handle RPC calls.
        """
        self.rpc = rpc
        
    def execute(self, action: str, node: str, params: Dict[str, Any] = None) -> Any:
        """Execute an action on a specified Bitcoin node.

        Args:
            action (str): The action to execute (e.g., 'getblock', 'sendtoaddress').
            node (str): The node identifier (e.g., 'node_1').
            params (Dict[str, Any], optional): Parameters for the action. Defaults to None.

        Returns:
            Any: The result of the RPC call.
        """
        
    
        # this is a dispatcher method that calls the appropriate RPC method
        methode = f"_action_{action}"
        if hasattr(self, methode):
            return getattr(self, methode)(node, params)
        else:
            raise ValueError(f"Action '{action}' is not supported.")
    
    # ===== Action Methods =====
    
    def _action_cmd(self, node: str, params: Dict[str, Any] = None) -> Any:
        """Execute a raw command on the specified node."""
        if params is None:
            params = {}
        command = params.get('cmd', '')
        call = command.split(' ')[0]
        args = command.split(' ')[1:] if len(command.split(' ')) > 1 else []
        return self.rpc.call(node, call, args)
    
    def _action_create_wallet(self, node: str, params: Dict[str, Any] = None) -> Any:
        """Create a new wallet on the specified node."""
        if params is None:
            params = {}
        return self.rpc.call(node, 'createwallet', [params.get('wallet_name', 'default_wallet')])
    
    def _action_create_address(self, node: str, params: Dict[str, Any] = None) -> Any:
        """Create a new address on the specified node."""
        if params is None:
            params = {}
        return self.rpc.call(node, 'getnewaddress', [params.get('label', ''), params.get('address_type', 'bech32')])