# this file generates a docker-compose.yml file based on the provided configuration

import random

from config import (
    NODE_NUMBER,
    NODE_BASE_RPC_PORT,
    NODE_BASE_P2P_PORT,
    MAX_PEERS,
    NODE_BASE_NAME,
    RPC_USER,
    RPC_PASSWORD
)

# ==== functions ====

def generate_names(number: int, base_name: str) -> list:
    """Generate a list of node names based on the base name and the number of nodes.

    Args:
        number (int): Number of nodes to generate names for.

    Returns:
        list: A list of node names.
    """
    
    return [f"{base_name}_{i+1}" for i in range(number)]

def compute_ports(number: int, base_rpc: int, base_p2p: int, base_name: str) -> dict:
    """Compute the ports for the nodes based on the base ports and the number of nodes.

    Args:
        number (int): Number of nodes to generate ports for.
        base_rpc (int): Base RPC port.
        base_p2p (int): Base P2P port.
        base_name (str): Base name for the nodes.

    Returns:
        dict: A dictionary where keys are node names and values are tuples (rpc_port, p2p_port).
    """
    
    ports = {}
    rpc_port = base_rpc
    p2p_port = base_p2p
    
    for i in range(number):
        node_name = f"{base_name}_{i+1}"
        ports[node_name] = (rpc_port, p2p_port)
        rpc_port += 2
        p2p_port += 2
    
    return ports

def generate_peers(names: list, max_peers: int) -> dict:
    """Generate a list of peers for each node where each node has a random number of peers.
    Args:
        names (list): List of node names.
        max_peers (int): Maximum number of peers each node can have.

    Returns:
        dict: A dictionary where keys are node names and values are lists of peer names.
    """
        
    peers = {}
        
    for name in names:
        # Get all other nodes (excluding the current node)
        available_peers = [n for n in names if n != name]
         
        # Determine random number of peers (between 1 and max_peers, but not more than available peers)
        num_peers = random.randint(1, min(max_peers, len(available_peers)))
            
        # Randomly select peers
        selected_peers = random.sample(available_peers, num_peers)
            
        peers[name] = selected_peers
        
    return peers

def generate_command(
        template_path,
        rpc_user,
        rpc_password,
        max_peers,
        rpc_port,
        p2p_port,
        peers,
        all_ports : dict,
    ):
    
    add_command = ""
    for peer in peers:
        if peer in all_ports:
            _ , p2p_peer = all_ports[peer]
            add_command += f"    - -addnode={peer}:{p2p_peer} \n"
            #                 ^ the indentation is important for the docker-compose file
    
    add_command = add_command.strip('\n')  # Remove trailing newline
    
    with open(template_path, 'r') as file:
        command_template = file.read()
        command = command_template.format(
            RPCUSER = rpc_user,
            RPCPASSWORD = rpc_password,
            MAXCONNECTIONS = max_peers,
            RPCPORT = rpc_port,
            P2PPORT = p2p_port,
            ADDNODE = add_command
        )
    
    return(command)

def export_data(all_ports: dict, node_names: list, output_dir: str = 'data'):
    """Export node names and RPC ports to environment files.

    Args:
        all_ports (dict): A dictionary where keys are node names and values are tuples (rpc_port, p2p_port).
        node_names (list): List of node names.
        output_dir (str): Subdirectory of /docker to store the .env files. Defaults to 'data'.
    """
    
    # export node names :
    output_file_names = f"docker/{output_dir}/.env.node_names"
    with open(output_file_names, 'w') as file:
        file.write("# Node names\n")
        for node_name in node_names:
            file.write(f"{node_name}\n")
    print(f"Node names exported to {output_file_names}.")
            
    # export ports :
    output_file_port = f"docker/{output_dir}/.env.rpc_ports"
    with open(output_file_port, 'w') as file:
        file.write("# RPC ports for each node\n")
        for node_name, ports in all_ports.items():
            rpc_port = ports[0]
            env_name = node_name.upper().replace("-", "_") + "_RPC_PORT"
            file.write(f"{env_name}={rpc_port}\n")          
    print(f"RPC ports exported to {output_file_port}.")
    
# ==== main logic ====
if __name__ == "__main__":
    # generate node names, ports and peers
    node_names = generate_names(NODE_NUMBER, NODE_BASE_NAME)
    all_ports = compute_ports(NODE_NUMBER, NODE_BASE_RPC_PORT, NODE_BASE_P2P_PORT, NODE_BASE_NAME)
    peers = generate_peers(node_names, MAX_PEERS)
    
    services = ""
    
    # export rpc ports to a file
    export_data(all_ports, node_names)

    # iterate on each nodes
    for node_name in node_names:
        
        commands = generate_command(
            template_path='docker/templates/docker-command.template',
            rpc_user=RPC_USER,
            rpc_password=RPC_PASSWORD,
            max_peers=MAX_PEERS,
            rpc_port=all_ports[node_name][0],
            p2p_port=all_ports[node_name][1],
            peers=peers[node_name],
            all_ports=all_ports
        )
        
        with open("docker/templates/docker-service.template",'r') as file:
            service_template = file.read()
            service = service_template.format(
                SERVICENAME = f'  {node_name}',
                NODENAME = node_name,
                RPCUSER = RPC_USER,
                RPCPASSWORD = RPC_PASSWORD,
                RPCPORT = all_ports[node_name][0],
                P2PPORT = all_ports[node_name][1],
                COMMANDS = commands
            )
            
        services += service + "\n"
    
    with open("docker/templates/docker-compose.template", 'r') as file:
        compose_template = file.read()
        compose_content = compose_template.format(SERVICES=services)
    
    with open("docker/docker-compose.yml", 'w') as file:
        file.write(compose_content)
    print("docker-compose.yml file generated successfully.")