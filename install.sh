#!/bin/bash
set -euo pipefail

# ==== Variables ====
BGREEN='\033[1;32m'
BRED='\033[1;31m'
BYELLOW='\033[1;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPENDENCIES=(
    "docker"
    "python3"
)
SCRIPTS=(
    "bitcoin-on-local.sh"
    "bit-cli.sh"
    "./script/bit-logs.sh"
    "./script/scenario.sh"
)

# ==== Functions ====
function print_ok() {
    echo -e "${BGREEN}[OKAY]${NC} $1"
}

function print_error() {
    echo -e "${BRED}[ERROR]${NC} $1"
}

function print_warning() {
    echo -e "${BYELLOW}[WARNING]${NC} $1"
}

function check_dependencies() {
    local FAILURE=0

    for dep in "${DEPENDENCIES[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            print_error "Dependency '$dep' is not installed. Please install it."
            FAILURE=1
        else
            print_ok "Dependency '$dep' is installed."
        fi
    done
    if [[ $FAILURE -ne 0 ]]; then
        print_error "Please install the missing dependencies and try again."
        exit 1
    fi
}

function set_up_python(){

    # ceate venv
    if [[ ! -d "$SCRIPT_DIR/.venv" ]]; then
        python3 -m venv "$SCRIPT_DIR/.venv"
    else
        print_warning "Using existing virtual environment at $SCRIPT_DIR/.venv"
        # shellcheck disable=SC1091
        source "$SCRIPT_DIR/.venv/bin/activate"
    fi

    print_ok "Python virtual environment is set up."
}

function install_requirements() {
    if [[ -f "$SCRIPT_DIR/requirements.txt" ]]; then
        pip install -r "$SCRIPT_DIR/requirements.txt"
        print_ok "Python requirements installed."
    else
        print_error "requirements.txt not found in $SCRIPT_DIR."
        exit 1
    fi
}

function grant_permissions() {
    for script in "${SCRIPTS[@]}"; do
        if [[ -f "$SCRIPT_DIR/$script" ]]; then
            chmod +x "$SCRIPT_DIR/$script"
        else
            print_warning "Script $script not found in $SCRIPT_DIR."
        fi
    done

    print_ok "Permissions granted to scripts."
}

# ==== Main logic ====
echo "========| Bitcoin on local by Pallandos |========"
echo "[INFO] Starting installation script..."
echo "[INFO] Checking dependencies..."
check_dependencies
echo "[INFO] Setting up Python virtual environment..."
set_up_python
echo "[INFO] Installing Python requirements..."
install_requirements
echo "[INFO] Granting permissions to scripts..."
grant_permissions

print_ok "Installation completed successfully!"
./bitcoin-on-local.sh help