#!/usr/bin/env python3
"""
Path Manager for Chat Monitoring System
Provides centralized path resolution and configuration management.
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional


class PathManager:
    """Manages file paths and configuration for the chat monitoring system."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize PathManager with optional config file path.
        
        Args:
            config_path: Optional path to config.json file
        """
        self.project_root = self._find_project_root()
        self.config_path = config_path or os.path.join(self.project_root, 'config/config.json')
        self.config = self._load_config()
    
    def _find_project_root(self) -> str:
        """Find the project root directory."""
        # Start from current file location and work up
        current = Path(__file__).parent.parent.parent.parent.absolute()  # Go up to bchat root from core/src/utils/
        
        # Look for indicators of project root
        indicators = ['config/config.json', 'README.md', 'bin/bchat', 'core/src/chat_monitor.py']
        
        while current != current.parent:
            if any((current / indicator).exists() for indicator in indicators):
                return str(current)
            current = current.parent
        
        # Fallback to bchat project root (parent of core/src directory)
        return str(Path(__file__).parent.parent.parent.parent.absolute())
    
    def _load_config(self) -> Dict:
        """Load configuration from config.json."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Return default configuration if config file is missing or invalid
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "system": {
                "project_name": "chat_backup_system",
                "version": "1.0.0",
                "log_level": "INFO"
            },
            "paths": {
                "project_root": "",
                "chats_dir": "chats",
                "logs_dir": "logs",
                "claude_log": "chats/claude_current_day_raw.log",
                "gemini_log": "chats/gemini_current_day_raw.log",
                "chat_index": "chats/chat_index.json",
                "context_summary": "chats/context_summary.json"
            },
            "monitoring": {
                "enabled": True,
                "watch_interval": 1.0,
                "debounce_delay": 2.0,
                "triggers": ["bchat"],
                "auto_start": True,
                "max_file_size_mb": 50
            },
            "keywords": {
                "trigger_words": ["bchat"],
                "filter_keywords": ["bug", "error", "fix", "config", "workflow", "stage", "implementation", "claude", "code", "debug"],
                "error_patterns": ["error:.*", "exception:.*", "failed:.*", "traceback:.*"]
            }
        }
    
    def get_project_root(self) -> Path:
        """Get the project root directory."""
        return Path(self.project_root)
    
    def get_chats_dir(self) -> Path:
        """Get the chats directory path."""
        chats_dir = self.config.get('paths', {}).get('chats_dir', 'chats')
        chats_path = Path(chats_dir)
        if chats_path.is_absolute():
            return chats_path
        return self.get_project_root() / chats_dir
    
    def get_logs_dir(self) -> Path:
        """Get the logs directory path."""
        logs_dir = self.config.get('paths', {}).get('logs_dir', 'logs')
        logs_path = Path(logs_dir)
        if logs_path.is_absolute():
            return logs_path
        return self.get_project_root() / logs_dir
    
    def get_claude_log_path(self) -> Path:
        """Get the Claude log file path."""
        claude_log = self.config.get('paths', {}).get('claude_log', 'chats/claude_current_day_raw.log')
        claude_log_path = Path(claude_log)
        if claude_log_path.is_absolute():
            return claude_log_path
        return self.get_project_root() / claude_log
    
    def get_gemini_log_path(self) -> Path:
        """Get the Gemini log file path."""
        gemini_log = self.config.get('paths', {}).get('gemini_log', 'chats/gemini_current_day_raw.log')
        gemini_log_path = Path(gemini_log)
        if gemini_log_path.is_absolute():
            return gemini_log_path
        return self.get_project_root() / gemini_log
    
    def get_chat_index_path(self) -> Path:
        """Get the chat index file path."""
        chat_index = self.config.get('paths', {}).get('chat_index', 'chats/chat_index.json')
        chat_index_path = Path(chat_index)
        if chat_index_path.is_absolute():
            return chat_index_path
        return self.get_project_root() / chat_index
    
    def get_context_summary_path(self) -> Path:
        """Get the context summary file path."""
        context_summary = self.config.get('paths', {}).get('context_summary', 'chats/context_summary.json')
        context_summary_path = Path(context_summary)
        if context_summary_path.is_absolute():
            return context_summary_path
        return self.get_project_root() / context_summary
    
    def ensure_directories(self):
        """Ensure all required directories exist."""
        directories = [
            self.get_chats_dir(),
            self.get_logs_dir(),
            os.path.dirname(self.get_claude_log_path()),
            os.path.dirname(self.get_gemini_log_path()),
            os.path.dirname(self.get_chat_index_path()),
            os.path.dirname(self.get_context_summary_path())
        ]
        
        for directory in set(directories):  # Remove duplicates
            os.makedirs(directory, exist_ok=True)
    
    def get_config_value(self, *keys, default=None):
        """
        Get a configuration value using dot notation.
        
        Args:
            keys: Keys to traverse in the config dict
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        current = self.config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def __str__(self) -> str:
        """String representation of PathManager."""
        return f"PathManager(project_root='{self.project_root}', config='{self.config_path}')"
    
    def __repr__(self) -> str:
        """Detailed representation of PathManager."""
        return f"PathManager(project_root='{self.project_root}', config_path='{self.config_path}', chats_dir='{self.get_chats_dir()}')"


if __name__ == "__main__":
    # Test the PathManager
    pm = PathManager()
    print(f"Project Root: {pm.get_project_root()}")
    print(f"Chats Directory: {pm.get_chats_dir()}")
    print(f"Claude Log: {pm.get_claude_log_path()}")
    print(f"Gemini Log: {pm.get_gemini_log_path()}")
    print(f"Chat Index: {pm.get_chat_index_path()}")
    
    # Ensure directories exist
    pm.ensure_directories()
    print("All directories ensured.")