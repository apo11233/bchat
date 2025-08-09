#!/bin/bash
# Enhanced Gemini CLI wrapper with ISO 8601 timestamping and session management

# Get project root directory (two levels up from wrappers)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Load configuration
CONFIG_FILE="$PROJECT_ROOT/config/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found at $CONFIG_FILE" >&2
    exit 1
fi

# Extract log path from config (fallback to default)
GEMINI_LOG=$(python3 -c "
import json, sys
try:
    with open('$CONFIG_FILE', 'r') as f:
        config = json.load(f)
    print(config.get('paths', {}).get('gemini_log', 'chats/gemini_current_day_raw.log'))
except:
    print('chats/gemini_current_day_raw.log')
" 2>/dev/null)

# Convert to absolute path
if [[ "$GEMINI_LOG" != /* ]]; then
    GEMINI_LOG="$PROJECT_ROOT/$GEMINI_LOG"
fi

# Ensure log directory exists
LOG_DIR=$(dirname "$GEMINI_LOG")
mkdir -p "$LOG_DIR"

# Generate session ID
SESSION_ID="gemini_$(date +%Y%m%d_%H%M%S)_$$"

# Function to log with timestamp
log_with_timestamp() {
    local message_type="$1"
    local content="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
    
    echo "[$timestamp] [$SESSION_ID] [$message_type] $content" >> "$GEMINI_LOG"
}

# Function to handle script cleanup
cleanup() {
    log_with_timestamp "SESSION" "Session ended"
    echo "" >> "$GEMINI_LOG"  # Add blank line between sessions
}

# Set up cleanup trap
trap cleanup EXIT

# Log session start
log_with_timestamp "SESSION" "Session started - Gemini CLI wrapper"
log_with_timestamp "INFO" "Session ID: $SESSION_ID"
log_with_timestamp "INFO" "Log file: $GEMINI_LOG"
log_with_timestamp "INFO" "Command: gemini-cli $*"

# If arguments are provided, run non-interactively
if [ $# -gt 0 ]; then
    log_with_timestamp "NON_INTERACTIVE_INPUT" "$*"
    # Execute gemini and log its output line by line
    if command -v gemini &> /dev/null; then
        gemini "$@" | while IFS= read -r line; do
            log_with_timestamp "GEMINI_OUTPUT" "$line"
            echo "$line"
        done
        GEMINI_EXIT_CODE=${PIPESTATUS[0]}
    else
        log_with_timestamp "WARNING" "gemini command not found, using placeholder"
        echo "Gemini CLI placeholder - install @google/gemini-cli for actual functionality"
        GEMINI_EXIT_CODE=0
    fi
else
    # Interactive mode with named pipes
    PIPE_DIR="/tmp/gemini_wrapper_$"
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
            log_with_timestamp "GEMINI_OUTPUT" "$line"
            echo "$line"
        done
    }

    # Background process to handle input logging
    tee >(log_input) < /dev/stdin > "$INPUT_PIPE" &
    INPUT_PID=$!

    # Background process to handle output logging
    log_output < "$OUTPUT_PIPE" &
    OUTPUT_PID=$!

    # Check if gemini exists, fallback to a simple echo for testing
    if command -v gemini &> /dev/null; then
        gemini "$@" < "$INPUT_PIPE" | tee "$OUTPUT_PIPE"
        GEMINI_EXIT_CODE=$?
    else
        log_with_timestamp "WARNING" "gemini command not found, using placeholder"
        echo "Gemini CLI placeholder - install @google/gemini-cli for actual functionality" | tee "$OUTPUT_PIPE"
        GEMINI_EXIT_CODE=0
    fi

    # Cleanup for interactive mode
    kill $INPUT_PID $OUTPUT_PID 2>/dev/null
    rm -rf "$PIPE_DIR"
fi

# Log session completion
log_with_timestamp "INFO" "Gemini CLI exited with code: $GEMINI_EXIT_CODE"

exit $GEMINI_EXIT_CODE