#!/usr/bin/env python3
"""
Enhanced Chat Monitor with Watchdog-based File Monitoring
Monitors chat logs from multiple AI agents and provides intelligent consolidation.
"""

import os
import sys
import time
import json
import hashlib
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

# Third-party imports
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import google.generativeai as genai

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.path_manager import PathManager


class CircuitBreaker:
    """Circuit breaker pattern implementation for API resilience."""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 300):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self._lock = threading.Lock()
    
    def call(self, func, *args, **kwargs):
        with self._lock:
            if self.state == 'OPEN':
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = 'HALF_OPEN'
                else:
                    raise Exception("Circuit breaker is OPEN")
            
            try:
                result = func(*args, **kwargs)
                if self.state == 'HALF_OPEN':
                    self.state = 'CLOSED'
                    self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = 'OPEN'
                
                raise e


class APIManager:
    """Manages API calls with error handling, retries, and rate limiting."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api_config = config.get('api', {})
        self.error_config = config.get('error_handling', {})
        self.provider = self.api_config.get('provider', 'gemini').lower()
        
        # Initialize APIs based on provider
        if self.provider == 'gemini':
            self._initialize_gemini()
        elif self.provider == 'claude':
            self._initialize_claude()
        else:
            raise ValueError(f"Unsupported API provider: {self.provider}")
        
        # Initialize common components
        self._initialize_common()
    
    def _initialize_gemini(self):
        """Initialize Gemini API."""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required for Gemini")
        
        genai.configure(api_key=api_key)
        gemini_config = self.api_config.get('gemini', {})
        model_name = gemini_config.get('model', 'gemini-2.5-flash')
        self.model = genai.GenerativeModel(model_name=model_name)
    
    def _initialize_claude(self):
        """Initialize Claude API."""
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required for Claude")
        
        self.claude_config = self.api_config.get('claude', {})
        self.claude_model = self.claude_config.get('model', 'claude-3-5-sonnet-20241022')
        self.claude_api_url = 'https://api.anthropic.com/v1/messages'
        
    def _initialize_common(self):
        """Initialize common components after API setup."""
        # Circuit breaker for API resilience
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=self.error_config.get('circuit_breaker_threshold', 5),
            recovery_timeout=self.error_config.get('circuit_breaker_timeout', 300)
        )
        
        # Rate limiting
        self.rate_limit = self.api_config.get('rate_limit_requests_per_minute', 60)
        self.request_times = []
        self._rate_limit_lock = threading.Lock()
    
    def _check_rate_limit(self):
        """Enforce rate limiting."""
        with self._rate_limit_lock:
            now = time.time()
            # Remove requests older than 1 minute
            self.request_times = [t for t in self.request_times if now - t < 60]
            
            if len(self.request_times) >= self.rate_limit:
                sleep_time = 60 - (now - self.request_times[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
            
            self.request_times.append(now)
    
    def _exponential_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        base = self.error_config.get('exponential_backoff_base', 2)
        max_backoff = self.error_config.get('max_backoff_seconds', 60)
        delay = min(base ** attempt, max_backoff)
        return delay
    
    def call_api(self, content: str, ai_source: str, prompt_type: str = 'summarize') -> Dict:
        """Make API call with error handling and retries."""
        max_retries = self.api_config.get('max_retries', 3)
        
        for attempt in range(max_retries + 1):
            try:
                self._check_rate_limit()
                
                # Prepare prompt based on type
                if prompt_type == 'summarize':
                    prompt = self._create_summarization_prompt(content, ai_source)
                elif prompt_type == 'extract_entities':
                    prompt = self._create_entity_extraction_prompt(content, ai_source)
                else:
                    prompt = content
                
                # Make API call through circuit breaker based on provider
                if self.provider == 'gemini':
                    response = self.circuit_breaker.call(
                        self._make_gemini_request,
                        prompt
                    )
                elif self.provider == 'claude':
                    response = self.circuit_breaker.call(
                        self._make_claude_request,
                        prompt
                    )
                else:
                    raise ValueError(f"Unsupported provider: {self.provider}")
                
                return self._parse_response(response)
                
            except Exception as e:
                logging.warning(f"API call attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < max_retries:
                    delay = self._exponential_backoff(attempt)
                    time.sleep(delay)
                else:
                    # Final attempt failed, return error response
                    return {
                        "error": f"API call failed after {max_retries + 1} attempts: {str(e)}",
                        "summary": "API temporarily unavailable",
                        "decisions": [],
                        "errors": [str(e)],
                        "configurations": []
                    }
    
    def _make_gemini_request(self, prompt: str):
        """Make Gemini API request."""
        generation_config = {
            "response_mime_type": "application/json",
            "max_output_tokens": self.api_config.get('max_tokens', 4096),
            "temperature": self.api_config.get('temperature', 0.3)
        }
        
        response = self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        return response
    
    def _make_claude_request(self, prompt: str):
        """Make Claude API request."""
        import requests
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.anthropic_api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.claude_model,
            "max_tokens": self.api_config.get('max_tokens', 4096),
            "temperature": self.api_config.get('temperature', 0.3),
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = requests.post(
            self.claude_api_url,
            headers=headers,
            json=data,
            timeout=self.api_config.get('timeout', 30)
        )
        
        if response.status_code != 200:
            raise Exception(f"Claude API error: {response.status_code} - {response.text}")
        
        return response
    
    def _create_summarization_prompt(self, content: str, ai_source: str) -> str:
        """Create a prompt for content summarization."""
        return f"""
