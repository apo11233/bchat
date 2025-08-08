# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Directives
**IMPORTANT**: All developers and AI assistants MUST follow the development directives in `dev_directives/general.md`. These directives override any default behavior and must be adhered to exactly as written.

## Repository Overview

This is the AI CLI Chat Logger (bchat) - a Python-based system for monitoring and logging AI conversation sessions from CLI tools like Claude Code and Gemini CLI. The system provides intelligent chat analysis, structured logging, and consolidated backup files.

## Common Commands

### Installation and Setup
```bash
# Install the system (must be run from bchat directory)
./install.sh

# Check system status
python3 src/chat_monitor.py --help
```

### Testing Dependencies
```bash
# Test Python dependencies
python3 -c "import watchdog, google.generativeai, dotenv; print('All dependencies OK')"

# Verify API configuration
python3 -c "import os; print('API Key:', os.getenv('GOOGLE_API_KEY')[:10] + '...' if os.getenv('GOOGLE_API_KEY') else 'NOT SET')"
```

### Running the System
```bash
# Start monitoring (from bchat directory)
./start
# OR
./rchat
# OR  
./runchat

# Manual consolidation
./rchat --consolidate

# Run with specific config
python3 src/chat_monitor.py --config /path/to/config.json
```

### Chat Commands
```bash
# Backup current conversation (no args)
bchat

# Use Gemini CLI with logging (with args)
bchat -p "Your prompt here"
bchat --help  # Shows Gemini CLI options
```

### Linting and Testing
```bash
# Check Python syntax
python3 -m py_compile src/chat_monitor.py src/main.py src/utils/path_manager.py

# Run the path manager test
cd src/utils && python3 path_manager.py
```

## Architecture Overview

### Core Components

1. **ChatMonitor** (`src/chat_monitor.py`) - Main monitoring system with:
   - Watchdog-based file monitoring
   - Circuit breaker pattern for API resilience
   - Debounced event processing
   - Structured logging and indexing

2. **PathManager** (`src/utils/path_manager.py`) - Centralized path resolution:
   - Dynamic project root detection
   - Configuration-based path management
   - Directory structure validation

3. **APIManager** (embedded in `chat_monitor.py`) - API interaction handler:
   - Google Gemini API integration
   - Rate limiting and retry logic
   - Exponential backoff for failures

4. **bchat Command** - Universal chat interface:
   - No args: triggers backup/consolidation 
   - With args: routes to Gemini CLI with logging

### File Structure Patterns
- **Main module**: `src/chat_monitor.py` (identical to `src/main.py`)
- **Utilities**: `src/utils/` directory
- **Configuration**: `config.json` (workspace root) and `config.template.json`
- **Scripts**: Shell scripts in repository root (`bchat`, `rchat`, `start`, etc.)
- **Logs**: `logs/` directory for system logs
- **Chats**: `chats/` directory for processed chat data

### Configuration System
Configuration follows a hierarchical approach:
1. Load from `config.json` in workspace root
2. Fall back to `config.template.json` defaults
3. Environment variables (`.env` file)
4. Hard-coded defaults in `PathManager._get_default_config()`

Key config sections:
- `paths`: File and directory locations
- `monitoring`: Watchdog and debounce settings
- `api`: Gemini API configuration
- `error_handling`: Circuit breaker and retry settings
- `keywords`: Trigger words and filtering

### Data Flow
1. AI CLI tools (Claude Code, Gemini) write to log files
2. Watchdog monitors file changes with debouncing
3. Trigger words ("bchat") cause immediate processing
4. API calls generate structured summaries
5. Results saved to:
   - Individual session JSON files
   - `chats/chat_index.json` (searchable index)
   - `chats/context_summary.json` (cross-session context)

### Key Design Patterns
- **Circuit Breaker**: `CircuitBreaker` class for API resilience
- **Observer Pattern**: Watchdog `FileSystemEventHandler`
- **Singleton Configuration**: `PathManager` centralizes config
- **Debouncing**: Timer-based event consolidation
- **Structured Logging**: ISO 8601 timestamps, session IDs

## Environment Variables
Essential environment variables (create `.env` file):
```bash
GOOGLE_API_KEY=your_gemini_api_key_here  # Required for AI processing
CHAT_LOG_RETENTION_DAYS=90               # Optional: log retention
CHAT_MONITOR_DEBUG=false                 # Optional: debug mode
```

## Important Implementation Notes

### Python Dependencies
System requires Python 3.8+ with:
- `watchdog>=4.0.0` - File system monitoring
- `google-generativeai>=0.8.0` - Gemini API client  
- `python-dotenv>=1.0.0` - Environment variable management

### Shell Script Dependencies  
- `bchat` - Main command (symlinked to workspace root)
- `rchat`/`runchat` - Chat monitor launchers
- `start` - Quick start script
- `claude_wrapper.sh` - Claude CLI logging wrapper
- `gemini_wrapper.sh` - Gemini CLI logging wrapper

### Project Root Detection
`PathManager` auto-detects project root by searching for:
- `config.json`
- `.git` directory
- `package.json` 
- `chat_monitor.py`

### Trigger System
System processes content immediately when "bchat" keyword detected in logs. Otherwise content is stored for batch consolidation.

### Error Resilience
- Circuit breaker prevents API cascade failures
- Exponential backoff for retries
- Graceful degradation when APIs unavailable
- Comprehensive logging for debugging

## Working with This Codebase

### Making Changes
- The main logic is in `src/chat_monitor.py`
- Path management is centralized in `src/utils/path_manager.py`
- Shell scripts handle CLI integration
- Configuration is JSON-based with environment variable overrides

### Testing Approach  
- Manual testing via `python3 src/chat_monitor.py --consolidate`
- Path manager has built-in test: `cd src/utils && python3 path_manager.py`
- Integration testing via `bchat` commands
- Check logs in `logs/bchat.log`

### Common Issues
- Missing GOOGLE_API_KEY environment variable
- Incorrect file permissions on shell scripts
- Path resolution issues (check `PathManager` logic)
- API rate limiting (configured in `config.json`)

The system is designed for resilience and operates in the background to capture AI conversation context for future reference and analysis.