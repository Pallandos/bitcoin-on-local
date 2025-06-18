import unittest
from unittest.mock import patch, MagicMock
import subprocess
from network_info import get_peer_info


class TestGetPeerInfo(unittest.TestCase):
    
    @patch('network_info.get_info.subprocess.run')
    def test_get_peer_info_success(self, mock_run):
        """Test successful execution of get_peer_info."""
        mock_result = MagicMock()
        mock_result.stdout = '[{"id": 1, "addr": "127.0.0.1:8333"}]'
        mock_run.return_value = mock_result
        
        result = get_peer_info("node_1")
        
        mock_run.assert_called_once_with(
            ["./bit-cli.sh", "node_1", "getpeerinfo"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(result, [{"id": 1, "addr": "127.0.0.1:8333"}])
    
    @patch('network_info.get_info.subprocess.run')
    def test_get_peer_info_empty_response(self, mock_run):
        """Test get_peer_info with empty response."""
        mock_result = MagicMock()
        mock_result.stdout = '[]'
        mock_run.return_value = mock_result
        
        result = get_peer_info("node_1")
        
        self.assertEqual(result, [])
    
    @patch('network_info.get_info.subprocess.run')
    @patch('builtins.print')
    def test_get_peer_info_subprocess_error(self, mock_print, mock_run):
        """Test get_peer_info when subprocess raises an exception."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
        
        result = get_peer_info("node_1")
        
        self.assertEqual(result, [])
        mock_print.assert_called_once()
    
    @patch('network_info.get_info.subprocess.run')
    @patch('builtins.print')
    def test_get_peer_info_json_decode_error(self, mock_print, mock_run):
        """Test get_peer_info when JSON decoding fails."""
        mock_result = MagicMock()
        mock_result.stdout = 'invalid json'
        mock_run.return_value = mock_result
        
        result = get_peer_info("node_1")
        
        self.assertEqual(result, [])
        mock_print.assert_called_once()
    
    @patch('network_info.get_info.subprocess.run')
    def test_get_peer_info_with_different_node_names(self, mock_run):
        """Test get_peer_info with different node names."""
        mock_result = MagicMock()
        mock_result.stdout = '[]'
        mock_run.return_value = mock_result
        
        for node_name in ["node_1", "node_2", "test_node"]:
            get_peer_info(node_name)
            mock_run.assert_called_with(
                ["./bit-cli.sh", node_name, "getpeerinfo"],
                capture_output=True,
                text=True,
                check=True
            )


if __name__ == '__main__':
    unittest.main()
