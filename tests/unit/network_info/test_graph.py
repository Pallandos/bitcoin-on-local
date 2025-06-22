from unittest.mock import patch

import networkx as nx
from network_info import graph


class TestCreateNetworkGraph:
    @patch("network_info.graph.get_peer_info")
    @patch("network_info.graph.extract_connections")
    def test_create_network_graph_basic(
        self, mock_extract_connections, mock_get_peer_info
    ):
        """
        Test that create_network_graph creates a directed graph with correct nodes and edges,
        and that edge attributes are set according to connection type.
        """
        nodes_list = ["node1", "node2", "node3"]
        # Simulate peer info for each node
        mock_get_peer_info.side_effect = ["peerinfo1", "peerinfo2", "peerinfo3"]
        # Simulate connections for each node
        mock_extract_connections.side_effect = [
            [("node2", "manual"), ("node3", "inbound")],
            [("node1", "inbound")],
            [],
        ]
        G = graph.create_network_graph(nodes_list)
        assert isinstance(G, nx.DiGraph)
        # Check nodes
        assert set(G.nodes) == set(nodes_list)
        # Check edges and attributes
        assert G.has_edge("node1", "node2")
        assert G.has_edge("node1", "node3")
        assert G.has_edge("node2", "node1")
        assert G["node1"]["node2"]["type"] == "manual"
        assert G["node1"]["node2"]["color"] == "red"
        assert G["node1"]["node3"]["type"] == "inbound"
        assert G["node1"]["node3"]["color"] == "blue"
        assert G["node2"]["node1"]["type"] == "inbound"
        assert G["node2"]["node1"]["color"] == "blue"
        # node3 has no outgoing edges
        assert list(G.successors("node3")) == []

    @patch("network_info.graph.get_peer_info")
    @patch("network_info.graph.extract_connections")
    def test_create_network_graph_ignores_unknown_peers(
        self, mock_extract_connections, mock_get_peer_info
    ):
        """
        Test that create_network_graph ignores peers not present in the nodes_list.
        """
        nodes_list = ["node1", "node2"]
        mock_get_peer_info.return_value = "peerinfo"
        # Peer not in nodes_list should not be added as edge
        mock_extract_connections.return_value = [("unknown_node", "manual")]
        G = graph.create_network_graph(nodes_list)
        assert set(G.nodes) == set(nodes_list)
        assert G.number_of_edges() == 0

    @patch("network_info.graph.get_peer_info")
    @patch("network_info.graph.extract_connections")
    def test_create_network_graph_skips_empty_peers(
        self, mock_extract_connections, mock_get_peer_info
    ):
        """
        Test that create_network_graph skips nodes with no peer information.
        """
        nodes_list = ["node1"]
        mock_get_peer_info.return_value = None
        G = graph.create_network_graph(nodes_list)
        assert set(G.nodes) == set(nodes_list)
        assert G.number_of_edges() == 0

    @patch("network_info.graph.get_peer_info")
    @patch("network_info.graph.extract_connections")
    def test_create_network_graph_none_peer_name(
        self, mock_extract_connections, mock_get_peer_info
    ):
        """
        Test that create_network_graph does not create edges when peer_name is None.
        """
        nodes_list = ["node1", "node2"]
        mock_get_peer_info.return_value = "peerinfo"
        # None peer_name should not create edge
        mock_extract_connections.return_value = [(None, "manual")]
        G = graph.create_network_graph(nodes_list)
        assert set(G.nodes) == set(nodes_list)
        assert G.number_of_edges() == 0


class TestVisualizeNetwork:
    @patch("network_info.graph.create_network_graph")
    @patch("network_info.graph.open", create=True)
    @patch("matplotlib.pyplot.savefig")
    def test_visualize_network_runs(
        self, mock_savefig, mock_open, mock_create_network_graph
    ):
        """
        Test that visualize_network runs without errors and saves the image file.
        """
        # Mock file reading for node names
        mock_open.return_value.__enter__.return_value = [
            "node1\n",
            "node2\n",
            "#comment\n",
            "\n",
        ]
        # Mock graph
        G = nx.DiGraph()
        G.add_node("node1")
        G.add_node("node2")
        G.add_edge("node1", "node2", type="manual")
        mock_create_network_graph.return_value = G
        # Should not raise
        graph.visualize_network("test_img.png")
        mock_savefig.assert_called_once()
