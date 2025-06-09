import subprocess
import json

# this file is responsible of parsing from infos
def _docker_dns(ip_address):
    """Find container name from IP address using docker inspect.
    
    Args:
        ip_address (str): The IP address to look up
            
    Returns:
        str: Container name if found, None otherwise
    """
    try:
        # Get all container IDs
        result = subprocess.run(['/bin/docker', 'ps', '-q'], 
                                capture_output=True, text=True, check=True)
        container_ids = result.stdout.strip().split('\n')
            
        for container_id in container_ids:
            if not container_id:
                continue
                    
            # Inspect each container
            inspect_result = subprocess.run(['/bin/docker', 'inspect', container_id],
                                             capture_output=True, text=True, check=True)
            container_info = json.loads(inspect_result.stdout)[0]
                
            # Check networks for matching IP
            networks = container_info.get('NetworkSettings', {}).get('Networks', {})
            for network_name, network_info in networks.items():
                if network_info.get('IPAddress') == ip_address:
                    return container_info.get('Name', '').lstrip('/')
                        
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
        pass
            
    return None

def extract_connections(peers_info):
    """Extracts connections from peer information.

    Args:
        peers_info (json type String): JSON string containing peer information.

    Returns:
        List: A list of tuples containing peer IP and connection type.
        
    Example:
        >>> peers_info = [JSON object with 'addr' and 'connection_type']
        >>> extract_connections(peers_info)
        [('node_ip1', 'connection_type1'), ('node_ip2', 'connection_type2')]
    """
    connections = []
    
    for peer_json in peers_info:
        peer_addr = peer_json.get('addr', '').split(':')[0]  # peer IP
        connection_type = peer_json.get('connection_type', 'unknown')
        node_addr = peer_json.get("addrbind", '').split(':')[0]  # node IP
        
        if peer_addr and node_addr:
            # resolve container name if needed
            if peer_addr.startswith('172.20.0.'):
                peer_name = _docker_dns(peer_addr)
            else:
                peer_name = peer_addr
            connections.append((peer_name,connection_type))
    
    return connections

if __name__ == "__main__":
    #tests 
    
    name = _docker_dns("172.20.0.7")
    print(name)