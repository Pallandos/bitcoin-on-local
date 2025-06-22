from unittest.mock import Mock

import pytest
from scenario.actions import ActionExecutor
from scenario.rpc_caller import BitcoinRPC


class TestActionExecutor:
    def setup_method(self):
        """Setup method to initialize mocks for each test."""
        self.mock_rpc = Mock(spec=BitcoinRPC)
        self.executor = ActionExecutor(self.mock_rpc)

    def test_init(self):
        """Test ActionExecutor initialization."""
        rpc = Mock(spec=BitcoinRPC)
        executor = ActionExecutor(rpc)
        assert executor.rpc == rpc

    def test_execute_valid_action(self):
        """Test executing a valid action."""
        self.mock_rpc.call.return_value = "success"

        result = self.executor.execute(
            "create_wallet", "node_1", {"wallet_name": "test_wallet"}
        )

        assert result == "success"
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "createwallet", ["test_wallet"]
        )

    def test_execute_invalid_action(self):
        """Test executing an invalid action raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            self.executor.execute("invalid_action", "node_1")

        assert "Action 'invalid_action' is not supported." in str(exc_info.value)

    def test_execute_no_params(self):
        """Test executing an action without parameters."""
        self.mock_rpc.call.return_value = "success"

        result = self.executor.execute("create_wallet", "node_1")

        assert result == "success"
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "createwallet", ["default_wallet"]
        )

    def test_action_cmd_basic(self):
        """Test _action_cmd with basic command."""
        self.mock_rpc.call.return_value = "command_result"

        result = self.executor._action_cmd("node_1", {"cmd": "getinfo"})

        assert result == "command_result"
        self.mock_rpc.call.assert_called_once_with("node_1", "getinfo", [])

    def test_action_cmd_with_args(self):
        """Test _action_cmd with command and arguments."""
        self.mock_rpc.call.return_value = "command_result"

        result = self.executor._action_cmd("node_1", {"cmd": "getblock hash123 true"})

        assert result == "command_result"
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "getblock", ["hash123", "true"]
        )

    def test_action_cmd_empty_command(self):
        """Test _action_cmd with empty command."""
        self.mock_rpc.call.return_value = "empty_result"

        result = self.executor._action_cmd("node_1", {"cmd": ""})

        assert result == "empty_result"
        self.mock_rpc.call.assert_called_once_with("node_1", "", [])

    def test_action_cmd_no_params(self):
        """Test _action_cmd with no params."""
        self.mock_rpc.call.return_value = "default_result"

        result = self.executor._action_cmd("node_1")

        assert result == "default_result"
        self.mock_rpc.call.assert_called_once_with("node_1", "", [])

    def test_action_create_wallet_with_name(self):
        """Test _action_create_wallet with custom wallet name."""
        self.mock_rpc.call.return_value = {"name": "custom_wallet"}

        result = self.executor._action_create_wallet(
            "node_1", {"wallet_name": "custom_wallet"}
        )

        assert result == {"name": "custom_wallet"}
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "createwallet", ["custom_wallet"]
        )

    def test_action_create_wallet_default_name(self):
        """Test _action_create_wallet with default wallet name."""
        self.mock_rpc.call.return_value = {"name": "default_wallet"}

        result = self.executor._action_create_wallet("node_1")

        assert result == {"name": "default_wallet"}
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "createwallet", ["default_wallet"]
        )

    def test_action_create_address_with_params(self):
        """Test _action_create_address with custom parameters."""
        self.mock_rpc.call.return_value = "bc1qaddress123"

        result = self.executor._action_create_address(
            "node_1", {"label": "test_label", "address_type": "legacy"}
        )

        assert result == "bc1qaddress123"
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "getnewaddress", ["test_label", "legacy"]
        )

    def test_action_create_address_default_params(self):
        """Test _action_create_address with default parameters."""
        self.mock_rpc.call.return_value = "bc1qaddress456"

        result = self.executor._action_create_address("node_1")

        assert result == "bc1qaddress456"
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "getnewaddress", ["", "bech32"]
        )

    def test_action_send_to_with_params(self):
        """Test _action_send_to with custom parameters."""
        self.mock_rpc.call.return_value = "txid123"

        result = self.executor._action_send_to(
            "node_1", {"to": "bc1qrecipient123", "amount": 0.5}
        )

        assert result == "txid123"
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "sendtoaddress", ["bc1qrecipient123", 0.5]
        )

    def test_action_send_to_default_params(self):
        """Test _action_send_to with default parameters."""
        self.mock_rpc.call.return_value = "txid456"

        result = self.executor._action_send_to("node_1")

        assert result == "txid456"
        self.mock_rpc.call.assert_called_once_with("node_1", "sendtoaddress", ["", 0.0])

    def test_action_mine_with_params(self):
        """Test _action_mine with custom parameters."""
        self.mock_rpc.call.return_value = ["block_hash_1", "block_hash_2"]

        result = self.executor._action_mine(
            "node_1", {"amount": 2, "address": "bc1qminer123"}
        )

        assert result == ["block_hash_1", "block_hash_2"]
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "generatetoaddress", [2, "bc1qminer123"]
        )

    def test_action_mine_default_amount(self):
        """Test _action_mine with default amount."""
        self.mock_rpc.call.return_value = ["block_hash_1"]

        result = self.executor._action_mine("node_1", {"address": "bc1qminer456"})

        assert result == ["block_hash_1"]
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "generatetoaddress", [1, "bc1qminer456"]
        )

    def test_action_mine_no_address(self):
        """Test _action_mine without address parameter."""
        self.mock_rpc.call.return_value = ["block_hash_1"]

        result = self.executor._action_mine("node_1", {"amount": 1})

        assert result == ["block_hash_1"]
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "generatetoaddress", [1, None]
        )

    def test_execute_all_supported_actions(self):
        """Test that all implemented actions can be executed."""
        supported_actions = [
            "cmd",
            "create_wallet",
            "create_address",
            "send_to",
            "mine",
        ]

        for action in supported_actions:
            self.mock_rpc.call.return_value = f"result_for_{action}"
            result = self.executor.execute(action, "node_1", {})
            assert result == f"result_for_{action}"

    def test_action_cmd_single_word_command(self):
        """Test _action_cmd with single word command."""
        self.mock_rpc.call.return_value = "single_word_result"

        result = self.executor._action_cmd("node_1", {"cmd": "help"})

        assert result == "single_word_result"
        self.mock_rpc.call.assert_called_once_with("node_1", "help", [])

    def test_action_cmd_multiple_spaces(self):
        """Test _action_cmd with command containing multiple consecutive spaces."""
        self.mock_rpc.call.return_value = "multi_space_result"

        result = self.executor._action_cmd(
            "node_1", {"cmd": "getblock  hash123   true"}
        )

        assert result == "multi_space_result"
        # Should still parse correctly despite extra spaces
        self.mock_rpc.call.assert_called_once_with(
            "node_1", "getblock", ["", "hash123", "", "", "true"]
        )

    def test_params_none_handling(self):
        """Test that all action methods handle params=None correctly."""
        actions_to_test = [
            ("cmd", "createwallet", ["default_wallet"]),
            ("create_wallet", "createwallet", ["default_wallet"]),
            ("create_address", "getnewaddress", ["", "bech32"]),
            ("send_to", "sendtoaddress", ["", 0.0]),
            ("mine", "generatetoaddress", [1, None]),
        ]

        for action, expected_method, expected_args in actions_to_test:
            self.mock_rpc.call.return_value = "test_result"
            result = self.executor.execute(action, "node_1", None)

            assert result == "test_result"
            if action == "cmd":
                # Special case for cmd action with empty command
                self.mock_rpc.call.assert_called_with("node_1", "", [])
            else:
                self.mock_rpc.call.assert_called_with(
                    "node_1", expected_method, expected_args
                )

            self.mock_rpc.call.reset_mock()
