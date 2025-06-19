import subprocess
import json

def get_peer_info(node_name : str):
    """Get peer information for a given node.

    Args:
        node_name (str): Name of the node to get peer information for.

    Returns:
        list: List of peer information dictionaries or an empty list if an error occurs.
    """
    try:
        cmd = [
            "./bit-cli.sh",
            node_name,
            "getpeerinfo"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error for {node_name}: {e}")
        return []