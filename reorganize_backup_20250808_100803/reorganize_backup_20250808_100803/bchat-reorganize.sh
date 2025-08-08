#!/bin/bash
# bchat-reorganize.sh - Safe bchat directory reorganization
# This script reorganizes the bchat directory into a clean, professional structure

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$SCRIPT_DIR/reorganize_backup_$TIMESTAMP"

# Function to print status
print_status() {
    local status=$1
    local message=$2
    case $status in
        "info") echo -e "${BLUE}ℹ️  $message${NC}" ;;
        "success") echo -e "${GREEN}✅ $message${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "error") echo -e "${RED}❌ $message${NC}" ;;
    esac
}

echo -e "${BLUE}🚀 bchat Directory Reorganization${NC}"
echo -e "${BLUE}=================================${NC}"
echo ""

# Create complete backup first
print_status "info" "Creating complete backup before reorganization..."
mkdir -p "$BACKUP_DIR"
cp -r "$SCRIPT_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
print_status "success" "Backup created at: $BACKUP_DIR"

# Create new directory structure
print_status "info" "Creating new directory structure..."

mkdir -p "$SCRIPT_DIR/core/src"
mkdir -p "$SCRIPT_DIR/bin"
mkdir -p "$SCRIPT_DIR/config/wrappers"
mkdir -p "$SCRIPT_DIR/data/chats"
mkdir -p "$SCRIPT_DIR/data/logs" 
mkdir -p "$SCRIPT_DIR/data/backups"
mkdir -p "$SCRIPT_DIR/docs/archive"
mkdir -p "$SCRIPT_DIR/dev/dev_directives"

print_status "success" "Directory structure created"

# Move core system files
print_status "info" "Moving core system files..."
[ -f "$SCRIPT_DIR/install.sh" ] && mv "$SCRIPT_DIR/install.sh" "$SCRIPT_DIR/core/"
[ -f "$SCRIPT_DIR/requirements.txt" ] && mv "$SCRIPT_DIR/requirements.txt" "$SCRIPT_DIR/core/"
[ -f "$SCRIPT_DIR/config.template.json" ] && mv "$SCRIPT_DIR/config.template.json" "$SCRIPT_DIR/core/"

