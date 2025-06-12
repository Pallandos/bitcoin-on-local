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
        wallet_name = params.get('wallet_name', 'default_wallet')
        return self.rpc.call(node, 'createwallet', [wallet_name])
    
    def _action_create_address(self, node: str, params: Dict[str, Any] = None) -> Any:
        """Create a new address on the specified node."""
        if params is None:
            params = {}
        label = params.get('label', '')
        address_type = params.get('address_type', 'bech32')
        return self.rpc.call(node, 'getnewaddress', [label, address_type])

    def _action_send_to(self, node: str, params: Dict[str, Any] = None) -> Any:
        """Send Bitcoin to a specified address on the node."""
        if params is None:
            params = {}
            
        address = params.get('to', '')
        amount = params.get('amount', 0.0)
        return self.rpc.call(node, 'sendtoaddress', [address, amount])
    
    def _action_mine(self, node: str, params: Dict[str, Any] = None) -> Any:
        """Mine a block on the specified node."""
        if params is None:
            params = {}
        num_blocks = params.get('amount', 1)
        address = params.get('address', None) #required
        return self.rpc.call(node, 'generatetoaddress', [num_blocks, address])