Analyze the following {ai_source} chat history and generate a structured JSON summary.

Content:
{content}

Please provide a JSON response with the following structure:
{{
    "summary": "Brief executive summary of the session",
    "decisions": ["Key decisions made during the session"],
    "errors": ["Errors encountered and their solutions"],
    "configurations": ["Configuration changes or settings modified"],
    "key_topics": ["Main topics discussed"],
    "files_modified": ["Files that were created, modified, or deleted"],
    "commands_executed": ["Important commands or operations performed"]
}}

Focus on extracting actionable information and key insights that would be useful for context in future sessions.
"""
    
    def _create_entity_extraction_prompt(self, content: str, ai_source: str) -> str:
        """Create a prompt for entity extraction."""
        return f"""
Extract structured entities from this {ai_source} chat log.

Content:
{content}

Return JSON with these entities:
{{
    "files_modified": ["file paths mentioned"],
    "key_decisions": ["important decisions made"],
    "errors_fixed": ["errors that were resolved"],
    "database_tables": ["database tables mentioned"],
    "api_endpoints": ["API endpoints discussed"],
    "commands_executed": ["shell or system commands"],
    "configurations_changed": ["config files or settings modified"]
}}
"""
    
    def _parse_response(self, response) -> Dict:
        """Parse API response and handle errors."""
        try:
            if self.provider == 'gemini':
                # Gemini response format
                if hasattr(response, 'text'):
                    return json.loads(response.text)
                else:
                    return {"error": "Invalid Gemini response format"}
            elif self.provider == 'claude':
                # Claude response format
                response_data = response.json()
                content = response_data.get('content', [])
                if content and len(content) > 0:
                    text_content = content[0].get('text', '')
                    return json.loads(text_content)
                else:
                    return {"error": "Invalid Claude response format"}
            else:
                return {"error": f"Unknown provider: {self.provider}"}
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse API response as JSON: {e}")
            return {
                "error": "Failed to parse response",
                "summary": "Content processed but parsing failed",
                "decisions": [],
                "errors": [],
                "configurations": []
            }


class ChatLogHandler(FileSystemEventHandler):
    """Handles file system events for chat log monitoring."""
    
    def __init__(self, monitor: 'ChatMonitor'):
        self.monitor = monitor
        self.debounce_delay = monitor.config.get('monitoring', {}).get('debounce_delay', 2.0)
        self.pending_events = {}
        self._lock = threading.Lock()
    
    def on_modified(self, event):
        """Handle file modification events with debouncing."""
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Only process relevant log files
        if not self._is_relevant_file(file_path):
            return
        
        with self._lock:
            # Cancel previous timer if exists
            if file_path in self.pending_events:
                self.pending_events[file_path].cancel()
            
            # Set up new debounced processing
            timer = threading.Timer(
                self.debounce_delay,
                self._process_file_change,
                [file_path]
            )
            self.pending_events[file_path] = timer
            timer.start()
    
    def _is_relevant_file(self, file_path: str) -> bool:
        """Check if file is a relevant chat log."""
        relevant_files = [
            self.monitor.path_manager.get_claude_log_path(),
            self.monitor.path_manager.get_gemini_log_path()
        ]
        return os.path.abspath(file_path) in [os.path.abspath(f) for f in relevant_files]
    
    def _process_file_change(self, file_path: str):
        """Process file change after debounce delay."""
        try:
            self.monitor.process_file_change(file_path)
        finally:
            with self._lock:
                if file_path in self.pending_events:
                    del self.pending_events[file_path]


class ChatMonitor:
    """Main chat monitoring system with watchdog-based file monitoring."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.path_manager = PathManager(config_path)
        self.config = self.path_manager.config
        
        # Setup logging
        self._setup_logging()
        
        # Initialize components
        self.api_manager = APIManager(self.config)
        self.observer = Observer()
        self.handler = ChatLogHandler(self)
        
        # State tracking
        self.last_processed_sizes = {}
        self.session_data = {}
        self.running = False
        
        # Ensure directories exist
        self.path_manager.ensure_directories()
        
        logging.info("Chat monitor initialized")
    
    def _setup_logging(self):
        """Configure logging based on config settings."""
        log_level = getattr(logging, self.config.get('system', {}).get('log_level', 'INFO'))
        logs_dir = self.path_manager.get_logs_dir()
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(logs_dir, 'bchat.log')),
                logging.StreamHandler(sys.stdout) if not self.config.get('error_handling', {}).get('silent_mode', True) else logging.NullHandler()
            ]
        )
    
    def start_monitoring(self):
        """Start the file monitoring system."""
        if self.running:
            logging.warning("Monitor is already running")
            return
        
        self.running = True
        
        # Set up watchdog observer
        watch_paths = [
            os.path.dirname(self.path_manager.get_claude_log_path()),
            os.path.dirname(self.path_manager.get_gemini_log_path())
        ]
        
        for path in set(watch_paths):  # Remove duplicates
            if os.path.exists(path):
                self.observer.schedule(self.handler, path, recursive=False)
                logging.info(f"Watching directory: {path}")
        
        self.observer.start()
        logging.info("Chat monitoring started")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop the monitoring system."""
        if not self.running:
            return
        
        self.running = False
        self.observer.stop()
        self.observer.join()
        logging.info("Chat monitoring stopped")
    
    def process_file_change(self, file_path: str):
        """Process changes in a chat log file."""
        try:
            # Determine AI source
            ai_source = self._get_ai_source(file_path)
            
            # Read new content
            new_content = self._read_new_content(file_path)
            
            if not new_content.strip():
                return
            
            # Check for trigger keywords
            trigger_words = self.config.get('keywords', {}).get('trigger_words', ['bckpchat'])
            has_trigger = any(trigger.lower() in new_content.lower() for trigger in trigger_words)
            
            if has_trigger:
                logging.info(f"Trigger word detected in {ai_source} log, processing immediately")
                self._process_content(new_content, ai_source, immediate=True)
            else:
                # Store for later consolidation
                self._store_content(new_content, ai_source)
        
        except Exception as e:
            logging.error(f"Error processing file change for {file_path}: {e}")
    
    def _get_ai_source(self, file_path: str) -> str:
        """Determine AI source from file path."""
        if 'claude' in file_path.lower():
            return 'Claude'
        elif 'gemini' in file_path.lower():
            return 'Gemini'
        else:
            return 'Unknown'
    
    def _read_new_content(self, file_path: str) -> str:
        """Read only new content from file since last processing."""
        try:
            current_size = os.path.getsize(file_path)
            last_size = self.last_processed_sizes.get(file_path, 0)
            
            if current_size <= last_size:
                return ""
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(last_size)
                new_content = f.read()
            
            self.last_processed_sizes[file_path] = current_size
            return new_content
            
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return ""
    
    def _process_content(self, content: str, ai_source: str, immediate: bool = False):
        """Process content using API and save results."""
        try:
            # Filter relevant content
            relevant_content = self._filter_relevant_content(content)
            
            if not relevant_content.strip():
                return
            
            # Generate summary using API
            summary_data = self.api_manager.call_api(
                relevant_content,
                ai_source,
                'summarize'
            )
            
            # Generate session data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = f"{ai_source.lower()}_{timestamp}"
            
            log_data = {
                "id": session_id,
                "timestamp": datetime.now().isoformat(),
                "stage": self._get_current_stage(),
                "ai_source": ai_source,
                "session_id": session_id,
                "content_hash": hashlib.md5(content.encode()).hexdigest(),
                "keywords": self._extract_keywords(content),
                "summary": summary_data.get("summary", "No summary available"),
                "sections": [
                    {"title": "Key Achievements", "type": "list", "items": summary_data.get("decisions", [])},
                    {"title": "Errors", "type": "list", "items": summary_data.get("errors", [])},
                    {"title": "Configurations", "type": "list", "items": summary_data.get("configurations", [])},
                ],
                "metadata": {
                    "processed_at": datetime.now().isoformat(),
                    "trigger_immediate": immediate,
                    "content_length": len(content)
                }
            }
            
            # Save individual session log
            self._save_session_log(log_data)
            
            # Update context summary
            self._update_context_summary(log_data)
            
            # Update chat index
            self._update_chat_index(log_data)
            
            logging.info(f"Processed {ai_source} content - Session: {session_id}")
            
        except Exception as e:
            logging.error(f"Error processing content from {ai_source}: {e}")
    
    def _filter_relevant_content(self, content: str) -> str:
        """Filter content to extract only relevant parts."""
        keywords = self.config.get('keywords', {}).get('filter_keywords', [])
        error_patterns = self.config.get('keywords', {}).get('error_patterns', [])
        
        relevant_lines = []
        lines = content.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            
            # Check keywords
            if any(keyword.lower() in line_lower for keyword in keywords):
                relevant_lines.append(line)
                continue
            
            # Check error patterns
            if any(re.search(pattern, line, re.IGNORECASE) for pattern in error_patterns):
                relevant_lines.append(line)
                continue
            
            # Include lines with substantial content (not just timestamps or system messages)
            if len(line.strip()) > 20 and not line.startswith('[') and not line.startswith('INFO'):
                relevant_lines.append(line)
        
        return '\n'.join(relevant_lines)
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content."""
        keywords = self.config.get('keywords', {}).get('filter_keywords', [])
        found_keywords = []
        
        content_lower = content.lower()
        for keyword in keywords:
            if keyword.lower() in content_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _get_current_stage(self) -> str:
        """Get current project stage."""
        # Try to read from stage file
        try:
            stage_file = os.path.join(self.path_manager.get_project_root(), 'stages', 'current_stage')
            if os.path.exists(stage_file):
                with open(stage_file, 'r') as f:
                    return f.read().strip()
        except:
            pass
        
        return "stage_00_refactor"  # Default stage
    
    def _store_content(self, content: str, ai_source: str):
        """Store content for later consolidation."""
        date_key = datetime.now().strftime("%Y-%m-%d")
        
        if date_key not in self.session_data:
            self.session_data[date_key] = {}
        
        if ai_source not in self.session_data[date_key]:
            self.session_data[date_key][ai_source] = []
        
        self.session_data[date_key][ai_source].append({
            "timestamp": datetime.now().isoformat(),
            "content": content
        })
    
    def _save_session_log(self, log_data: Dict):
        """Save individual session log."""
        chats_dir = self.path_manager.get_chats_dir()
        filename = f"chat_log_{log_data['id']}.json"
        filepath = os.path.join(chats_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
    
    def _update_context_summary(self, log_data: Dict):
        """Update the context summary file."""
        context_file = self.path_manager.get_context_summary_path()
        
        # Load existing summary
        summaries = []
        if os.path.exists(context_file):
            try:
                with open(context_file, 'r', encoding='utf-8') as f:
                    summaries = json.load(f)
            except:
                summaries = []
        
        # Add new summary
        summary_entry = {
            "session_id": log_data['id'],
            "timestamp": log_data['timestamp'],
            "stage": log_data['stage'],
            "ai_source": log_data['ai_source'],
            "summary": log_data['summary'],
            "keywords": log_data['keywords']
        }
        
        summaries.append(summary_entry)
        
        # Keep only recent summaries (last 50)
        summaries = summaries[-50:]
        
        # Save updated summary
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, indent=2)
    
    def _update_chat_index(self, log_data: Dict):
        """Update the chat index."""
        index_file = self.path_manager.get_chat_index_path()
        
        # Load existing index
        index = []
        if os.path.exists(index_file):
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
            except:
                index = []
        
        # Create index entry
        index_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "stage": log_data['stage'],
            "keywords": log_data['keywords'],
            "file_path": f"chat_log_{log_data['id']}.json",
            "ai_source": log_data['ai_source'],
            "executive_summary": log_data['summary'],
            "entities": {
                "decisions": [item for section in log_data['sections'] if section['title'] == 'Key Achievements' for item in section['items']],
                "errors": [item for section in log_data['sections'] if section['title'] == 'Errors' for item in section['items']],
                "configurations": [item for section in log_data['sections'] if section['title'] == 'Configurations' for item in section['items']]
            },
            "relevance_score": len(log_data['keywords']) * 0.1 + (1.0 if log_data['metadata']['trigger_immediate'] else 0.5)
        }
        
        index.append(index_entry)
        
        # Save updated index
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    
    def trigger_consolidation(self):
        """Manually trigger daily consolidation."""
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            logging.info(f"Triggering manual consolidation for {date_str}")
            
            # Process any pending session data from memory
            if date_str in self.session_data:
                for ai_source, sessions in self.session_data[date_str].items():
                    for session in sessions:
                        self._process_content(session['content'], ai_source, immediate=True)
                
                # Clear processed data
                del self.session_data[date_str]
            
            # Also process content from raw log files
            chats_dir = self.path_manager.get_chats_dir()
            for file_name in os.listdir(chats_dir):
                if file_name.endswith('_raw.log'):
                    file_path = os.path.join(chats_dir, file_name)
                    ai_source = self._get_ai_source(file_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if content.strip():
                            logging.info(f"Processing raw log content from {file_name}")
                            self._process_content(content, ai_source, immediate=True)
                    
                    except Exception as e:
                        logging.error(f"Error reading {file_path}: {e}")
            
            logging.info("Manual consolidation completed")
            
        except Exception as e:
            logging.error(f"Error during manual consolidation: {e}")


def main():
    """Main entry point for the chat monitor."""
    import argparse
    
    # Load environment variables from .env file
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Enhanced Chat Monitor')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--consolidate', action='store_true', help='Trigger manual consolidation')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    
    args = parser.parse_args()
    
    try:
        monitor = ChatMonitor(args.config)
        
        if args.consolidate:
            monitor.trigger_consolidation()
        else:
            monitor.start_monitoring()
            
    except KeyboardInterrupt:
        logging.info("Shutting down chat monitor")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()