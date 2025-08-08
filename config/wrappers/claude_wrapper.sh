#!/bin/bash
# Enhanced Claude CLI wrapper with ISO 8601 timestamping and session management

# Get project root directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

# Load configuration
CONFIG_FILE="$PROJECT_ROOT/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found at $CONFIG_FILE" >&2
    exit 1
fi

# Extract log path from config (fallback to default)
CLAUDE_LOG=$(python3 -c "
import json, sys
try:
    with open('$CONFIG_FILE', 'r') as f:
        config = json.load(f)
    print(config.get('paths', {}).get('claude_log', 'chats/claude_current_day_raw.log'))
except:
    print('chats/claude_current_day_raw.log')
" 2>/dev/null)

# Convert to absolute path
if [[ "$CLAUDE_LOG" != /* ]]; then
    CLAUDE_LOG="$PROJECT_ROOT/$CLAUDE_LOG"
fi

# Ensure log directory exists
LOG_DIR=$(dirname "$CLAUDE_LOG")
mkdir -p "$LOG_DIR"

# Generate session ID
SESSION_ID="claude_$(date +%Y%m%d_%H%M%S)_$$"

# Function to log with timestamp
log_with_timestamp() {
    local message_type="$1"
    local content="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
    
    echo "[$timestamp] [$SESSION_ID] [$message_type] $content" >> "$CLAUDE_LOG"
}

# Function to handle script cleanup
cleanup() {
    log_with_timestamp "SESSION" "Session ended"
    echo "" >> "$CLAUDE_LOG"  # Add blank line between sessions
}

# Set up cleanup trap
trap cleanup EXIT

# Log session start
log_with_timestamp "SESSION" "Session started - Claude CLI wrapper"
log_with_timestamp "INFO" "Session ID: $SESSION_ID"
log_with_timestamp "INFO" "Log file: $CLAUDE_LOG"
log_with_timestamp "INFO" "Command: claude $*"

# Create a named pipe for capturing both stdin and stdout
PIPE_DIR="/tmp/claude_wrapper_$$"
mkdir -p "$PIPE_DIR"
INPUT_PIPE="$PIPE_DIR/input"
OUTPUT_PIPE="$PIPE_DIR/output"

mkfifo "$INPUT_PIPE" "$OUTPUT_PIPE"

# Function to log input
log_input() {
    while IFS= read -r line; do
        log_with_timestamp "USER_INPUT" "$line"
        echo "$line"
    done
}

# Function to log output  
log_output() {
    while IFS= read -r line; do
        log_with_timestamp "CLAUDE_OUTPUT" "$line"
        echo "$line"
    done
}

# Background process to handle input logging
tee >(log_input) < /dev/stdin > "$INPUT_PIPE" &
INPUT_PID=$!

# Background process to handle output logging
log_output < "$OUTPUT_PIPE" &
OUTPUT_PID=$!

# Run Claude CLI with input/output redirection
claude "$@" < "$INPUT_PIPE" | tee "$OUTPUT_PIPE"
CLAUDE_EXIT_CODE=$?

# Cleanup
kill $INPUT_PID $OUTPUT_PID 2>/dev/null
rm -rf "$PIPE_DIR"

# Log session completion
log_with_timestamp "INFO" "Claude CLI exited with code: $CLAUDE_EXIT_CODE"

exit $CLAUDE_EXIT_CODE