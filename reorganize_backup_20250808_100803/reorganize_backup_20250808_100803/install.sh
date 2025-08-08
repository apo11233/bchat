#!/bin/bash
# bchat Installation Script
# Deploys bchat system to any workspace (including empty ones)

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BCHAT_VERSION="1.0.0"
MIN_PYTHON_VERSION="3.8"
REQUIRED_NODE_VERSION="16"

# Initialize logging
LOG_FILE="installation.log"
START_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# Create/clear log file
echo "bchat Installation Log - Started at $START_TIME" > "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo -e "${BLUE}🚀 bchat Installation Script v${BCHAT_VERSION}${NC}"
echo -e "${BLUE}=====================================================${NC}"
echo "📋 Installation log: $LOG_FILE"

# Function to print status with logging
print_status() {
    local status=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Print to console
    case $status in
        "info") echo -e "${BLUE}ℹ️  $message${NC}" ;;
        "success") echo -e "${GREEN}✅ $message${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "error") echo -e "${RED}❌ $message${NC}" ;;
    esac
    
    # Log to file
    echo "[$timestamp] [$(echo "$status" | tr '[:lower:]' '[:upper:]')] $message" >> "$LOG_FILE"
}

# Function to log command execution
log_command() {
    local command="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [COMMAND] $command" >> "$LOG_FILE"
}

# Function to check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to validate path safety
validate_path() {
    local path="$1"
    local name="$2"
    
    # Check for basic path safety
    if [[ ! "$path" =~ ^/[a-zA-Z0-9/_.-]+$ ]] && [[ ! "$path" =~ ^[a-zA-Z0-9/_.-]+$ ]]; then
        print_status "error" "Invalid $name path: $path"
        return 1
    fi
    
    # Check for directory traversal attempts
    if [[ "$path" =~ \.\./|/\.\./ ]]; then
        print_status "error" "Path traversal detected in $name: $path"
        return 1
    fi
    
    return 0
}

# Function to create backup of files before overwriting
create_backup() {
    local file="$1"
    if [ -f "$file" ]; then
        local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$file" "$backup"
        print_status "info" "Backup created: $backup"
    fi
}

