# 🤖 AI CLI Chat Logger (bchat)

**Universal AI Conversation Intelligence System**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Nyrk0/bchat/releases)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey.svg)](#installation)
[![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)](#system-requirements)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Contributors](https://img.shields.io/github/contributors/Nyrk0/bchat.svg)](https://github.com/Nyrk0/bchat/graphs/contributors)

A lightweight, fully local Python utility for capturing AI-powered CLI chat logs from Visual Studio Code (and potentially Cursor-compatible). Designed for simplicity, it requires no external platforms or complex dependencies, making it easy to adapt to your environment.

## 📋 Development Guidelines
**For Developers and AI Contributors**: All development work must follow the mandatory directives in [`dev_directives/general.md`](dev_directives/general.md). These guidelines ensure code quality, security, and consistency across the project.

---

## 🎯 **Why bchat?**

- **🔒 Fully Local**: No data leaves your machine
- **🚀 Zero Config**: Works out of the box with one command
- **🌍 Universal Access**: `bchat` command works from anywhere in your workspace
- **🤖 AI-Smart**: Intelligent chat analysis and summarization
- **📦 Lightweight**: Minimal dependencies, maximum functionality

---

## ✨ Features

- 🔍 **Real-time Monitoring**: Automatically watches and processes AI chat logs
- 🧠 **AI-Powered Analysis**: Uses Gemini API for intelligent summarization and entity extraction
- 📊 **Structured Data**: Creates machine-readable JSON indexes with metadata
- 🔄 **Daily Consolidation**: Merges multiple chat files into organized single files
- 🚀 **Universal Access**: `bchat` command works from any directory in your workspace
- 💬 **Multi-AI Support**: Compatible with Claude Code, Gemini CLI, and extensible to other AI tools
- 🛡️ **Resilient Architecture**: Circuit breaker patterns, retry logic, and graceful error handling

---

## 🚀 Quick Start

### System Requirements
- **Python 3.8+** (required)
- **Node.js 16+** (optional, for Gemini CLI)
- **Git** (for installation)
- **Google API key** (optional, for AI analysis)

### Installation (macOS/Linux)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nyrk0/bchat.git
   cd bchat
   ```

2. **Run the installer:**
   ```bash
   ./install.sh
   ```

3. **Configure API keys (optional):**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key:
   # GOOGLE_API_KEY=your_actual_api_key_here
   ```

4. **Start using bchat:**
   ```bash
   # Backup current chat conversation
   bchat
   
   # Use Gemini CLI with logging
   bchat -p "Explain quantum computing"
   ```

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

After installation, your workspace will have:

```
your-workspace/
├── bchat/                  # Main application (this repo)
│   ├── src/chat_monitor.py # Core monitoring system
│   ├── install.sh          # Installation script
│   ├── bchat              # Universal chat command
│   ├── rchat              # Monitoring controls
│   └── docs/              # Documentation
│
├── config.json            # Workspace configuration
├── chats/                 # Chat logs and indexes
│   ├── chat_index.json    # Machine-readable index
│   ├── context_summary.json
│   └── chat_backup_*.md   # Daily consolidated files
│
└── logs/                  # System logs
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Required: Google API key for AI processing
GOOGLE_API_KEY=your_google_api_key_here

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
  "monitoring": {
    "enabled": true,
    "debounce_delay": 2.0,
    "triggers": ["bchat", "backup chat"]
  }
}
```

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

![GitHub stars](https://img.shields.io/github/stars/Nyrk0/ai-cli-chat-logger.svg)
![GitHub forks](https://img.shields.io/github/forks/Nyrk0/ai-cli-chat-logger.svg)
![GitHub issues](https://img.shields.io/github/issues/Nyrk0/ai-cli-chat-logger.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/Nyrk0/ai-cli-chat-logger.svg)

---

**🚀 Ready to get started? Run `./install.sh` and you'll be monitoring AI conversations in under a minute!**