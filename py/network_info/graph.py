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
    G = nx.DiGraph()  # Graphe dirigé pour distinguer entrant/sortant
    
    # Ajoute tous les nœuds au graphe
    for node in nodes_list:
        G.add_node(node)
    
    # Pour chaque nœud, récupère ses connexions
    for node_name in nodes_list:
        print(f"Analysing connections for {node_name}...")
        
        # Récupère les infos des peers de ce nœud
        peers_info = get_peer_info(node_name)
        
        if not peers_info:
            continue
            
        # Extrait les connexions (peer_name, connection_type)
        connections = extract_connections(peers_info)
        
        # Ajoute les arêtes au graphe
        for peer_name, connection_type in connections:
            if peer_name and peer_name in nodes_list:  # Vérifie que le peer est dans notre liste
                # Ajoute l'arête avec les métadonnées
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
        nodes_list = [line.strip() for line in f if line.strip()]
        nodes = nodes_list
    
    # create the network graph
    G = create_network_graph(nodes)
        
    plt.figure(figsize=(12, 8))
    
    # Layout du graphe
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Dessine les nœuds
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=1500, alpha=0.9)
    
    # Dessine les arêtes par type
    manual_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'manual']
    inbound_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('type') == 'inbound']
    
    nx.draw_networkx_edges(G, pos, edgelist=manual_edges, 
                          edge_color='red', alpha=0.8, width=2.5,
                          arrowsize=25, arrowstyle='->',
                          connectionstyle='arc3,rad=0.1',
                          label='Outbound connections (manual)')
    
    nx.draw_networkx_edges(G, pos, edgelist=inbound_edges, 
                          edge_color='blue', alpha=0.8, width=2,
                          arrowsize=25, arrowstyle='->',
                            connectionstyle='arc3,rad=0.1',
                            label='Inbound connections')
    
    # Ajoute les labels des nœuds
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.title("Bitcoin Network Map", fontsize=16)
    plt.legend()
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(img_path, dpi=300, bbox_inches='tight')