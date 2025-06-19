from unittest.mock import Mock, patch

import pytest
from scenario.actions import ActionExecutor
from scenario.loader import ScenarioLoader
from scenario.rpc_caller import BitcoinRPC
from scenario.runner import ScenarioNotLoadedError, ScenarioRunner, ScenarioRunnerError


class TestScenarioRunnerError:
    def test_scenario_runner_error_inheritance(self):
        """Test that ScenarioRunnerError inherits from Exception."""
        error = ScenarioRunnerError("test error")
        assert isinstance(error, Exception)
        assert str(error) == "test error"


class TestScenarioNotLoadedError:
    def test_scenario_not_loaded_error_inheritance(self):
        """Test that ScenarioNotLoadedError inherits from ScenarioRunnerError."""
        error = ScenarioNotLoadedError()
        assert isinstance(error, ScenarioRunnerError)
        assert isinstance(error, Exception)
        assert str(error) == "No scenario loaded. Please load a scenario first."


class TestScenarioRunner:
    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    def test_init_default_parameters(self, mock_loader, mock_rpc, mock_executor):
        """Test ScenarioRunner initialization with default parameters."""
        mock_rpc_instance = Mock()
        mock_rpc.return_value = mock_rpc_instance
        mock_executor_instance = Mock()
        mock_executor.return_value = mock_executor_instance
        mock_loader_instance = Mock()
        mock_loader.return_value = mock_loader_instance

        runner = ScenarioRunner("test_user", "test_password")

        assert runner.variables == {}
        assert runner.scenario is None
        assert runner.config is None
        assert runner.loader == mock_loader_instance
        assert runner.executor == mock_executor_instance

        mock_loader.assert_called_once_with("./scenarios")
        mock_rpc.assert_called_once_with("test_user", "test_password", 18443)
        mock_executor.assert_called_once_with(mock_rpc_instance)

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    def test_init_custom_parameters(self, mock_loader, mock_rpc, mock_executor):
        """Test ScenarioRunner initialization with custom parameters."""
        mock_rpc_instance = Mock()
        mock_rpc.return_value = mock_rpc_instance
        mock_executor_instance = Mock()
        mock_executor.return_value = mock_executor_instance
        mock_loader_instance = Mock()
        mock_loader.return_value = mock_loader_instance

        runner = ScenarioRunner(
            "custom_user",
            "custom_password",
            scenarios_dir="/custom/scenarios",
            base_port=19443,
        )

        assert runner.variables == {}
        assert runner.scenario is None
        assert runner.config is None

        mock_loader.assert_called_once_with("/custom/scenarios")
        mock_rpc.assert_called_once_with("custom_user", "custom_password", 19443)
        mock_executor.assert_called_once_with(mock_rpc_instance)

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    def test_load_scenario(self, mock_print, mock_loader, mock_rpc, mock_executor):
        """Test loading a scenario successfully."""
        mock_scenario = {
            "scenario": {
                "name": "Test Scenario",
                "description": "A test scenario",
                "author": "Test Author",
                "date": "2024-01-01",
            },
            "config": {"default_node": "node_1", "default_wait": 1},
        }

        mock_loader_instance = Mock()
        mock_loader_instance.load_scenario.return_value = mock_scenario
        mock_loader.return_value = mock_loader_instance

        runner = ScenarioRunner("user", "password")
        runner.load_scenario("test_scenario")

        assert runner.scenario == mock_scenario
        assert runner.config == mock_scenario["config"]
        mock_loader_instance.load_scenario.assert_called_once_with("test_scenario")

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    def test_list_scenarios(self, mock_print, mock_loader, mock_rpc, mock_executor):
        """Test listing available scenarios."""
        mock_loader_instance = Mock()
        mock_loader_instance.list_scenarios.return_value = ["scenario1", "scenario2"]
        mock_loader.return_value = mock_loader_instance

        runner = ScenarioRunner("user", "password")
        runner.list_scenarios()

        mock_loader_instance.list_scenarios.assert_called_once()
        mock_print.assert_any_call("Available scenarios:")
        mock_print.assert_any_call("scenario1\nscenario2")

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    def test_list_scenarios_empty(
        self, mock_print, mock_loader, mock_rpc, mock_executor
    ):
        """Test listing scenarios when none are available."""
        mock_loader_instance = Mock()
        mock_loader_instance.list_scenarios.return_value = []
        mock_loader.return_value = mock_loader_instance

        runner = ScenarioRunner("user", "password")
        runner.list_scenarios()

        mock_print.assert_any_call("Available scenarios:")
        mock_print.assert_any_call("No scenarios found.")

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    def test_substitute_variables_string(self, mock_loader, mock_rpc, mock_executor):
        """Test variable substitution with string input."""
        runner = ScenarioRunner("user", "password")
        runner.variables = {"address": "bc1qtest123", "amount": "0.5"}

        result = runner._substitute_variables("Send ${amount} to ${address}")
        assert result == "Send 0.5 to bc1qtest123"

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    def test_substitute_variables_dict(self, mock_loader, mock_rpc, mock_executor):
        """Test variable substitution with dictionary input."""
        runner = ScenarioRunner("user", "password")
        runner.variables = {"address": "bc1qtest123", "amount": "0.5"}

        params = {
            "to": "${address}",
            "amount": "${amount}",
            "comment": "Test transaction",
        }

        result = runner._substitute_variables(params)
        expected = {"to": "bc1qtest123", "amount": "0.5", "comment": "Test transaction"}
        assert result == expected

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    def test_substitute_variables_list(self, mock_loader, mock_rpc, mock_executor):
        """Test variable substitution with list input."""
        runner = ScenarioRunner("user", "password")
        runner.variables = {"node": "node_1", "blocks": "10"}

        params = ["${node}", "${blocks}", "fixed_value"]

        result = runner._substitute_variables(params)
        expected = ["node_1", "10", "fixed_value"]
        assert result == expected

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    def test_substitute_variables_no_variables(
        self, mock_loader, mock_rpc, mock_executor
    ):
        """Test variable substitution with no variables defined."""
        runner = ScenarioRunner("user", "password")
        runner.variables = {}

        result = runner._substitute_variables("No variables here")
        assert result == "No variables here"

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    def test_substitute_variables_non_string_types(
        self, mock_loader, mock_rpc, mock_executor
    ):
        """Test variable substitution with non-string types."""
        runner = ScenarioRunner("user", "password")
        runner.variables = {"test": "value"}

        # Test with integer
        assert runner._substitute_variables(42) == 42

        # Test with float
        assert runner._substitute_variables(3.14) == 3.14

        # Test with boolean
        assert runner._substitute_variables(True) is True

        # Test with None
        assert runner._substitute_variables(None) is None

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    @patch("time.sleep")
    def test_run_step_basic(
        self, mock_sleep, mock_print, mock_loader, mock_rpc, mock_executor
    ):
        """Test running a basic step."""
        mock_executor_instance = Mock()
        mock_executor_instance.execute.return_value = "test_result"
        mock_executor.return_value = mock_executor_instance

        runner = ScenarioRunner("user", "password")
        runner.config = {"default_node": "node_1", "default_wait": 1}

        step = {
            "name": "test_step",
            "action": "create_wallet",
            "args": {"wallet_name": "test_wallet"},
        }

        runner._run_step(step)

        mock_executor_instance.execute.assert_called_once_with(
            "create_wallet", "node_1", {"wallet_name": "test_wallet"}
        )
        mock_sleep.assert_called_once_with(1)

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    @patch("time.sleep")
    def test_run_step_with_custom_node(
        self, mock_sleep, mock_print, mock_loader, mock_rpc, mock_executor
    ):
        """Test running a step with custom node."""
        mock_executor_instance = Mock()
        mock_executor_instance.execute.return_value = "test_result"
        mock_executor.return_value = mock_executor_instance

        runner = ScenarioRunner("user", "password")
        runner.config = {"default_node": "node_1", "default_wait": 1}

        step = {
            "name": "test_step",
            "action": "create_wallet",
            "node": "node_2",
            "args": {"wallet_name": "test_wallet"},
        }

        runner._run_step(step)

        mock_executor_instance.execute.assert_called_once_with(
            "create_wallet", "node_2", {"wallet_name": "test_wallet"}
        )

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    @patch("time.sleep")
    def test_run_step_with_print_option(
        self, mock_sleep, mock_print, mock_loader, mock_rpc, mock_executor
    ):
        """Test running a step with print option enabled."""
        mock_executor_instance = Mock()
        mock_executor_instance.execute.return_value = "test_result"
        mock_executor.return_value = mock_executor_instance

        runner = ScenarioRunner("user", "password")
        runner.config = {"default_node": "node_1", "default_wait": 1}

        step = {
            "name": "test_step",
            "action": "create_wallet",
            "print": True,
            "args": {"wallet_name": "test_wallet"},
        }

        runner._run_step(step)

        mock_print.assert_any_call("Result: \n → test_result \n")

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    @patch("time.sleep")
    def test_run_step_with_store_result(
        self, mock_sleep, mock_print, mock_loader, mock_rpc, mock_executor
    ):
        """Test running a step with store_result option."""
        mock_executor_instance = Mock()
        mock_executor_instance.execute.return_value = "stored_value"
        mock_executor.return_value = mock_executor_instance

        runner = ScenarioRunner("user", "password")
        runner.config = {"default_node": "node_1", "default_wait": 1}

        step = {
            "name": "test_step",
            "action": "create_wallet",
            "args": {"wallet_name": "test_wallet", "store_result": "wallet_result"},
        }

        runner._run_step(step)

        assert runner.variables["wallet_result"] == "stored_value"
        mock_print.assert_any_call(
            "Stored result in variable: wallet_result = stored_value"
        )

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    @patch("time.sleep")
    def test_run_step_with_custom_wait(
        self, mock_sleep, mock_print, mock_loader, mock_rpc, mock_executor
    ):
        """Test running a step with custom wait time."""
        mock_executor_instance = Mock()
        mock_executor_instance.execute.return_value = "test_result"
        mock_executor.return_value = mock_executor_instance

        runner = ScenarioRunner("user", "password")
        runner.config = {"default_node": "node_1", "default_wait": 1}

        step = {
            "name": "test_step",
            "action": "create_wallet",
            "wait_after": 5,
            "args": {"wallet_name": "test_wallet"},
        }

        runner._run_step(step)

        mock_sleep.assert_called_once_with(5)

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    def test_run_scenario_not_loaded(self, mock_loader, mock_rpc, mock_executor):
        """Test running scenario when no scenario is loaded."""
        runner = ScenarioRunner("user", "password")

        with pytest.raises(ScenarioNotLoadedError):
            runner.run_scenario()

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    @patch("time.sleep")
    def test_run_scenario_success(
        self, mock_sleep, mock_print, mock_loader, mock_rpc, mock_executor
    ):
        """Test successful scenario execution."""
        mock_executor_instance = Mock()
        mock_executor_instance.execute.return_value = "success"
        mock_executor.return_value = mock_executor_instance

        runner = ScenarioRunner("user", "password")
        runner.scenario = {
            "scenario": {"name": "Test Scenario"},
            "steps": {
                "step1": {
                    "name": "Create Wallet",
                    "action": "create_wallet",
                    "args": {"wallet_name": "test"},
                },
                "step2": {
                    "name": "Get Info",
                    "action": "cmd",
                    "args": {"cmd": "getinfo"},
                },
            },
        }
        runner.config = {"default_node": "node_1", "default_wait": 1, "timeout": 2}

        runner.run_scenario()

        assert mock_executor_instance.execute.call_count == 2
        mock_print.assert_any_call("[SCENARIO] Running scenario: Test Scenario")
        mock_print.assert_any_call("[SCENARIO] Scenario execution completed.")

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    @patch("time.sleep")
    def test_run_scenario_with_step_error(
        self, mock_sleep, mock_print, mock_loader, mock_rpc, mock_executor
    ):
        """Test scenario execution with step error."""
        mock_executor_instance = Mock()
        mock_executor_instance.execute.side_effect = Exception("Test error")
        mock_executor.return_value = mock_executor_instance

        runner = ScenarioRunner("user", "password")
        runner.scenario = {
            "scenario": {"name": "Test Scenario"},
            "steps": {
                "step1": {
                    "name": "Failing Step",
                    "action": "create_wallet",
                    "args": {"wallet_name": "test"},
                }
            },
        }
        runner.config = {"default_node": "node_1", "default_wait": 1, "timeout": 2}

        with pytest.raises(Exception) as exc_info:
            runner.run_scenario()

        assert "Test error" in str(exc_info.value)
        mock_print.assert_any_call(
            "[ERROR] An error occurred while running step 'step1': Test error"
        )

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    @patch("builtins.print")
    @patch("time.sleep")
    def test_run_scenario_with_timeout(
        self, mock_sleep, mock_print, mock_loader, mock_rpc, mock_executor
    ):
        """Test scenario execution with initial timeout."""
        mock_executor_instance = Mock()
        mock_executor_instance.execute.return_value = "success"
        mock_executor.return_value = mock_executor_instance

        runner = ScenarioRunner("user", "password")
        runner.scenario = {
            "scenario": {"name": "Test Scenario"},
            "steps": {
                "step1": {
                    "name": "Test Step",
                    "action": "create_wallet",
                    "args": {"wallet_name": "test"},
                }
            },
        }
        runner.config = {"default_node": "node_1", "default_wait": 1, "timeout": 5}

        runner.run_scenario()

        # Check that timeout sleep was called
        sleep_calls = mock_sleep.call_args_list
        assert any(call[0][0] == 5 for call in sleep_calls)

    @patch("scenario.runner.ActionExecutor")
    @patch("scenario.runner.BitcoinRPC")
    @patch("scenario.runner.ScenarioLoader")
    def test_run_step_variable_substitution(self, mock_loader, mock_rpc, mock_executor):
        """Test that variable substitution works in step execution."""
        mock_executor_instance = Mock()
        mock_executor_instance.execute.return_value = "success"
        mock_executor.return_value = mock_executor_instance

        runner = ScenarioRunner("user", "password")
        runner.config = {"default_node": "node_1", "default_wait": 1}
        runner.variables = {"wallet_name": "my_wallet"}

        step = {
            "name": "test_step",
            "action": "create_wallet",
            "args": {"wallet_name": "${wallet_name}"},
        }

        with patch("time.sleep"):
            runner._run_step(step)

        mock_executor_instance.execute.assert_called_once_with(
            "create_wallet", "node_1", {"wallet_name": "my_wallet"}
        )
