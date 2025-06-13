from scenario import ScenarioRunner
import argparse
import sys
from config import (
    RPC_USER,
    RPC_PASSWORD,
    NODE_BASE_RPC_PORT,
    SCENARIO_PATH,
)

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"[ERROR] {message}")
        self.print_help()
        sys.exit(2)


def main():
    runner = ScenarioRunner(
        rpc_user=RPC_USER,
        rpc_password=RPC_PASSWORD,
        base_port=NODE_BASE_RPC_PORT,
        scenarios_dir=SCENARIO_PATH,
    )
    
    # === args ===
    parser = CustomArgumentParser(description="Scenario Runner : run scenarios described in TOML files",
                                  prog='bitcoin-on-local.sh scenario',)   
    parser.add_argument('command',
                        choices = ['list', 'run'],
                        help='Command : list | run')
    parser.add_argument('scenario',
                        nargs='?',
                        help='Scenario name to run (only required for "run" command)')
    
    args = parser.parse_args()
    
    # === Main logic ===
    if args.command == 'list':
        runner.list_scenarios()
    elif args.command == 'run':
        if not args.scenario:
            print("[ERROR] Scenario name is required for 'run' command.")
            sys.exit(1)
        runner.load_scenario(args.scenario)
        runner.run_scenario()
    else:
        print(f"[ERROR] Unknown command: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()