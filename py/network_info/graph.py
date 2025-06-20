# this file is responsible for creating the network graph

import networkx as nx
import matplotlib.pyplot as plt
from .get_info import get_peer_info
from .parse import extract_connections

def create_network_graph(nodes_list):
    """Create a NetworkX graph representing the Bitcoin network.
    
    Args:
        nodes_list (list): List of node names to analyze (e.g., ['node_1', 'node_2', ...])
        
    Returns:
        networkx.DiGraph: Directed graph representing the network connections
    """
    G = nx.DiGraph() 
    
    # Adding nodes 
    for node in nodes_list:
        G.add_node(node)
    
    # get peer information for each node
    for node_name in nodes_list:
        print(f"Analysing connections for {node_name}...")
        
        peers_info = get_peer_info(node_name)
        
        if not peers_info:
            continue
            
        connections = extract_connections(peers_info)
        
        for peer_name, connection_type in connections:
            if peer_name and peer_name in nodes_list: 
                G.add_edge(node_name, peer_name, 
                          type=connection_type,
                          color='red' if connection_type == 'manual' else 'blue')
    
    return G

def visualize_network(img_path : str = 'img/bitcoin_network_map.png'):
    """Visualize the Bitcoin network graph and save it as an image.

    Args:
        img_path (str, optional): Path to save the img. Defaults to 'img/bitcoin_network_map.png'.
    """
    nodes = []
    # create a list of nodes to analyze
    with open('docker/data/.env.node_names', 'r') as f:
        nodes_list = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        nodes = nodes_list
    
    # create the network graph
    G = create_network_graph(nodes)
        
    plt.figure(figsize=(12, 8))
    
    # Layout du graphe
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    manual_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'manual']
    inbound_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'inbound']
    
    nx.draw_networkx_edges(G, pos, edgelist=manual_edges, 
                          edge_color='red', alpha=0.8, width=2.5,
                          arrowsize=25, arrowstyle='->',
                          connectionstyle='arc3,rad=0',
                          node_size=1200,
                          label='Outbound connections (manual)')
    
    nx.draw_networkx_edges(G, pos, edgelist=inbound_edges, 
                          edge_color='blue', alpha=0.8, width=2,
                          arrowsize=25, arrowstyle='->',
                            connectionstyle='arc3,rad=0',
                            node_size=1200,
                            label='Inbound connections')

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=1200, alpha=0.9)
    
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title("Bitcoin Network Map", fontsize=16)

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='red', lw=2.5, label='Outbound connections (manual)'),
        Line2D([0], [0], color='blue', lw=2, label='Inbound connections')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    print(f"[DONE ] Network graph saved to {img_path}")