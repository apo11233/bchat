# SuperClaude | Automate Git Documentation with AI

> A complete guide to automating your Git documentation. One CLI that handles commit messages, changelogs, and code reviews automatically.

https://www.superclaude.sh/

### Before SuperClaude
* ✗ Manually writing "fix stuff" commit messages.
* ✗ Writing vague code reviews yourself.
* ✗ Spending hours writing changelogs manually.
* ✗ Forgetting what you changed last week.

### After SuperClaude
* ✓ AI writes perfect commit messages automatically.
* ✓ One command generates comprehensive code reviews.
* ✓ Beautiful changelogs created from your git history.
* ✓ Never lose track of your development progress.

https://www.youtube.com/watch?v=4f71SUKPWCw

## Why you’ll love it

*   **Git-based Checkpoints & Session History**: Navigate back to any point in a conversation or debugging session using a Git-integrated checkpoint system — no more losing context or digging through logs.
*   **Token-Optimized Documentation**: Documentation is automatically generated using a token-reduction strategy. Code examples, API references, and usage notes follow a structured, repeatable template — ensuring docs evolve alongside your work.
*   **Lean Context, Larger Scope**: Our 70% token-reduction pipeline keeps prompts compact and efficient, allowing Claude to manage larger, more complex projects without slowing down.

## Built-in intelligence

*   **Evidence-Based Decisions**: No more "this is better" without proof.
*   **Smart model routing**: Picks the right Claude variant for the job.
*   **Intelligent Tool Integration**:
    *   **Auto Documentation Lookup**: Context7 finds library docs instantly.
    *   **Complex Analysis**: Sequential thinking for deep problems.
    *   **UI Generation**: Magic creates React components.
    *   **Browser Testing**: Puppeteer validates your work.

## Why SuperClaude?

*   **Before**: Generic AI assistance
*   **After**: Specialized, context-aware development partner
*   ✅ Consistent workflows across all projects
*   ✅ Research-first approach → Always finds official docs
*   ✅ Quality standards → Built-in best practices
*   ✅ Cognitive specialization → Right mindset for each task

## Zero-friction install

```bash
git clone https://github.com/NomenAK/SuperClaude.git
cd SuperClaude
./install.sh
```

*Auto-Backup integrated! Should be compatible with any of your MCPs.*
*That’s it—no databases, no extra services. Installs to `~/.claude/` and works in every Claude Code project.*

## Get Started in 60 Seconds

1.  **Install SuperClaude**
    ```bash
    npm install -g superclaude
    ```
2.  **Setup Claude CLI (one time only)**
    ```bash
    npm install -g @anthropic-ai/claude-code && claude
    ```
    Choose your auth method: Claude Pro/Team subscription, Anthropic Console, or Enterprise.
3.  **Use anywhere, anytime**
    ```bash
    cd your-project
    superclaude commit # Perfect commit messages, instantly
    ```

## Commands

SuperClaude provides a comprehensive set of commands to cover the entire development lifecycle. These commands are organized into several categories:

### Development Commands

These commands cover the main software development lifecycle:

*   **/sc:build**: Used for building the application, with flags for different technologies like `--react` or for specific approaches like `--tdd` (Test-Driven Development).
*   **/sc:design**: Helps with system design, including options like `--api` for API design and `--ddd` for Domain-Driven Design.
*   **/sc:implement**: To implement new features.
*   **/sc:test**: For running tests.
*   **/sc:deploy**: To handle deployment tasks.

### Analysis and Review

These commands are for understanding and improving existing code:

*   **/sc:analyze**: Can be used to profile performance, check for security issues, or analyze the architecture.
*   **/sc:review**: For code reviews, checking against security, performance, and best practices.
*   **/sc:troubleshoot**: To investigate and fix bugs.
*   **/sc:explain**: To get an explanation of a piece of code.
*   **/sc:cleanup**: To refactor and clean up code.

### Other Commands

