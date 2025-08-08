# 🤝 Contributing to AI CLI Chat Monitor

Thank you for considering contributing to AI CLI Chat Monitor! We welcome contributions from developers of all experience levels.

## 🚀 Quick Start for Contributors

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/bchat.git
cd bchat

# Add the original repository as upstream
git remote add upstream https://github.com/Nyrk0/bchat.git
```

### 2. Set Up Development Environment
```bash
# Install dependencies
pip3 install -r requirements.txt

# Install development tools
pip3 install pytest black flake8 mypy

# Copy environment template
cp .env.example .env
# Add your GOOGLE_API_KEY to .env

# Test installation
./install.sh
```

### 3. Create Feature Branch
```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

## 🔥 High Priority Contribution Areas

### Windows Support (Most Wanted!)
- **Windows installer script** - Adapt `install.sh` for Windows/PowerShell
- **Windows path handling** - Ensure path resolution works on Windows
- **Windows testing** - Verify functionality on different Windows versions

### Cross-Platform Improvements
- **Linux distribution testing** - Test on Ubuntu, Debian, Fedora, Arch, etc.
- **Shell compatibility** - Ensure compatibility with bash, zsh, fish
- **Package managers** - Add support for different package managers

### Features & Enhancements
- **Web dashboard** - Browser interface for viewing chat analytics
- **Search functionality** - Search through chat history and summaries
- **Export features** - Export to PDF, HTML, Markdown formats
- **Performance optimization** - Async processing, better caching

## 📝 Development Guidelines

### Code Style
- **Python**: Follow PEP 8, use `black` for formatting
- **Shell scripts**: Use shellcheck-compliant bash
- **Documentation**: Clear docstrings and comments

### Testing
```bash
# Run tests (when available)
pytest

# Check code style
black --check src/
flake8 src/

# Type checking
mypy src/
```

### Commit Messages
Use clear, descriptive commit messages:
```bash
# Good examples
git commit -m "Add Windows PowerShell installer script"
git commit -m "Fix path resolution on Windows systems"
git commit -m "Update README with Windows installation instructions"

# Avoid
git commit -m "fix stuff"
git commit -m "update"
```

## 🛠️ Specific Contribution Instructions

### Adding Windows Support

**Priority: HIGH** 🔥

1. **Create Windows installer:**
   ```powershell
   # Create install.ps1 or install.bat
   # Should handle:
   # - Python dependency installation
   # - Node.js/npm package installation  
   # - Directory creation
   # - Configuration file setup
   # - Symlink creation (or PATH modification)
   ```

2. **Update path handling:**
   ```python
   # In src/utils/path_manager.py
   # Ensure Windows path separators work
   # Handle Windows-specific path patterns
   ```

3. **Test on Windows:**
   - Windows 10/11
   - PowerShell vs CMD
   - Different Python installations (python.org, Anaconda, etc.)

### Improving Installation Process

1. **Add package manager support:**
   ```bash
   # Add support for:
   # - Homebrew (macOS)
   # - apt/yum/pacman (Linux)
   # - Chocolatey/Scoop (Windows)
   ```

2. **Better error handling:**
   ```bash
   # Improve install.sh with:
   # - Better error messages
   # - Dependency checking
   # - Recovery suggestions
   ```

### Adding New AI Platform Support

1. **Create new wrapper:**
   ```bash
   # Follow pattern of bchat/gemini_wrapper.sh
   # Add support for:
   # - OpenAI CLI
   # - Anthropic Claude variants
   # - Local AI models
   ```

2. **Update monitoring:**
   ```python
   # In src/chat_monitor.py
   # Add log file patterns for new AI platforms
   # Extend parsing logic
   ```

## 🧪 Testing Guidelines

### Manual Testing Checklist

Before submitting a PR, please test:

**Installation:**
- [ ] Fresh installation on clean system
- [ ] Installation with existing chat_monitor
- [ ] Installation without required dependencies

**Basic functionality:**
- [ ] `bchat` command works from any directory
- [ ] Chat monitoring detects new conversations
- [ ] Daily consolidation works correctly
- [ ] API integration functions properly

**Cross-platform (if applicable):**
- [ ] Test on target operating system
- [ ] Verify path handling
- [ ] Check shell compatibility

### Automated Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_installation.py
pytest tests/test_monitoring.py
pytest tests/test_api.py

# Run with coverage
pytest --cov=src tests/
```

## 📋 Pull Request Process

### Before Submitting

1. **Update your fork:**
   ```bash
   git checkout main
   git fetch upstream
   git merge upstream/main
   git push origin main
   ```

2. **Rebase your feature branch:**
   ```bash
   git checkout feature/your-feature
   git rebase main
   ```

3. **Test thoroughly:**
   - Run automated tests
   - Manual testing on target platform
   - Check code style and formatting

### PR Submission

1. **Create descriptive PR:**
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Screenshots for UI changes
   - Instructions for testing

2. **Link related issues:**
   ```markdown
   Closes #123
   Related to #456
   ```

3. **Mark as draft if work in progress**

### PR Review Process

- Maintainers will review within 1-2 weeks
- Address feedback promptly
- Keep discussion focused and professional
- Be open to suggestions and changes

## 🐛 Bug Reports

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Update to latest version** to see if bug still exists
3. **Test with minimal configuration** to isolate the issue

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what the bug is.

**To Reproduce**
1. Step 1
2. Step 2
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. macOS 12.6, Ubuntu 22.04, Windows 11]
- Python version: [e.g. 3.9.1]
- Chat Monitor version: [e.g. 1.0.0]

**Additional context**
- Log files
- Configuration files
- Screenshots if applicable
```

## 💡 Feature Requests

We welcome feature requests! Please:

1. **Check existing issues** for similar requests
2. **Describe the use case** - why is this feature needed?
3. **Propose implementation** if you have ideas
4. **Consider contributing** the feature yourself!

## 📞 Getting Help

- **Discussions:** Use GitHub Discussions for questions
- **Issues:** Use GitHub Issues for bugs and feature requests
- **Email:** [Contact maintainers] for security issues

## 🏆 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Recognized in the project README

## 📄 Code of Conduct

Be respectful, inclusive, and professional in all interactions. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).

---

**Thank you for contributing to AI CLI Chat Monitor! 🚀**