#!/bin/bash

# ST_00 Rollback Procedure
# Safe rollback to known working state

echo "🔄 ST_00 Rollback Procedure"
echo "==========================="
echo "Date: $(date)"
echo ""

# Configuration
BACKUP_DIR="dev/dev_stages/ST_00/backup"
PROJECT_ROOT="$(pwd)"

# Check if we're in the right directory
if [ ! -f "config/config.json" ]; then
    echo "❌ Error: Not in bchat project root directory"
    echo "   Please run from bchat directory"
    exit 1
fi

# Check if backup exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Error: Backup directory not found at $BACKUP_DIR"
    echo "   Run backup creation first"
    exit 1
fi

echo "⚠️  WARNING: This will restore system to ST_00 baseline state"
echo "   Current changes since backup will be lost"
echo ""
read -p "Continue with rollback? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Rollback cancelled"
    exit 0
fi

echo ""
echo "🔄 Starting rollback process..."

# Function to restore file if backup exists
restore_file() {
    local file_path="$1"
    local backup_path="$BACKUP_DIR/$file_path"
    
    if [ -f "$backup_path" ]; then
        echo "  Restoring $file_path"
        cp "$backup_path" "$file_path"
        return 0
    else
        echo "  ⚠️  Backup not found for $file_path"
        return 1
    fi
}

# Function to restore directory if backup exists
restore_directory() {
    local dir_path="$1"
    local backup_path="$BACKUP_DIR/$dir_path"
    
    if [ -d "$backup_path" ]; then
        echo "  Restoring directory $dir_path"
        rm -rf "$dir_path"
        cp -r "$backup_path" "$dir_path"
        return 0
    else
        echo "  ⚠️  Backup not found for directory $dir_path"
        return 1
    fi
}

echo ""
echo "📂 Restoring Core Files"
echo "----------------------"

# Restore core system files
restore_file "config/config.json"
restore_file "core/src/bchat.py"
restore_file "core/src/auto_detect.py"
restore_file ".env"
restore_file "bchat"
restore_file "install.sh"

echo ""
echo "📁 Restoring Data Directories"
echo "-----------------------------"

# Restore data directories
restore_directory "data/chats"
restore_directory "data/logs"

echo ""
echo "🔧 Restoring Virtual Environment"
echo "--------------------------------"

if [ -d "$BACKUP_DIR/dev/venv" ]; then
    echo "  Restoring Python virtual environment"
    rm -rf "dev/venv"
    cp -r "$BACKUP_DIR/dev/venv" "dev/venv"
else
    echo "  ⚠️  Virtual environment backup not found"
    echo "  You may need to run ./install.sh after rollback"
fi

echo ""
echo "✅ Rollback completed!"
echo ""
echo "🔍 Post-rollback validation:"

# Run validation to confirm rollback success
if [ -f "dev/dev_stages/ST_00/validation.sh" ]; then
    echo "Running validation suite..."
    ./dev/dev_stages/ST_00/validation.sh
    validation_result=$?
    
    if [ $validation_result -eq 0 ]; then
        echo ""
        echo "🎉 System successfully rolled back to ST_00 baseline!"
    else
        echo ""
        echo "⚠️  Validation failed after rollback"
        echo "   Manual intervention may be required"
    fi
else
    echo "⚠️  Validation script not found, manual testing recommended"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Test basic functionality: ./bchat --status"
echo "2. If issues persist, check backup integrity"
echo "3. Consider git reset if needed: git reset --hard HEAD"