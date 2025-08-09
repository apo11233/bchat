# 🤖 AI CLI Chat Logger (bchat)

**AI Conversation Intelligence with Technical Context Preservation**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Nyrk0/bchat/releases)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey.svg)](#installation)
[![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)](#system-requirements)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Contributors](https://img.shields.io/github/contributors/Nyrk0/bchat.svg)](https://github.com/Nyrk0/bchat/graphs/contributors)

**AI Conversation Intelligence with Technical Context Preservation**

A lightweight, fully local Python utility that captures AI-powered CLI chat logs with intelligent semantic processing **and preserves the crucial technical "how" and "why"** that future development sessions need. Features dual AI provider support (Claude/Gemini), automatic chat analysis with implementation details, and structured JSON backups that maintain technical continuity. Simple 3-step setup with professional-grade organization and no external platform dependencies.

## 📋 Development Guidelines
**For Developers and AI Contributors**: All development work must follow the mandatory directives in [`dev_directives/general.md`](dev_directives/general.md). These guidelines ensure code quality, security, and consistency across the project.

---

## 🎯 **Why bchat?**

- **🧠 Technical Context Preservation**: Captures the crucial "how" and "why" that future development sessions need
- **🔒 Fully Local**: No data leaves your machine
- **⚡ Simple Setup**: Ready in 3 steps - clone, add API key, install
- **🌍 Universal Access**: `bchat` command works from anywhere in your workspace
- **🤖 AI-Smart**: Intelligent chat analysis with implementation detail extraction
- **📦 Lightweight**: Minimal dependencies, maximum functionality

---

## ✨ Features

- 🧠 **Technical Context Intelligence**: Preserves implementation details, code changes, and architectural decisions that enable seamless development continuity
- 🔍 **Real-time Monitoring**: Automatically watches and processes AI chat logs
- 🧠 **Dual AI Providers**: Choose between Claude or Gemini APIs for intelligent analysis
- 📊 **Structured Data**: Creates machine-readable JSON indexes with technical metadata and implementation tracking
- 🔄 **Daily Consolidation**: Merges multiple chat files into organized single files with context preservation
- 🚀 **Universal Access**: `bchat` command works from any directory in your workspace
- 💬 **Multi-AI Support**: Compatible with Claude Code, Gemini CLI, and extensible to other AI tools
- 🛡️ **Resilient Architecture**: Circuit breaker patterns, retry logic, and graceful error handling
- ⚡ **Professional Organization**: Clean workspace structure with essential files at root level

---

## 🚀 Quick Start

### System Requirements
- **Python 3.8+** (required)
- **AI API Key** (required for intelligent processing): Anthropic API key for Claude OR Google API key for Gemini
- **Node.js 16+** (optional, for Gemini CLI integration)
- **Git** (for installation)

### Installation (macOS/Linux)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nyrk0/bchat.git
   cd bchat
   ```

2. **Configure your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key:
   # For Claude (recommended): ANTHROPIC_API_KEY=your_anthropic_api_key_here
   # For Gemini: GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Run the installer:**
   ```bash
   ./install.sh
   ```

4. **Start using bchat:**
   ```bash
   # Check system status (works without API key)
   ./bchat --status
   
   # Backup and process chat conversation (requires API key)
   ./bchat
   
   # Use Gemini CLI with logging (requires API key)
   ./bchat -p "Explain quantum computing"
   ```

> **💡 Note**: Basic commands like `--status` work immediately. Intelligent processing features require an API key configured in step 2.

### Windows Support
Windows installation is not yet supported. **[Contributions for Windows installer scripts are highly welcomed!](CONTRIBUTING.md#windows-support-most-wanted)** The core Python functionality should work on Windows with manual setup.

---

## 🎯 How to Use

### The Universal `bchat` Command

The `bchat` command works from **anywhere** in your workspace:

#### **Backup Mode (no arguments)**
```bash
# From any directory - triggers chat backup/consolidation
bchat
```
- **From AI CLI windows**: Saves current AI conversation to structured logs
- **From VSCode terminal**: Consolidates recent chat activity 
- **From any location**: Works globally across the workspace

#### **Gemini CLI Mode (with arguments)**
```bash
bchat -p "Explain quantum computing"
bchat -a -p "Analyze this project structure"  # Include all files
bchat --help                                  # See all Gemini options
```

### Monitoring Commands
```bash
# Start monitoring system
./start

# Control monitoring (from ai-cli-chat-logger directory)
./rchat --help          # View all options
./runchat              # Alternative command (same as rchat)

# Manual consolidation
./rchat --consolidate
```

---

## 📁 What Gets Created

When you clone from GitHub:
```bash
cd /their/workspace/
git clone https://github.com/Nyrk0/bchat.git
```

You will get:
```
their-workspace/
├── their-existing-file.txt     # User's files (no conflict)
├── their-config.json           # User's files (no conflict) 
├── their-install.sh            # User's files (no conflict)
└── bchat/                      # All bchat files contained here
    ├── README.md               # Documentation
    ├── LICENSE                 # MIT License
    ├── CLAUDE.md               # Claude Code instructions
    ├── bchat                   # Main executable
    ├── install.sh              # Installation script
    ├── requirements.txt        # Python dependencies
    ├── .env.example           # Environment template
    ├── bin/                    # All executable scripts
    │   ├── bchat-status        # System status checker
    │   ├── rchat               # Chat monitor launcher
    │   ├── runchat             # Alternative launcher
    │   └── start               # Quick start script
    ├── config/                 # Configuration files
    │   ├── config.json         # Main config (Claude Sonnet 4 default)
    │   └── wrappers/
    │       ├── claude_wrapper.sh   # Claude CLI logging wrapper
    │       └── gemini_wrapper.sh   # Gemini CLI logging wrapper
    ├── core/                   # Python source code
    │   └── src/
    │       ├── chat_monitor.py # Core monitoring system
    │       └── utils/
    │           └── path_manager.py # Path resolution utilities
    ├── data/                   # Runtime data (created during use)
    │   ├── chats/              # Chat logs and processed JSON
    │   │   ├── chat_index.json      # Searchable session index
    │   │   ├── context_summary.json # Cross-session analysis
    │   │   ├── chat_log_*.json      # Individual session logs
    │   │   ├── claude_current_day_raw.log   # Raw Claude logs
    │   │   └── gemini_current_day_raw.log   # Raw Gemini logs
    │   └── logs/
    │       └── bchat.log       # System operation logs
    ├── dev/                    # Development tools
    │   ├── venv/               # Virtual environment (created by install)
    │   └── dev_directives/
    │       └── general.md      # Development guidelines
    └── docs/                   # Complete documentation
        ├── user-guide.md       # User documentation
        ├── ai-integration.md   # AI integration guide
        ├── CHANGELOG.md        # Project history
        └── structure.md        # Workspace organization guide
```

**Perfect Namespace Isolation**: All bchat files are contained within the `bchat/` directory, preventing any conflicts with your existing files. You can have your own `install.sh`, `config.json`, etc. without any naming conflicts.

---

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# API Keys (choose your preferred provider)
GOOGLE_API_KEY=your_google_api_key_here        # For Gemini provider
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # For Claude provider

# Optional: Chat log retention (default: 90 days)
CHAT_LOG_RETENTION_DAYS=90

# Optional: Debug mode (default: false)
CHAT_MONITOR_DEBUG=false
```

### Advanced Configuration (config.json)
```json
{
  "system": {
    "project_name": "your_project",
    "log_level": "INFO"
  },
  "api": {
    "provider": "gemini",
    "model": "gemini-2.5-flash",
    "claude": {
      "model": "claude-3-5-sonnet-20241022"
    }
  },
  "monitoring": {
    "enabled": true,
    "debounce_delay": 2.0,
    "triggers": ["bchat", "backup chat"]
  }
}
```

---

## 🧠 **Technical Context Intelligence**

**The Core Purpose**: bchat solves the critical problem of **technical context continuity** in AI-assisted development sessions.

### **The Problem**
Traditional chat logging captures *what* was decided but loses the crucial *how* and *why*:
- ❌ Specific code changes and their locations
- ❌ Root cause analysis of issues
- ❌ System architecture understanding
- ❌ Implementation strategies and technical decisions
- ❌ Development stage progress and status

### **bchat's Solution**
bchat preserves **technical implementation context** that future development sessions need:
- ✅ **Code Change Tracking**: Documents specific files modified and why
- ✅ **Architecture Mapping**: Captures component relationships and system understanding  
- ✅ **Stage Progress**: Tracks development methodology progress (ST_00 → ST_01 → ST_02...)
- ✅ **Issue Resolution**: Preserves root cause analysis and solution implementation
- ✅ **Technical Decisions**: Documents the reasoning behind implementation choices

### **Foundation Audit Results**
Our comprehensive system analysis reveals that while basic JSON processing works excellently, enhanced technical context capture is essential for development continuity. See detailed findings in [`dev/dev_stages/ST_00/01-250808-audit_report.md`](dev/dev_stages/ST_00/01-250808-audit_report.md).

**Key Discovery**: Context continuity gaps were identified as a HIGH priority issue affecting development efficiency and technical knowledge preservation.

---

## 📊 Usage Examples

### AI Development Sessions
```bash
# Start a Claude Code session
claude

# After productive conversation, backup progress
bchat

# Continue in VSCode terminal and save work
bchat
```

### Team Collaboration
```bash
# After significant progress
bchat

# System creates:
# ✅ chats/chat_backup_YYYY-MM-DD.md     # Human-readable
# ✅ chats/chat_index.json              # Machine-readable
# ✅ chats/context_summary.json         # Cross-session context
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/your-feature`
3. **Make your changes and test**
4. **Commit with clear messages:** `git commit -m "Add Windows installer support"`
5. **Push and create a pull request**

### 🔥 High Priority Contributions Needed

- **Windows installer script** - Adapt `install.sh` for Windows/PowerShell
- **Linux distribution testing** - Test on Ubuntu, Debian, Fedora, etc.
- **Performance optimizations** - Async processing, caching
- **Web dashboard** - Browser interface for chat analytics
- **Unit tests** - Test coverage for all components

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 🔍 Troubleshooting

### Common Issues

<details>
<summary><strong>Installation fails</strong></summary>

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Install dependencies manually
pip3 install watchdog google-generativeai python-dotenv
```
</details>

<details>
<summary><strong>API errors</strong></summary>

```bash
# Verify API key
echo $GOOGLE_API_KEY | head -c 10

# Test API connection
python3 -c "import google.generativeai as genai; genai.configure(api_key='$GOOGLE_API_KEY'); print('API works')"
```
</details>

<details>
<summary><strong>bchat not found</strong></summary>

```bash
# Re-run installer
./install.sh

# Check symlink
ls -la ../bchat
```
</details>

### Getting Help

- 📖 **Documentation**: Check our [docs/](docs/) directory
- 🐛 **Bug Reports**: [Create an issue](https://github.com/Nyrk0/bchat/issues/new)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Nyrk0/bchat/discussions)
- 📧 **Contact**: Open an issue for questions

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Alex Walter Rettig Eglinton

---

## 🔗 Related Projects

- [Claude Code](https://claude.ai/code) - Official Claude CLI
- [Gemini CLI](https://github.com/google/generative-ai-python) - Google's Gemini CLI
- [Watchdog](https://github.com/gorakhargosh/watchdog) - Python file monitoring

---

## ⭐ Support This Project

If this project helps you, please consider:
- ⭐ **Starring the repository**
- 🐛 **Reporting bugs** via Issues
- 💡 **Suggesting features** via Issues  
- 🔧 **Contributing code** via Pull Requests
- 📢 **Sharing with others** who might find it useful

---

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Nyrk0/bchat.svg)
![GitHub forks](https://img.shields.io/github/forks/Nyrk0/bchat.svg)
![GitHub issues](https://img.shields.io/github/issues/Nyrk0/bchat.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/Nyrk0/bchat.svg)

---

**🚀 Ready to get started? Run `./install.sh` and you'll be monitoring AI conversations in under a minute!**