# Move source code
if [ -d "$SCRIPT_DIR/src" ] && [ "$SCRIPT_DIR/src" != "$SCRIPT_DIR/core/src" ]; then
    mv "$SCRIPT_DIR/src"/* "$SCRIPT_DIR/core/src/" 2>/dev/null || true
    rmdir "$SCRIPT_DIR/src" 2>/dev/null || true
fi

# Move virtual environment
[ -d "$SCRIPT_DIR/venv" ] && mv "$SCRIPT_DIR/venv" "$SCRIPT_DIR/dev/"

print_status "success" "Core files moved"

# Move executable files to bin/
print_status "info" "Moving executable files..."
for exe in bchat rchat runchat bchat-status start; do
    if [ -f "$SCRIPT_DIR/$exe" ] && [ -x "$SCRIPT_DIR/$exe" ]; then
        mv "$SCRIPT_DIR/$exe" "$SCRIPT_DIR/bin/"
    fi
done

print_status "success" "Executables moved to bin/"

# Move configuration files
print_status "info" "Moving configuration files..."
[ -f "$SCRIPT_DIR/config.json" ] && mv "$SCRIPT_DIR/config.json" "$SCRIPT_DIR/config/"
[ -f "$SCRIPT_DIR/claude_wrapper.sh" ] && mv "$SCRIPT_DIR/claude_wrapper.sh" "$SCRIPT_DIR/config/wrappers/"
[ -f "$SCRIPT_DIR/gemini_wrapper.sh" ] && mv "$SCRIPT_DIR/gemini_wrapper.sh" "$SCRIPT_DIR/config/wrappers/"

print_status "success" "Configuration files moved"

# Move data files
print_status "info" "Moving data files..."
if [ -d "$SCRIPT_DIR/chats" ]; then
    mv "$SCRIPT_DIR/chats"/* "$SCRIPT_DIR/data/chats/" 2>/dev/null || true
    rmdir "$SCRIPT_DIR/chats" 2>/dev/null || true
fi

if [ -d "$SCRIPT_DIR/logs" ]; then
    mv "$SCRIPT_DIR/logs"/* "$SCRIPT_DIR/data/logs/" 2>/dev/null || true
    rmdir "$SCRIPT_DIR/logs" 2>/dev/null || true
fi

# Move backup files
print_status "info" "Moving backup files..."
mv "$SCRIPT_DIR"/*.backup.* "$SCRIPT_DIR/data/backups/" 2>/dev/null || true

print_status "success" "Data files moved"

# Move documentation
print_status "info" "Moving documentation..."
if [ -d "$SCRIPT_DIR/docs" ] && [ "$SCRIPT_DIR/docs" != "$SCRIPT_DIR/docs" ]; then
    # Move contents if docs directory exists elsewhere
    for doc in "$SCRIPT_DIR/docs"/*; do
        if [ -e "$doc" ]; then
            if [ -d "$doc" ] && [ "$(basename "$doc")" = "archive" ]; then
                mv "$doc"/* "$SCRIPT_DIR/docs/archive/" 2>/dev/null || true
                rmdir "$doc" 2>/dev/null || true
            else
                mv "$doc" "$SCRIPT_DIR/docs/"
            fi
        fi
    done
fi

print_status "success" "Documentation moved"

# Move development files
print_status "info" "Moving development files..."
[ -f "$SCRIPT_DIR/installation.log" ] && mv "$SCRIPT_DIR/installation.log" "$SCRIPT_DIR/dev/"
[ -f "$SCRIPT_DIR/installation_issues.md" ] && mv "$SCRIPT_DIR/installation_issues.md" "$SCRIPT_DIR/dev/"
[ -f "$SCRIPT_DIR/bchat.change.log" ] && mv "$SCRIPT_DIR/bchat.change.log" "$SCRIPT_DIR/dev/"

if [ -d "$SCRIPT_DIR/dev_directives" ]; then
    mv "$SCRIPT_DIR/dev_directives"/* "$SCRIPT_DIR/dev/dev_directives/" 2>/dev/null || true
    rmdir "$SCRIPT_DIR/dev_directives" 2>/dev/null || true
fi

print_status "success" "Development files moved"

# Update configuration paths
print_status "info" "Updating configuration paths..."

# Update config.json paths
if [ -f "$SCRIPT_DIR/config/config.json" ]; then
    sed -i.bak 's|"chats_dir": "chats"|"chats_dir": "data/chats"|g' "$SCRIPT_DIR/config/config.json"
    sed -i.bak 's|"logs_dir": "logs"|"logs_dir": "data/logs"|g' "$SCRIPT_DIR/config/config.json"
    sed -i.bak 's|"claude_log": "chats/|"claude_log": "data/chats/|g' "$SCRIPT_DIR/config/config.json"
    sed -i.bak 's|"gemini_log": "chats/|"gemini_log": "data/chats/|g' "$SCRIPT_DIR/config/config.json"
    sed -i.bak 's|"chat_index": "chats/|"chat_index": "data/chats/|g' "$SCRIPT_DIR/config/config.json"
    sed -i.bak 's|"context_summary": "chats/|"context_summary": "data/chats/|g' "$SCRIPT_DIR/config/config.json"
    rm "$SCRIPT_DIR/config/config.json.bak" 2>/dev/null || true
fi

# Update executable paths
for exe in "$SCRIPT_DIR/bin"/*; do
    if [ -f "$exe" ] && [ -x "$exe" ]; then
        # Update paths in executable files
        if grep -q "SCRIPT_DIR.*rchat" "$exe" 2>/dev/null; then
            sed -i.bak 's|"$SCRIPT_DIR/rchat"|"$SCRIPT_DIR/bin/rchat"|g' "$exe"
            rm "$exe.bak" 2>/dev/null || true
        fi
        if grep -q "SCRIPT_DIR.*gemini_wrapper.sh" "$exe" 2>/dev/null; then
            sed -i.bak 's|"$SCRIPT_DIR/gemini_wrapper.sh"|"$SCRIPT_DIR/config/wrappers/gemini_wrapper.sh"|g' "$exe"
            rm "$exe.bak" 2>/dev/null || true
        fi
    fi
done

print_status "success" "Configuration paths updated"

# Create symbolic links for easy access
print_status "info" "Creating convenience symlinks..."
ln -sf "$SCRIPT_DIR/bin/bchat" "$SCRIPT_DIR/bchat" 2>/dev/null || true
ln -sf "$SCRIPT_DIR/bin/bchat-status" "$SCRIPT_DIR/bchat-status" 2>/dev/null || true
ln -sf "$SCRIPT_DIR/core/install.sh" "$SCRIPT_DIR/install.sh" 2>/dev/null || true

print_status "success" "Convenience symlinks created"

# Clean up reorganization script
rm "$SCRIPT_DIR/bchat-reorganize.sh" 2>/dev/null || true

# Final summary
echo ""
print_status "success" "🎉 bchat reorganization completed successfully!"
echo ""
echo -e "${GREEN}📁 New Structure:${NC}"
echo "├── 📁 core/          # Core system files & source code"
echo "├── 📁 bin/           # Executable commands"  
echo "├── 📁 config/        # Configuration files"
echo "├── 📁 data/          # User data, chats, logs, backups"
echo "├── 📁 docs/          # Documentation"
echo "├── 📁 dev/           # Development files"
echo "└── 📄 README.md      # Main documentation"
echo ""
echo -e "${YELLOW}💡 Quick Commands:${NC}"
echo "  ./bchat-status      # Check system status"
echo "  ./bchat             # Main bchat command"
echo "  ./install.sh        # Reinstall if needed"
echo ""
echo -e "${BLUE}🔒 Backup Location: $BACKUP_DIR${NC}"