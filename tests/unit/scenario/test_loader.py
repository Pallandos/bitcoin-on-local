import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from scenario import ScenarioLoader


class TestScenarioLoader:
    def test_init_default_path(self):
        """Test ScenarioLoader initialization with default path."""
        loader = ScenarioLoader()
        assert loader.scenarios_dir == Path("./scenariosss") # just for testing purposes

    def test_init_custom_path(self):
        """Test ScenarioLoader initialization with custom path."""
        custom_path = "/custom/scenarios"
        loader = ScenarioLoader(custom_path)
        assert loader.scenarios_dir == Path(custom_path)

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.glob')
    def test_list_scenarios_success(self, mock_glob, mock_exists):
        """Test successful listing of scenarios."""
        mock_exists.return_value = True
        
        # Mock scenario files
        mock_files = [
            MagicMock(stem="scenario1"),
            MagicMock(stem="scenario2"),
            MagicMock(stem="test_scenario")
        ]
        mock_glob.return_value = mock_files
        
        loader = ScenarioLoader()
        scenarios = loader.list_scenarios()
        
        assert scenarios == ["scenario1", "scenario2", "test_scenario"]
        mock_glob.assert_called_once_with("*.toml")

    @patch('pathlib.Path.exists')
    def test_list_scenarios_directory_not_exists(self, mock_exists):
        """Test listing scenarios when directory doesn't exist."""
        mock_exists.return_value = False
        
        loader = ScenarioLoader()
        scenarios = loader.list_scenarios()
        
        assert scenarios == []

    def test_validator_valid_data(self):
        """Test validator with valid scenario data."""
        valid_data = {
            "scenario": {"name": "test"},
            "config": {
                "default_node": "node1",
                "default_wait": 5,
                "timeout": 30
            },
            "steps": {
                "step1": {
                    "name": "test_step",
                    "action": "test_action"
                }
            }
        }
        
        assert ScenarioLoader._validator(valid_data) is True

    def test_validator_missing_required_key(self):
        """Test validator with missing required key."""
        invalid_data = {
            "config": {
                "default_node": "node1",
                "default_wait": 5,
                "timeout": 30
            },
            "steps": {}
        }
        # Missing "scenario" key
        
        with patch('builtins.print') as mock_print:
            result = ScenarioLoader._validator(invalid_data)
            assert result is False
            mock_print.assert_called_with("[Scenario] Missing required key: scenario")

    def test_validator_missing_config_key(self):
        """Test validator with missing config key."""
        invalid_data = {
            "scenario": {"name": "test"},
            "config": {
                "default_node": "node1",
                "default_wait": 5
                # Missing "timeout"
            },
            "steps": {
                "step1": {
                    "name": "test_step",
                    "action": "test_action"
                }
            }
        }
        
        with patch('builtins.print') as mock_print:
            result = ScenarioLoader._validator(invalid_data)
            assert result is False
            mock_print.assert_called_with("[Scenario] Missing required config key: timeout")

    def test_validator_missing_step_key(self):
        """Test validator with missing step key."""
        invalid_data = {
            "scenario": {"name": "test"},
            "config": {
                "default_node": "node1",
                "default_wait": 5,
                "timeout": 30
            },
            "steps": {
                "step1": {
                    "name": "test_step"
                    # Missing "action"
                }
            }
        }
        
        with patch('builtins.print') as mock_print:
            result = ScenarioLoader._validator(invalid_data)
            assert result is False
            mock_print.assert_called_with("[Scenario] Missing required step key: action")

    @patch('pathlib.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('tomli.load')
    @patch('scenario.loader.ScenarioLoader._validator')
    @patch('builtins.print')
    def test_load_scenario_success(self, mock_print, mock_validator, mock_tomli_load, mock_file, mock_exists):
        """Test successful scenario loading."""
        mock_exists.return_value = True
        mock_validator.return_value = True
        
        scenario_data = {
            "scenario": {"name": "test"},
            "config": {"default_node": "node1", "default_wait": 5, "timeout": 30},
            "steps": {"step1": {"name": "test_step", "action": "test_action"}}
        }
        mock_tomli_load.return_value = scenario_data
        
        loader = ScenarioLoader()
        result = loader.load_scenario("test_scenario")
        
        assert result == scenario_data
        mock_print.assert_called_with("[Scenario] Loaded scenario: test_scenario")
        mock_file.assert_called_once()

    @patch('pathlib.Path.exists')
    def test_load_scenario_file_not_found(self, mock_exists):
        """Test loading scenario when file doesn't exist."""
        mock_exists.return_value = False
        
        loader = ScenarioLoader()
        
        with pytest.raises(FileNotFoundError, match="Scenario 'nonexistent' not found"):
            loader.load_scenario("nonexistent")

    @patch('pathlib.Path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('tomli.load')
    @patch('scenario.loader.ScenarioLoader._validator')
    def test_load_scenario_invalid_data(self, mock_validator, mock_tomli_load, mock_file, mock_exists):
        """Test loading scenario with invalid data."""
        mock_exists.return_value = True
        mock_validator.return_value = False
        mock_tomli_load.return_value = {"invalid": "data"}
        
        loader = ScenarioLoader()
        
        with pytest.raises(ValueError, match="Invalid scenario data in invalid_scenario.toml"):
            loader.load_scenario("invalid_scenario")