import json
from unittest.mock import Mock, patch

import pytest
import requests
from scenario.rpc_caller import BitcoinRPC, BitcoinRPCError, RPCUnexpectedResponseError


class TestBitcoinRPC:
    def test_init_default_port(self):
        rpc = BitcoinRPC("user", "password")
        assert rpc.rpc_user == "user"
        assert rpc.rpc_password == "password"
        assert rpc.base_port == 18443

    def test_init_custom_port(self):
        rpc = BitcoinRPC("user", "password", 19443)
        assert rpc.base_port == 19443

    @patch("requests.post")
    def test_call_successful_request(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success", "error": None}
        mock_post.return_value = mock_response

        rpc = BitcoinRPC("user", "password")
        result = rpc.call("node_1", "getinfo")

        assert result == "success"
        mock_post.assert_called_once()

        # Verify the request was made with correct parameters
        call_args = mock_post.call_args
        assert call_args[1]["auth"] == ("user", "password")
        assert call_args[1]["timeout"] == 10
        assert "http://localhost:18443" in call_args[0]

    @patch("requests.post")
    def test_call_with_params(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success", "error": None}
        mock_post.return_value = mock_response

        rpc = BitcoinRPC("user", "password")
        result = rpc.call("node_2", "getblock", ["hash123"])

        assert result == "success"

        # Verify payload contains params
        call_args = mock_post.call_args
        payload = json.loads(call_args[1]["data"])
        assert payload["params"] == ["hash123"]
        assert payload["method"] == "getblock"

    def test_port_calculation(self):
        rpc = BitcoinRPC("user", "password", 18443)

        with patch("requests.post") as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {"result": "success", "error": None}
            mock_post.return_value = mock_response

            # Test different node numbers
            rpc.call("node_1", "getinfo")
            assert "http://localhost:18443" in mock_post.call_args[0][0]

            rpc.call("node_2", "getinfo")
            assert "http://localhost:18445" in mock_post.call_args[0][0]

            rpc.call("node_3", "getinfo")
            assert "http://localhost:18447" in mock_post.call_args[0][0]

    @patch("requests.post")
    def test_call_rpc_error(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "result": None,
            "error": {"message": "Invalid method"},
        }
        mock_post.return_value = mock_response

        rpc = BitcoinRPC("user", "password")

        with pytest.raises(BitcoinRPCError) as exc_info:
            rpc.call("node_1", "invalidmethod")

        assert "RPC error on node_1: Invalid method" in str(exc_info.value)

    @patch("requests.post")
    def test_call_connection_error(self, mock_post):
        mock_post.side_effect = requests.ConnectionError("Connection refused")

        rpc = BitcoinRPC("user", "password")

        with pytest.raises(requests.ConnectionError) as exc_info:
            rpc.call("node_1", "getinfo")

        assert "Connection failed to node_1" in str(exc_info.value)

    @patch("requests.post")
    def test_call_timeout_error(self, mock_post):
        mock_post.side_effect = requests.Timeout("Request timeout")

        rpc = BitcoinRPC("user", "password")

        with pytest.raises(requests.Timeout) as exc_info:
            rpc.call("node_1", "getinfo")

        assert "Timeout for node_1" in str(exc_info.value)

    @patch("requests.post")
    def test_call_json_decode_error(self, mock_post):
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)
        mock_post.return_value = mock_response

        rpc = BitcoinRPC("user", "password")

        with pytest.raises(json.JSONDecodeError) as exc_info:
            rpc.call("node_1", "getinfo")

        assert "Invalid JSON response from node_1" in str(exc_info.value)

    @patch("requests.post")
    def test_call_unexpected_error(self, mock_post):
        mock_post.side_effect = ValueError("Unexpected error")

        rpc = BitcoinRPC("user", "password")

        with pytest.raises(RPCUnexpectedResponseError) as exc_info:
            rpc.call("node_1", "getinfo")

        assert "Unexpected response from node_1: Unexpected error" in str(
            exc_info.value
        )

    @patch("requests.post")
    def test_call_no_result_field(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"error": None}
        mock_post.return_value = mock_response

        rpc = BitcoinRPC("user", "password")
        result = rpc.call("node_1", "getinfo")

        assert result is None

    @patch("requests.post")
    def test_call_payload_structure(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success", "error": None}
        mock_post.return_value = mock_response

        rpc = BitcoinRPC("user", "password")
        rpc.call("node_1", "getinfo", ["param1", "param2"])

        # Verify payload structure
        call_args = mock_post.call_args
        payload = json.loads(call_args[1]["data"])

        assert payload["jsonrpc"] == "2.0"
        assert payload["method"] == "getinfo"
        assert payload["params"] == ["param1", "param2"]
        assert payload["id"] == 1

    @patch("requests.post")
    def test_call_headers(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success", "error": None}
        mock_post.return_value = mock_response

        rpc = BitcoinRPC("user", "password")
        rpc.call("node_1", "getinfo")

        # Verify headers
        call_args = mock_post.call_args
        assert call_args[1]["headers"]["content-type"] == "application/json"

    def test_node_name_parsing_edge_cases(self):
        rpc = BitcoinRPC("user", "password")

        with patch("requests.post") as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {"result": "success", "error": None}
            mock_post.return_value = mock_response

            # Test node with multiple underscores
            rpc.call("bitcoin_node_5", "getinfo")
            assert "http://localhost:18451" in mock_post.call_args[0][0]

    @patch("requests.post")
    def test_call_empty_params_default(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success", "error": None}
        mock_post.return_value = mock_response

        rpc = BitcoinRPC("user", "password")
        rpc.call("node_1", "getinfo")

        # Verify params is empty list when not provided
        call_args = mock_post.call_args
        payload = json.loads(call_args[1]["data"])
        assert payload["params"] == []
