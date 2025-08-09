# bchat User Guide

## Overview
The `bchat` command provides universal AI conversation backup and Gemini CLI integration. Use it from anywhere in your workspace to save conversations and interact with AI tools.

## Quick Start

### Basic Usage
```bash
# Backup current conversation (no arguments)
bchat

# Use Gemini CLI with logging (with arguments)
bchat -p "Your prompt here"
bchat --help  # Shows Gemini CLI options
```

## Universal Access

### Works From Anywhere
The `bchat` command works from any directory in your workspace:

```bash
# From project root
bchat

# From subdirectories
cd apps/frontend/src/components/
bchat                    # Still works

# From VSCode terminal
bchat                    # Always accessible
```

### Common Scenarios

#### After AI Development Session
```bash
# 1. Finish coding with Claude Code
# 2. Backup the conversation
bchat                    # "Save our progress"
```

#### Multi-AI Workflow
```bash
# Use Claude for architecture
# ... productive conversation ...
bchat                    # Save architectural decisions

# Switch to Gemini for implementation  
bchat -p "Implement the architecture we designed"
bchat                    # Save implementation notes
```

#### Team Context Sharing
```bash
# After significant progress
bchat                    # Creates structured backup

# Automatically creates:
# ✅ chats/chat_backup_YYYY-MM-DD.md     # Human-readable
# ✅ chats/chat_index.json              # Machine-readable
# ✅ chats/context_summary.json         # Cross-session context
```

## Command Integration

### Installation Requirements
```bash
# Gemini CLI installation
npm install -g @google/gemini-cli

# Verification
which gemini            # Should show: /opt/homebrew/bin/gemini
./bchat --help         # Should display Gemini CLI options
```

### Command Flow
```
User Input → bchat → gemini_wrapper.sh → gemini CLI → Output + Logging
```

### Features
- **Session Tracking**: Unique session IDs with ISO 8601 timestamps
- **Complete Logging**: All input/output captured to `chats/gemini_current_day_raw.log`
- **AI Processing**: Automatic summarization when "bchat" keyword detected
- **JSON Indexing**: Machine-readable metadata in `chats/chat_index.json`

## Usage Examples

### Interactive Mode
```bash
./bchat                 # Opens interactive Gemini session
```

### Prompt Mode
```bash
./bchat -p "Explain quantum computing"
./bchat -p "Help debug this error: [error details]"

# IMPORTANT: Use quotes for prompts with spaces or special characters.
# The shell uses spaces to separate arguments, so quotes group your prompt into a single argument.
./bchat -p "Analyze this project and suggest three improvements."
```

### Project Analysis
```bash
./bchat -a -p "Review this entire project"
./bchat -p "Analyze the codebase architecture"
```

## Troubleshooting

### Command Not Found
```bash
# If 'bchat' not found:
chmod +x bchat
./install.sh           # Re-run installer

# If 'gemini' command not found:
npm list -g @google/gemini-cli
npm install -g @google/gemini-cli
```

### Logging Issues
- Check `config.json` for correct paths
- Verify `chats/` directory exists and is writable
- Ensure `gemini_wrapper.sh` has execute permissions

### No AI Processing
- Ensure `GOOGLE_API_KEY` environment variable is set
- Check if bchat monitoring is running
- Verify "bchat" keyword appears in logs for trigger detection

## What Gets Saved

### Automatic Backup
- Complete conversation threads
- Code changes and solutions
- Decisions made and problems solved
- Timestamps and session metadata
- AI-generated summaries

### File Locations
- `chats/gemini_current_day_raw.log` - Raw daily logs
- `chats/chat_backup_YYYY-MM-DD.md` - Daily consolidated backups
- `chats/chat_index.json` - Searchable conversation index
- `chats/context_summary.json` - Cross-session context

## Tips

### Natural Usage
- Just type `bchat` whenever you want to preserve important conversations
- No need to navigate to specific directories
- Works seamlessly with any AI development workflow

### Best Practices
- Use `bchat` at key milestones in your work
- Let the system handle the technical details automatically
- Review `chats/chat_index.json` to see what's been saved
- Check daily backup files for consolidated summaries

The `bchat` command provides effortless AI conversation management - just use it naturally and let the system handle the rest!