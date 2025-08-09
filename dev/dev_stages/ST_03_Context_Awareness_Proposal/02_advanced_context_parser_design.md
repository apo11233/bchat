# Design: Advanced Context Parsers (Claude-Enhanced)

**Date**: 2025-08-09
**Stage**: ST_03 (Context Awareness Proposal)
**Author**: Gemini Assistant, with feedback from Claude
**Status**: PROPOSED

## 1. Overview

This document outlines the technical design for the new parsers required to process the advanced context data sources discovered in the `~/.claude` directory. This design has been significantly improved based on direct feedback from Claude.

## 2. Data Source Analysis (Revised)

Our analysis of the data sources has been refined based on Claude's feedback.

### 2.1. `shell-snapshots`

*   **Format**: A shell script (zsh) containing a complete snapshot of the shell environment.
*   **Key Information**: The most valuable data is the *change* in the environment between snapshots. This includes new functions, aliases, and exports.
*   **Refined Parsing Strategy**: The parser must use more robust regex to capture multiple function definition formats. It should also extract aliases and exports. The filename contains a Unix millisecond timestamp which must be used for sorting.

### 2.2. `todos`

*   **Format**: A JSON array of objects, where each object represents a single to-do item.
*   **Key Information**: The `content`, `status`, and `priority` of each to-do item.
*   **Refined Parsing Strategy**: The parser should categorize todos by status and priority to provide more structured context. The filenames are UUID-based, so they must be sorted by modification time, not by name.

## 3. Parser Design (Claude's Recommendations)

We will adopt the improved parser designs recommended by Claude.

### 3.1. `ShellSnapshotParser` (Enhanced)

```python
class ShellSnapshotParser:
    """Parses Claude's shell snapshot files."""

    def _extract_timestamp(self, filename: str) -> int:
        match = re.search(r'snapshot-zsh-(\d+)-', filename)
        return int(match.group(1)) if match else 0

    def parse(self, file_path: Path) -> Dict:
        """Parses a single snapshot file and extracts key information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            func_patterns = [
                r'^(\w+)\s*\(\)\s*\{\',          # funcname () {
                r'^function\s+(\w+)\s*\{\',
                r'^(\w+)\s*\(\)\s*\n\{\',        # funcname ()
        ]
            all_functions = set()
            for pattern in func_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                all_functions.update(matches)

            aliases_matches = re.findall(r'^alias\s+(\w+)=', content, re.MULTILINE)
            exports_matches = re.findall(r'^export\s+(\w+)=', content, re.MULTILINE)

            return {
                'functions': list(all_functions),
                'aliases': aliases_matches,
                'exports': exports_matches,
                'timestamp': self._extract_timestamp(file_path.name)
            }
        except Exception as e:
            logging.warning(f"Could not parse shell snapshot {file_path}: {e}")
            return {}
```

### 3.2. `TodoParser` (Enhanced)

```python
class TodoParser:
    """Parses Claude's todo list files."""

    def parse(self, file_path: Path) -> Dict:
        """Parses a todo file and categorizes the tasks."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                todos = json.load(f)

            categorized = {
                'completed': [], 'in_progress': [], 'pending': [], 'high_priority': []
            }

            for todo in todos:
                status = todo.get('status', 'unknown')
                content = todo.get('content', '')
                priority = todo.get('priority', 'normal')

                if status in categorized:
                    categorized[status].append(content)
                if priority == 'high':
                    categorized['high_priority'].append(content)

            return categorized
        except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
            logging.warning(f"Could not parse todo file {file_path}: {e}")
            return {}
```

## 4. `ContextExtractor` Integration (Claude's Architecture)

We will adopt the more sophisticated architecture recommended by Claude.

```python
class ContextExtractor:
    # ... (existing code) ...

    def extract_advanced_context(self, provider: str, max_files: int = 5) -> str:
        if provider.lower() != 'claude':
            return ""

        claude_dir = Path.home() / '.claude'

        # Get recent snapshots and analyze changes
        snapshots = self._get_recent_files(claude_dir / 'shell-snapshots', max_files)
        snapshot_context = self._analyze_snapshot_changes(snapshots)

        # Get recent todos and extract meaningful tasks
        recent_todos = self._get_recent_files(claude_dir / 'todos', max_files)
        todo_context = self._extract_meaningful_todos(recent_todos)

        return f"{snapshot_context}\n{todo_context}".strip()

    # ... (implementation of _get_recent_files, _analyze_snapshot_changes, etc. to follow)
```

## 5. Critical Edge Cases & Pitfalls (from Claude)

*   **File Selection**: The `_find_latest_file` approach is insufficient. We need a `_get_recent_files` method that can handle both timestamped and UUID-named files (by using file modification time for the latter).
*   **Performance**: Shell snapshots can be large. We must consider streaming or line-by-line parsing if performance becomes an issue.
*   **Data Quality**: The parsers must be enhanced to filter out sensitive environment variables from snapshots and to identify non-user-defined system functions.

## 6. Next Steps

This enhanced design is ready for review. Upon approval, I will begin implementing these new, more robust parsers and integrating them into the `ContextExtractor`.