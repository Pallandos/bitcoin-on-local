from unittest.mock import patch
from network_info import extract_connections


class TestExtractConnections:
    def test_extract_connections_basic(self):
        peers_info = [
            {
                "addr": "192.168.1.1:8333",
                "connection_type": "outbound-full-relay",
                "addrbind": "172.20.0.5:8333",
            },
            {
                "addr": "10.0.0.1:8333",
                "connection_type": "inbound",
                "addrbind": "172.20.0.5:8333",
            },
        ]

        result = extract_connections(peers_info)
        expected = [("192.168.1.1", "outbound-full-relay"), ("10.0.0.1", "inbound")]
        assert result == expected

    @patch("network_info.parse._docker_dns")
    def test_extract_connections_with_docker_dns(self, mock_docker_dns):
        mock_docker_dns.return_value = "bitcoin-node-1"

        peers_info = [
            {
                "addr": "172.20.0.7:8333",
                "connection_type": "outbound-full-relay",
                "addrbind": "172.20.0.5:8333",
            }
        ]

        result = extract_connections(peers_info)
        expected = [("bitcoin-node-1", "outbound-full-relay")]
        assert result == expected
        mock_docker_dns.assert_called_once_with("172.20.0.7")

    def test_extract_connections_missing_fields(self):
        peers_info = [
            {
                "addr": "192.168.1.1:8333",
                "connection_type": "outbound-full-relay",
                # missing addrbind
            },
            {
                "connection_type": "inbound",
                "addrbind": "172.20.0.5:8333",
                # missing addr
            },
        ]

        result = extract_connections(peers_info)
        assert result == []

    def test_extract_connections_default_connection_type(self):
        peers_info = [
            {
                "addr": "192.168.1.1:8333",
                "addrbind": "172.20.0.5:8333",
                # missing connection_type
            }
        ]

        result = extract_connections(peers_info)
        expected = [("192.168.1.1", "unknown")]
        assert result == expected

    def test_extract_connections_empty_list(self):
        result = extract_connections([])
        assert result == []

    def test_extract_connections_empty_addr(self):
        peers_info = [
            {
                "addr": "",
                "connection_type": "outbound-full-relay",
                "addrbind": "172.20.0.5:8333",
            }
        ]

        result = extract_connections(peers_info)
        assert result == []

    @patch("network_info.parse._docker_dns")
    def test_extract_connections_docker_dns_returns_none(self, mock_docker_dns):
        mock_docker_dns.return_value = None

        peers_info = [
            {
                "addr": "172.20.0.7:8333",
                "connection_type": "outbound-full-relay",
                "addrbind": "172.20.0.5:8333",
            }
        ]

        result = extract_connections(peers_info)
        expected = [(None, "outbound-full-relay")]
        assert result == expected
