import time
from .loader import ScenarioLoader
from .rpc_caller import BitcoinRPC
from .actions import ActionExecutor
from typing import Dict, Any, List

# Error classes for ScenarioRunner
class ScenarioRunnerError(Exception):
    """Base class for all scenario runner errors."""
    pass
class ScenarioNotLoadedError(ScenarioRunnerError):
    """Raised when a scenario is tried to be runned but not loaded."""
    def __init__(self, scenario_name: str):
        super().__init__("No scenario loaded. Please load a scenario first.")

class ScenarioRunner:
    """ScenarioRunner is a class that manages the execution of Bitcoin scenarios.
    """
    def __init__(self,
                 rpc_user : str,
                 rpc_password : str,
                 scenarios_dir : str = "./scenarios",
                 base_port : int = 18443,
                 ):
        
        self.loader = ScenarioLoader(scenarios_dir)
        self.variables = {} # Store scenario variables
        
        rpc = BitcoinRPC(rpc_user, rpc_password, base_port)
        self.executor = ActionExecutor(rpc)
    
    def load_scenario(self, scenario_name : str):
        
        self.scenario = self.loader.load_scenario(scenario_name)
        self.config = self.scenario["config"] # so we dont have to load it again
        
        # print infos :
        print("==========================================")
        print(f"Name: {self.scenario['scenario']['name']} \n")
        print(f"Description: {self.scenario['scenario']['description']}\n")
        print(f"Written by: {self.scenario['scenario']['author']}\n")
        print(f"Date: {self.scenario['scenario']['date']}")
        print("==========================================")
    
    def list_scenarios(self):
        """List available scenarios"""
        print("Available scenarios:")
        scenarios = self.loader.list_scenarios()
        print("\n".join(scenarios) if scenarios else "No scenarios found.")
    
    def _substitute_variables(self, params: Any) -> Any:
        """Replace ${var} with actual values"""
        if isinstance(params, str):
            for var_name, var_value in self.variables.items():
                params = params.replace(f"${{{var_name}}}", str(var_value))
            return params
        elif isinstance(params, dict):
            return {k: self._substitute_variables(v) for k, v in params.items()}
        elif isinstance(params, list):
            return [self._substitute_variables(item) for item in params]
        return params
    
    # ==== runners ====
    
    def _run_step(self, step: Dict[str , Any]) -> None:
        
        # exctract actions details
        # → the scenario is valid so we can assume that the step has the required keys
        action_name = step["name"]
        action = step["action"]
        node = step.get("node", self.config["default_node"])
        args = self._substitute_variables(step.get("args", {}))
        
        # execute the action
        print(f"Running step: {action_name} (on node: {node})")
        result = self.executor.execute(action, node, args)
        
        # == deal with options ==
        if step.get("print", False):
            print(f"Result: \n → {result} \n")
        if args.get("store_result",""):
            # store the result in the variables dict
            var_name = args.get("store_result")
            self.variables[var_name] = result
            print(f"Stored result in variable: {var_name} = {result}")
        
        # time and wait
        time.sleep(step.get("wait_after", self.config["default_wait"]))
    
    def run_scenario(self) -> None:
        """Run the loaded scenario step by step"""
        if not hasattr(self, 'scenario'):
            raise ScenarioNotLoadedError()
        
        print(f"[SCENARIO] Running scenario: {self.scenario['scenario']['name']}")
        
        # timeout sleep:
        time.sleep(self.config.get("timeout"))
        
        for i, ststep_name in enumerate(self.scenario["steps"]):
            print(f"\n[SCENARIO] Step {i + 1}/{len(self.scenario['steps'])}")
            step = self.scenario["steps"][ststep_name]
            
            try:
                self._run_step(step)
            except Exception as e:
                print(f"[ERROR] An error occurred while running step '{ststep_name}': {e}")
                raise e
        
        print("[SCENARIO] Scenario execution completed.")