# Rollback function for cleanup on failure
rollback() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    print_status "warning" "Installation failed, cleaning up..."
    
    echo "[$timestamp] [ROLLBACK] Installation failed, performing cleanup" >> "$LOG_FILE"
    
    # Log cleanup actions
    if [ -f "$WORKSPACE_ROOT/bchat" ]; then
        rm -f "$WORKSPACE_ROOT/bchat"
        echo "[$timestamp] [ROLLBACK] Removed symlink: $WORKSPACE_ROOT/bchat" >> "$LOG_FILE"
    fi
    
    # Restore backups if they exist
    for backup in "$INSTALL_DIR"/*.backup.*; do
        if [ -f "$backup" ]; then
            original="${backup%.backup.*}"
            mv "$backup" "$original"
            echo "[$timestamp] [ROLLBACK] Restored backup: $original" >> "$LOG_FILE"
        fi
    done
    
    echo "[$timestamp] [ROLLBACK] Installation rollback completed" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    echo "Installation failed. Check $LOG_FILE for details." >&2
    exit 1
}

# Function to detect virtual environment and set pip flags
detect_virtual_env() {
    if [[ "$VIRTUAL_ENV" != "" ]] || [[ "$CONDA_DEFAULT_ENV" != "" ]] || python3 -c "import sys; exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>/dev/null; then
        print_status "info" "Virtual environment detected - using venv pip installation"
        PIP_USER_FLAG=""
    else
        print_status "info" "System Python detected - using --user flag"
        PIP_USER_FLAG="--user"
    fi
}

# Set up trap for cleanup on failure
trap rollback ERR

# Get installation directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$INSTALL_DIR/.." && pwd)"

# Log installation paths
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Installation Directory: $INSTALL_DIR" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Workspace Root: $WORKSPACE_ROOT" >> "$LOG_FILE"

# Validate paths
validate_path "$INSTALL_DIR" "installation directory" || exit 1
validate_path "$WORKSPACE_ROOT" "workspace root" || exit 1

echo -e "${YELLOW}📁 Installation Directory: ${INSTALL_DIR}${NC}"
echo -e "${YELLOW}📁 Workspace Root: ${WORKSPACE_ROOT}${NC}"

# Detect virtual environment and set pip flags
detect_virtual_env

# Check system requirements
print_status "info" "Checking system requirements..."

# Check Python
if ! command_exists python3; then
    print_status "error" "Python 3 is required but not installed"
    echo "Please install Python 3.8+ and run this script again"
    exit 1
fi

log_command "python3 -c 'import sys; print(sys.version_info)'"
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
print_status "success" "Python $PYTHON_VERSION found"

# Check Node.js for Gemini CLI
if ! command_exists node; then
    print_status "warning" "Node.js not found - Gemini CLI features will be limited"
    echo "Install Node.js 16+ for full Gemini integration"
else
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -ge "$REQUIRED_NODE_VERSION" ]; then
        print_status "success" "Node.js v$(node --version) found"
    else
        print_status "warning" "Node.js version is old - recommend updating to v16+"
    fi
fi

# Check npm for Gemini CLI installation
if command_exists npm; then
    print_status "info" "Checking for Gemini CLI..."
    if command_exists gemini; then
        print_status "success" "Gemini CLI already installed"
    else
        print_status "info" "Verifying Gemini CLI package..."
        # Verify package exists and get version info
        if npm info @google/gemini-cli version >/dev/null 2>&1; then
            print_status "info" "Installing Gemini CLI..."
            log_command "npm install -g @google/gemini-cli"
            if npm install -g @google/gemini-cli; then
                print_status "success" "Gemini CLI installed successfully"
            else
                print_status "warning" "Failed to install Gemini CLI - manual installation may be required"
            fi
        else
            print_status "warning" "Cannot verify Gemini CLI package - skipping installation"
        fi
    fi
fi

# Create directory structure
print_status "info" "Creating directory structure..."
mkdir -p "$WORKSPACE_ROOT"/{chats,logs}
mkdir -p "$WORKSPACE_ROOT/chats"
print_status "success" "Directories created"

# Install Python dependencies
print_status "info" "Installing Python dependencies..."

# Check if we can write to pip directories
if ! python3 -m pip list >/dev/null 2>&1; then
    print_status "error" "Cannot access pip - check Python installation"
    exit 1
fi

if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    # Validate requirements.txt exists and is readable
    if [ -r "$INSTALL_DIR/requirements.txt" ]; then
        print_status "info" "Installing from requirements.txt with verification..."
        log_command "python3 -m pip install $PIP_USER_FLAG -r $INSTALL_DIR/requirements.txt"
        if python3 -m pip install $PIP_USER_FLAG -r "$INSTALL_DIR/requirements.txt"; then
            print_status "success" "Python dependencies installed"
        else
            print_status "error" "Failed to install Python dependencies"
            print_status "info" "Trying manual installation of core packages..."
            log_command "python3 -m pip install $PIP_USER_FLAG watchdog google-generativeai python-dotenv"
            python3 -m pip install $PIP_USER_FLAG watchdog google-generativeai python-dotenv
        fi
    else
        print_status "error" "Cannot read requirements.txt file"
        exit 1
    fi
else
    print_status "info" "Installing core packages manually..."
    log_command "python3 -m pip install $PIP_USER_FLAG watchdog google-generativeai python-dotenv"
    python3 -m pip install $PIP_USER_FLAG watchdog google-generativeai python-dotenv
    print_status "success" "Core packages installed"
fi

# Copy configuration files
print_status "info" "Setting up configuration..."

# Check write permissions for workspace root
if [ ! -w "$WORKSPACE_ROOT" ]; then
    print_status "error" "No write permission to workspace root: $WORKSPACE_ROOT"
    exit 1
fi

if [ -f "$INSTALL_DIR/config.template.json" ] && [ ! -f "$WORKSPACE_ROOT/config.json" ]; then
    # Validate template file is readable
    if [ -r "$INSTALL_DIR/config.template.json" ]; then
        cp "$INSTALL_DIR/config.template.json" "$WORKSPACE_ROOT/config.json"
        print_status "success" "Configuration file created from template"
    else
        print_status "error" "Cannot read config template file"
        exit 1
    fi
elif [ -f "$INSTALL_DIR/config.json" ] && [ ! -f "$WORKSPACE_ROOT/config.json" ]; then
    if [ -r "$INSTALL_DIR/config.json" ]; then
        cp "$INSTALL_DIR/config.json" "$WORKSPACE_ROOT/config.json"
        print_status "success" "Configuration file copied"
    else
        print_status "error" "Cannot read config file"
        exit 1
    fi
fi

# Make scripts executable
print_status "info" "Making scripts executable..."
chmod +x "$INSTALL_DIR"/*.sh
if [ -f "$INSTALL_DIR/bchat" ]; then
    chmod +x "$INSTALL_DIR/bchat"
    print_status "success" "bchat command ready in bchat directory"
fi

# Create global bchat symlink for easy access from anywhere in workspace
if [ -f "$INSTALL_DIR/bchat" ]; then
    # Create backup if target exists
    create_backup "$WORKSPACE_ROOT/bchat"
    
    # Create symlink
    ln -sf "$INSTALL_DIR/bchat" "$WORKSPACE_ROOT/bchat"
    print_status "success" "bchat linked to workspace root for global access"
fi

# Create bchat executables inside bchat directory
print_status "info" "Setting up bchat executables..."

# Validate script directory is writable
if [ ! -w "$INSTALL_DIR" ]; then
    print_status "error" "No write permission to installation directory: $INSTALL_DIR"
    exit 1
fi

# Create rchat (short command for running bchat)
create_backup "$INSTALL_DIR/rchat"
cat > "$INSTALL_DIR/rchat" << 'EOF'
#!/bin/bash
# bchat Launcher Script - Short Command
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/src/chat_monitor.py" ]; then
    cd "$SCRIPT_DIR"
    python3 src/chat_monitor.py "$@"
elif [ -f "$SCRIPT_DIR/src/main.py" ]; then
    cd "$SCRIPT_DIR" 
    python3 src/main.py "$@"
else
    echo "bchat not found. Please check installation."
    exit 1
fi
EOF
chmod +x "$INSTALL_DIR/rchat"

# Create runchat (alias for rchat)
create_backup "$INSTALL_DIR/runchat"
ln -sf "$INSTALL_DIR/rchat" "$INSTALL_DIR/runchat"

print_status "success" "bchat executables created: rchat, runchat"

# Setup environment variables
print_status "info" "Checking API key configuration..."
if [ -z "$GOOGLE_API_KEY" ] && [ -z "$GEMINI_API_KEY" ]; then
    print_status "warning" "No API keys found in environment"
    echo ""
    echo "To enable full functionality, set your API keys:"
    echo "  export GOOGLE_API_KEY='your-gemini-api-key'"
    echo "  export GEMINI_API_KEY='your-gemini-api-key'"
    echo ""
    echo "Add these to your ~/.bashrc, ~/.zshrc, or .env file"
else
    print_status "success" "API keys found in environment"
fi

# Create VSCode tasks.json for auto-startup
if [ -d "$WORKSPACE_ROOT/.vscode" ] || [ -f "$WORKSPACE_ROOT/.vscode/tasks.json" ]; then
    print_status "info" "Setting up VSCode integration..."
    mkdir -p "$WORKSPACE_ROOT/.vscode"
    
    cat > "$WORKSPACE_ROOT/.vscode/tasks.json" << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start bchat",
            "type": "shell",
            "command": "${workspaceFolder}/bchat",
            "options": {
                "cwd": "${workspaceFolder}"
            },
            "group": "build",
            "presentation": {
                "echo": false,
                "reveal": "never",
                "focus": false,
                "panel": "shared",
                "showReuseMessage": false,
                "clear": false
            },
            "isBackground": true,
            "problemMatcher": [],
            "runOptions": {
                "runOn": "folderOpen"
            }
        }
    ]
}
EOF
    print_status "success" "VSCode tasks.json created for auto-startup"
fi

# Test installation
print_status "info" "Testing installation..."

# Test Python import
if python3 -c "import sys; sys.path.append('$INSTALL_DIR/src'); import chat_monitor" 2>/dev/null; then
    print_status "success" "bchat Python module loads correctly"
else
    print_status "warning" "bchat module test failed - may need manual configuration"
fi

# Test bchat command
if [ -x "$INSTALL_DIR/rchat" ]; then
    if timeout 5s "$INSTALL_DIR/rchat" --help >/dev/null 2>&1; then
        print_status "success" "bchat (rchat) command works"
    else
        print_status "warning" "bchat test timed out - may need API key configuration"
    fi
fi

# Create start script inside bchat directory
create_backup "$INSTALL_DIR/start"
cat > "$INSTALL_DIR/start" << 'EOF'
#!/bin/bash
# Quick start script for bchat
echo "🚀 Starting bchat..."
echo "Press Ctrl+C to stop"

# Check for API key
if [ -z "$GOOGLE_API_KEY" ] && [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Warning: No API key set. Set GOOGLE_API_KEY or GEMINI_API_KEY for full functionality"
fi

# Start bchat using rchat
exec "$(dirname "$0")/rchat"
EOF
chmod +x "$INSTALL_DIR/start"

print_status "success" "Start script created: ./start"

# Installation summary
echo ""
echo -e "${GREEN}🎉 Installation Complete!${NC}"
echo -e "${GREEN}=========================${NC}"
echo ""
echo "📁 Installed to: $WORKSPACE_ROOT"
echo "🔧 Configuration: $WORKSPACE_ROOT/config.json"
echo "📝 Logs directory: $WORKSPACE_ROOT/logs"
echo "💬 Chats directory: $WORKSPACE_ROOT/chats"
echo ""
echo -e "${YELLOW}🚀 Quick Start Commands (from bchat directory):${NC}"
echo "  ./start                    # Start monitoring (quick)"
echo "  ./rchat --help             # Monitor options (short)"
echo "  ./runchat                  # Alternative monitor command"
echo "  ./bchat --help             # Use Gemini CLI"
echo ""
echo -e "${YELLOW}📖 For detailed usage, see:${NC}"
echo "  $INSTALL_DIR/README.md"
echo "  $INSTALL_DIR/docs/"
echo ""

if [ -z "$GOOGLE_API_KEY" ] && [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  Don't forget to set your API keys for full functionality!${NC}"
fi

# Installation completion summary
END_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "Installation completed successfully at $END_TIME" >> "$LOG_FILE"
echo "Total installation time: $(date -d "$END_TIME" +%s) - $(date -d "$START_TIME" +%s) seconds" >> "$LOG_FILE" 2>/dev/null || true
echo "" >> "$LOG_FILE"
echo "Files created:" >> "$LOG_FILE"
echo "- $WORKSPACE_ROOT/config.json" >> "$LOG_FILE"
echo "- $WORKSPACE_ROOT/bchat (symlink)" >> "$LOG_FILE"
echo "- $INSTALL_DIR/rchat" >> "$LOG_FILE"
echo "- $INSTALL_DIR/runchat" >> "$LOG_FILE"
echo "- $INSTALL_DIR/start" >> "$LOG_FILE"
if [ -f "$WORKSPACE_ROOT/.vscode/tasks.json" ]; then
    echo "- $WORKSPACE_ROOT/.vscode/tasks.json" >> "$LOG_FILE"
fi
echo "" >> "$LOG_FILE"
echo "Directories created:" >> "$LOG_FILE"
echo "- $WORKSPACE_ROOT/chats" >> "$LOG_FILE"
echo "- $WORKSPACE_ROOT/logs" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

print_status "success" "bchat is ready to use!"
print_status "info" "Installation details logged to: $LOG_FILE"