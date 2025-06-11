import tomli
from pathlib import Path
from typing import List, Dict, Any

class ScenarioLoader:
    """A class to load and validate scenarios from TOML files.
    """
    
    def __init__(self, scenarios_dir : str = "./scenarios"):
        """Initialize the ScenarioLoader with the directory containing scenario files.

        Args:
            scenarios_dir (str, optional): path to the scenario dir. Defaults to "./scenarios".
        """
        self.scenarios_dir = Path(scenarios_dir)

    def list_scenarios(self) -> List[str]:
        """List available scenarios"""
        if not self.scenarios_dir.exists():
            return []
        return [f.stem for f in self.scenarios_dir.glob("*.toml")]
    
    def _validator(self, data: Dict[str, Any]) -> bool:
        """Validate the scenario data structure.

        Args:
            data (Dict[str, Any]): The scenario data to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        
        # validate required keys
        required_keys = ["scenario","config", "steps"]
        for key in required_keys:
            if key not in data:
                print(f"[Scenario] Missing required key: {key}")
                return False
        
        # validate config
        required__keys_config = ["default_node","default_wait","timeout"]
        for key in required__keys_config:
            if key not in data["config"]:
                print(f"[Scenario] Missing required config key: {key}")
                return False
        
        # validate steps
        required_keys_steps = ["name", "action"]
        for step in data["steps"]:
            for key in required_keys_steps:
                if key not in data["steps"][step]:
                    print(f"[Scenario] Missing required step key: {key}")
                    return False
        
        return True
        
        
    
    def load_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """Load a scenario from a TOML file.

        Args:
            scenario_name (str): Name of the scenario to load (without .toml extension).

        Returns:
            Dict[str, Any]: Parsed scenario data.
        """
        
        scenario_path = self.scenarios_dir / f"{scenario_name}.toml"
        
        if not scenario_path.exists():
            raise FileNotFoundError(f"Scenario '{scenario_name}' not found in {self.scenarios_dir}")
        
        with open (scenario_path, "rb") as f:
            scenario_data = tomli.load(f)
        
        if not self._validator(scenario_data):
            raise ValueError(f"Invalid scenario data in {scenario_name}.toml")
        
        print(f"[Scenario] Loaded scenario: {scenario_name}")
        return scenario_data