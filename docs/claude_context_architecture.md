# Claude Code: Context and Persistence Architecture

This document summarizes the key mechanisms that Claude Code uses for context memory and persistence across sessions. This information is foundational for the `bchat` Deep Context Engine.

## 1. `CLAUDE.md` Files: The Primary Context Source

`CLAUDE.md` files are the primary mechanism for storing reusable instructions, preferences, and project details. They are loaded automatically at startup.

### 1.1. Hierarchical Structure

`CLAUDE.md` files operate in a hierarchical structure, allowing for different scopes of context:

*   **Enterprise/Organization Level**: Located in system-wide directories (e.g., `/Library/Application Support/ClaudeCode/CLAUDE.md`). Used for shared company policies.
*   **Project Level**: Located at `./CLAUDE.md` in the project directory. Used for team-shared project details and checked into source control.
*   **User Level**: Located at `~/.claude/CLAUDE.md`. Used for personal preferences that apply across all projects.

### 1.2. Persistence and Modification

*   **Automatic Loading**: Claude Code recursively scans the current directory upwards to find and load all relevant `CLAUDE.md` files.
*   **In-Session Modification**: Users can add to these files during a session by:
    *   Using the `#` prefix in a prompt (e.g., `# Always use TypeScript`).
    *   Using the `/memory` slash command.

### 1.3. Imports

*   `CLAUDE.md` files can import other files using the `@path/to/file` syntax.
*   Imports can be recursive up to 5 levels deep.

## 2. Conversation History

Full conversation transcripts are saved locally to provide a resumable session history.

*   **Location**: `~/.claude/conversations/`
*   **Retention**: The retention period is configurable (default: 30 days) in `settings.json` via the `cleanupPeriodDays` key.
*   **Resuming Sessions**:
    *   `claude -c` or `--continue`: Resumes the most recent conversation.
    *   `claude -r <session-id>` or `--resume <session-id>`: Resumes a specific session.

## 3. Additional State Management

*   **`settings.json`**: These files, located at the user (`~/.claude/`) and project (`.claude/`) levels, store settings like tool permissions and environment variables.
*   **Model Context Protocol (MCP)**: An advanced feature for integrating with external, long-term memory services.

## 4. Limitations

*   **Conversation History vs. Full Context**: Resuming a session restores the transcript, but not necessarily the full state (e.g., tool outputs).
*   **Local Memory**: The context is local to the machine. Cross-device memory requires external tools like MCP.
*   **Token Limits**: Large `CLAUDE.md` files can consume a significant portion of the context window.

## 5. Implications for `bchat`

This architecture has significant implications for the `bchat` Deep Context Engine:

*   The `ContextExtractor` should be designed to find and parse both the `CLAUDE.md` files and the conversation history files.
*   This is a more robust and reliable source of context than the internal `shell-snapshots` and `todos` files.
*   The `bchat` engine can provide significant value by creating a unified view of this distributed context.
