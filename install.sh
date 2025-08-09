#!/bin/bash
# bchat Installation Script with Security Enhancements and Auto-Detection
# Version: 1.0.0
# This script provides comprehensive installation with security features

set -e  # Exit on any error

# Global variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BCHAT_VERSION="1.0.0"
INSTALL_LOG="$SCRIPT_DIR/dev/installation.log"
VENV_PATH="$SCRIPT_DIR/dev/venv"

# Ensure log directory exists
mkdir -p "$(dirname "$INSTALL_LOG")"

# Security and utility functions
validate_path() {
    local path="$1"
    
    # Check for directory traversal attempts
    if [[ "$path" == *".."* ]] || [[ "$path" == *"~"* ]]; then
        log_command "ERROR: Path validation failed for: $path"
        return 1
    fi
    
    # Validate path format
    if [[ ! "$path" =~ ^[a-zA-Z0-9/_.-]+$ ]]; then
        log_command "ERROR: Invalid characters in path: $path"
        return 1
    fi
    
    return 0
}

create_backup() {
    local file="$1"
    
    if [ -f "$file" ]; then
        local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$file" "$backup"
        log_command "Created backup: $backup"
        echo "$backup"
    fi
}

print_status() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "📦 bchat: $message"
    echo "[$timestamp] $message" >> "$INSTALL_LOG"
}

log_command() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] $message" >> "$INSTALL_LOG"
}

rollback() {
    print_status "Installation failed - performing rollback..."
    
    # Remove created virtual environment
    if [ -d "$VENV_PATH" ]; then
        rm -rf "$VENV_PATH"
        log_command "Removed virtual environment: $VENV_PATH"
    fi
    
    # Restore any backups created during this session
    # (Implementation would track backups created)
    
    print_status "Rollback completed"
    exit 1
}

# Set trap for cleanup on failure
trap rollback ERR

# Main installation functions
check_dependencies() {
    print_status "Checking system dependencies..."
    
    # Check Python 3.8+
    if ! command -v python3 &> /dev/null; then
        print_status "ERROR: Python 3 is required but not installed"
        exit 1
    fi
    
    local python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
    log_command "Found Python version: $python_version"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        print_status "WARNING: Git not found - some features may be limited"
    fi
    
    print_status "Dependencies check completed"
}

setup_directories() {
    print_status "Setting up directory structure..."
    
    local dirs=("data/chats" "data/logs" "dev")
    
    for dir in "${dirs[@]}"; do
        local full_path="$SCRIPT_DIR/$dir"
        if validate_path "$full_path"; then
            mkdir -p "$full_path"
            log_command "Created directory: $full_path"
        else
            print_status "ERROR: Failed to validate directory path: $dir"
            exit 1
        fi
    done
    
    print_status "Directory structure setup completed"
}

setup_virtual_environment() {
    print_status "Setting up Python virtual environment..."
    
    if [ -d "$VENV_PATH" ]; then
        print_status "Virtual environment already exists - skipping creation"
        return 0
    fi
    
    # Create virtual environment
    python3 -m venv "$VENV_PATH"
    log_command "Created virtual environment at: $VENV_PATH"
    
    # Activate and install dependencies
    source "$VENV_PATH/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip
    log_command "Upgraded pip in virtual environment"
    
    # Install requirements
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        pip install -r "$SCRIPT_DIR/requirements.txt"
        log_command "Installed packages from requirements.txt"
    else
        print_status "WARNING: requirements.txt not found"
    fi
    
    print_status "Virtual environment setup completed"
}

setup_permissions() {
    print_status "Setting up file permissions..."
    
    local executables=("bin/bchat" "bin/rchat" "bin/runchat" "bin/start" "bin/bchat-status")
    local wrappers=("config/wrappers/claude_wrapper.sh" "config/wrappers/gemini_wrapper.sh")
    
    for exec_file in "${executables[@]}" "${wrappers[@]}"; do
        local full_path="$SCRIPT_DIR/$exec_file"
        if [ -f "$full_path" ]; then
            chmod +x "$full_path"
            log_command "Made executable: $full_path"
        fi
    done
    
    print_status "File permissions setup completed"
}

create_symlink() {
    print_status "Creating symbolic link for bchat command..."
    
    local target_dir="/usr/local/bin"
    local source_file="$SCRIPT_DIR/bin/bchat"
    local link_name="$target_dir/bchat"
    
    if [ ! -d "$target_dir" ]; then
        print_status "WARNING: Target directory $target_dir does not exist. Skipping symlink."
        return
    fi
    
    if [ -L "$link_name" ] && [ -e "$link_name" ]; then
        print_status "Symbolic link already exists. Skipping."
        return
    fi
    
    print_status "This script needs sudo access to create a symbolic link in $target_dir."
    if sudo ln -s "$source_file" "$link_name"; then
        print_status "Symbolic link created successfully: $link_name -> $source_file"
    else
        print_status "ERROR: Failed to create symbolic link. You can try running 'sudo ln -s $source_file $link_name' manually."
    fi
}

run_auto_detection() {
    print_status "🔍 Running auto-detection and configuration..."
    
    # Activate virtual environment for auto-detection
    source "$VENV_PATH/bin/activate" 2>/dev/null || {
        print_status "WARNING: Could not activate virtual environment for auto-detection"
        return 1
    }
    
    if [ -f "$SCRIPT_DIR/core/src/auto_detect.py" ]; then
        python3 "$SCRIPT_DIR/core/src/auto_detect.py"
        log_command "Ran auto-detection system"
    else
        print_status "WARNING: Auto-detection module not found"
    fi
}

verify_installation() {
    print_status "Verifying installation..."
    
    # Check if main executable exists
    if [ -x "$SCRIPT_DIR/bchat" ]; then
        log_command "Main executable verified: bchat"
    else
        print_status "ERROR: Main executable not found or not executable"
        exit 1
    fi
    
    # Test basic functionality
    if [ -f "$SCRIPT_DIR/bin/bchat-status" ]; then
        log_command "Status checker available"
    else
        print_status "WARNING: Status checker not found"
    fi
    
    print_status "Installation verification completed"
}

# Main installation flow
main() {
    print_status "Starting bchat installation (v$BCHAT_VERSION)..."
    log_command "Installation started by user: $(whoami)"
    log_command "Installation directory: $SCRIPT_DIR"
    
    check_dependencies
    setup_directories
    setup_virtual_environment
    setup_permissions
    create_symlink
    run_auto_detection
    verify_installation
    
    print_status "Installation completed successfully!"
    
    # Installation summary
    print_status ""
    print_status "🚀 Installation Summary:"
    print_status "  📁 Project directory: $SCRIPT_DIR"
    print_status "  🐍 Virtual environment: $VENV_PATH"
    print_status "  📊 Installation log: $INSTALL_LOG"
    print_status ""
    print_status "🎯 Next steps:"
    print_status "1. Configure your API key: cp .env.example .env (then edit .env)"
    print_status "2. Check system status: ./bchat --status"
    print_status "3. Start using bchat: ./bchat"
    print_status ""
    print_status "📖 For detailed usage, see: README.md"
    
    log_command "Installation completed successfully"
}

# Run main installation
main "$@"