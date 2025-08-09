#!/usr/bin/env python3
"""
Context-Aware Prompting Engine for bchat
"""

import os
import sys
import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional

class ContextualQueryAnalyzer:
    """Analyzes a prompt to determine if it is a contextual query."""

    def __init__(self):
        self.contextual_keywords = ["remember", "recall", "what was", "what were", "what did", "what does", "find", "search for", "in our last conversation", "from last week"]
        self.provider_keywords = ["claude", "gemini"]

    def analyze(self, prompt: str) -> Dict:
        """Analyzes the prompt and returns the analysis result."""
        prompt_lower = prompt.lower()
        is_contextual = any(keyword in prompt_lower for keyword in self.contextual_keywords)

        search_keywords = []
        provider_filter = None

        if is_contextual:
            search_keywords = [word.strip('.,!?') for word in prompt.split() if len(word) > 3]
            for provider in self.provider_keywords:
                if provider in prompt_lower:
                    provider_filter = provider
                    search_keywords = [kw for kw in search_keywords if kw.lower() != provider]

        return {
            "is_contextual": is_contextual,
            "provider_filter": provider_filter,
            "search_keywords": search_keywords
        }

class ChatIndexSearcher:
    """Searches the chat index for relevant conversations."""

    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.index_data = self._load_index()

    def _load_index(self) -> List[Dict]:
        if not self.index_path.exists():
            return []
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def search(self, keywords: List[str], provider_filter: Optional[str] = None, limit: int = 3) -> List[Dict]:
        if not self.index_data:
            return []

        scored_entries = []
        for entry in self.index_data:
            if provider_filter and entry.get('ai_source', '').lower() != provider_filter.lower():
                continue

            score = 0
            for keyword in keywords:
                if keyword.lower() in entry.get('executive_summary', '').lower():
                    score += 2
                if keyword.lower() in " ".join(entry.get('keywords', [])).lower():
                    score += 1
            
            if score > 0:
                score += entry.get('relevance_score', 0)
                scored_entries.append({"score": score, "entry": entry})

        scored_entries.sort(key=lambda x: x['score'], reverse=True)
        return [item['entry'] for item in scored_entries[:limit]]

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
                r'^(\w+)\s*\(\)\s*\{\n',          # funcname () {
                r'^function\s+(\w+)\s*\{\n',      # function funcname {
                r'^(\w+)\s*\(\)\s*\n\{\n',        # funcname ()
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

class ClaudeMdParser:
    """Parses Claude.md files, handling imports and hierarchy."""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def parse_hierarchy(self, start_dir: Path) -> str:
        """Finds and parses the full hierarchy of Claude.md files."""
        # System-level (platform specific)
        if sys.platform == "darwin":
            system_path = Path("/Library/Application Support/ClaudeCode/CLAUDE.md")
        else:
            system_path = Path("/etc/claude/CLAUDE.md")

        # User-level
        user_path = Path.home() / ".claude" / "CLAUDE.md"

        # Project-level (scan upwards from start_dir)
        project_paths = []
        current_dir = start_dir
        while True:
            project_path = current_dir / "CLAUDE.md"
            if project_path.exists():
                project_paths.append(project_path)
            
            if current_dir == current_dir.parent:
                break
            current_dir = current_dir.parent

        # Combine and parse in order of precedence (project -> user -> system)
        all_paths = list(reversed(project_paths)) + [user_path, system_path]
        full_context = []
        for path in all_paths:
            if path.exists():
                full_context.append(self._parse_file(path))
        
        return "\n---\
".join(full_context)

    def _parse_file(self, file_path: Path, recursion_depth: int = 0) -> str:
        """Parses a single Claude.md file, recursively handling imports."""
        if recursion_depth > 5:
            logging.warning(f"Max recursion depth reached for imports in {file_path}")
            return ""

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import_pattern = r'^@(\S+)'
            lines = content.split('\n')
            processed_lines = []
            for line in lines:
                match = re.match(import_pattern, line)
                if match:
                    import_path_str = match.group(1)
                    import_path = file_path.parent / import_path_str
                    if import_path.exists():
                        imported_content = self._parse_file(import_path, recursion_depth + 1)
                        processed_lines.append(f"--- Imported content from {import_path_str} ---\n{imported_content}\n--- End of import ---")
                    else:
                        logging.warning(f"Imported file not found: {import_path}")
                else:
                    processed_lines.append(line)
            
            return "\n".join(processed_lines)

        except FileNotFoundError:
            return ""

class ContextExtractor:
    """Extracts and combines context from various sources."""

    def __init__(self, chats_dir: Path, project_root: Path):
        self.chats_dir = chats_dir
        self.project_root = project_root
        self.snapshot_parser = ShellSnapshotParser()
        self.todo_parser = TodoParser()
        self.claude_md_parser = ClaudeMdParser(self.project_root)

    def extract_chat_logs(self, file_paths: List[str]) -> str:
        """Extracts and formats context from a list of bchat log files."""
        full_context = []
        for file_path in file_paths:
            try:
                full_path = self.chats_dir / file_path
                with open(full_path, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                
                context_str = f"""
---
-- Context from session {log_data.get('id')} ({log_data.get('timestamp')}) ---
Summary: {log_data.get('summary')}
Decisions: {log_data.get('sections', [{}])[0].get('items', [])}
---
"""
                full_context.append(context_str)
            except (FileNotFoundError, json.JSONDecodeError, IndexError) as e:
                logging.warning(f"Could not process file {file_path}: {e}")
                continue
        
        return "\n".join(full_context)

    def extract_advanced_context(self, provider: str, max_files: int = 3) -> str:
        """Extracts context from the advanced data sources for a given provider."""
        if provider.lower() != 'claude':
            return ""

        claude_dir = Path.home() / '.claude'
        
        # Extract from recent shell snapshots
        snapshot_context = ""
        try:
            snapshots = self._get_recent_files(claude_dir / 'shell-snapshots', max_files)
            if snapshots:
                latest_snapshot_data = self.snapshot_parser.parse(snapshots[0])
                if latest_snapshot_data.get('functions'):
                    snapshot_context = f"Claude defined the following functions: {latest_snapshot_data['functions']}"
        except Exception as e:
            logging.warning(f"Could not process shell snapshots: {e}")

        # Extract from recent todo lists
        todo_context = ""
        try:
            recent_todos = self._get_recent_files(claude_dir / 'todos', max_files)
            if recent_todos:
                all_completed_tasks = []
                for todo_file in recent_todos:
                    todo_data = self.todo_parser.parse(todo_file)
                    if todo_data.get('completed'):
                        all_completed_tasks.extend(todo_data['completed'])
                if all_completed_tasks:
                    todo_context = f"Claude recently completed the following tasks: {all_completed_tasks}"
        except Exception as e:
            logging.warning(f"Could not process todos: {e}")

        return f"{snapshot_context}\n{todo_context}".strip()

    def _get_recent_files(self, directory: Path, limit: int) -> List[Path]:
        """Gets the most recent files from a directory, sorting by modification time."""
        if not directory.exists() or not directory.is_dir():
            return []
        
        files = [f for f in directory.iterdir() if f.is_file()]
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        return files[:limit]