*   **/sc:document**: For generating documentation.
*   **/sc:git**: Integrates with Git for version control tasks like creating checkpoints and rolling back changes.
*   **/sc:estimate**: To estimate the effort for a task.
*   **/sc:task**: For task management.
*   **/sc:index**: To index the codebase.
*   **/sc:load**: To load a context or a file.
*   **/sc:spawn**: To create a new agent or process.

### How to Use

To use these commands, you typically type them in your Claude Code interface, starting with a slash (`/`). For example:

```bash
/sc:build --react --magic --tdd
/sc:analyze --code --persona-architect
```

## Global Flags

*   `--interactive`, `-i`: Interactive mode - review and edit before committing
*   `--verbose`, `-v`: Verbose mode - see detailed progress and AI thinking process
*   `--verify`: Force full dependency verification (bypass cache)

## Personas

Switch Claude’s mindset in a heartbeat—manually or automatically:

| Persona      | Focus                       |
| :----------- | :-------------------------- |
| architect    | big-picture system design   |
| frontend     | React & UX polish           |
| backend      | API reliability & scale     |
| security     | threat modeling & secure code |
| analyzer     | deep-dive debugging         |
| qa           | test strategy & coverage    |
| performance  | speed tuning                |
| refactorer   | code clarity & cleanup      |
| mentor       | guided learning & coaching  |

## Team Workflows

Add these to your `package.json` for consistent team workflows:

```json
{
  "scripts": {
    "commit": "superclaude commit --interactive",
    "release:prep": "superclaude changelog && superclaude readme",
    "code:review": "superclaude review --verbose",
    "docs:update": "superclaude docs"
  }
}
```

## Privacy & Security

**Your Code Never Leaves Your Control**

SuperClaude is a CLI tool that runs locally on your machine. There are no SuperClaude servers, databases, or analytics. Your code only goes to the services you already trust: Claude AI and GitHub.

*   ✅ **Local Processing**: All operations happen on your machine
*   ✅ **No Tracking**: SuperClaude doesn't collect, store, or analyze your data
*   ✅ **Open Source**: Full transparency - inspect the code on GitHub
*   ✅ **Direct API Calls**: SuperClaude only talks to Claude AI and GitHub - no middleman

**Data Flow**: Your Machine → Claude AI (for analysis) → GitHub (for commits) → Your Machine

**SuperClaude Servers**: None. SuperClaude is just a CLI library - no servers exist.

## Common Issues

### Claude authentication failed
Make sure Claude CLI is properly authenticated:
```bash
claude
```
Follow the prompts to authenticate with your preferred method (Pro/Team subscription, API key, or Enterprise).

### Not in a git repository
SuperClaude needs to be run inside a git repository:
```bash
git init # Initialize git repo
git remote add origin https://github.com/username/repo # Add remote
```

### GitHub authentication issues
For best results, set up global GitHub authentication:
```bash
# Option 1: GitHub CLI (recommended)
brew install gh && gh auth login

# Option 2: SSH key
ssh-keygen -t ed25519 -C "your@email.com"
# Then add to GitHub: https://github.com/settings/keys
```

## Real World Examples

### Daily workflow
```bash
# Make some changes
echo "new feature" >> src/feature.js

# Perfect commit message instantly
superclaude commit
# ✅ Output: "feat: add user authentication with JWT tokens"

# Update docs automatically  
superclaude readme
# ✅ Professional README with new feature documented

# Prepare for release
superclaude changelog
# ✅ Human-readable release notes
```

### Before a release
```bash
# Get comprehensive code review
superclaude review --verbose

# Update all documentation
superclaude readme && superclaude docs

# Generate release changelog
superclaude changelog

# Everything ready for release!
```
---
[Back to Home](https://www.reddit.com/r/ClaudeAI/comments/1lhmts3/i_present_superclaude/) | [GitHub](https://github.com/NomenAK/SuperClaude) | [NPM](https://www.npmjs.com/package/superclaude)

*Made with ❤️ for developers who hate repetitive tasks*

*Made by gwendall • [GitHub](https://github.com/gwendall) • [Twitter](https://twitter.com/gwendall)*


