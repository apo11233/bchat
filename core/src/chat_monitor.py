#!/usr/bin/env python3
"""
bchat: Context-Aware AI Chat Processor
"""

import os
import sys
import json
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import re

# Third-party imports
from dotenv import load_dotenv
import google.generativeai as genai

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.path_manager import PathManager
from utils.context_engine import ContextualQueryAnalyzer, ChatIndexSearcher, ContextExtractor, ClaudeMdParser

class APIManager:
    """Manages API calls with error handling and retries."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api_config = config.get('api', {})
        self.provider = self.api_config.get('provider', 'gemini').lower()
        self._initialize_apis()

    def _initialize_apis(self):
        """Initializes the appropriate AI provider."""
        if self.provider == 'gemini':
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is required for Gemini")
            genai.configure(api_key=api_key)
            model_name = self.api_config.get('gemini', {}).get('model', 'gemini-1.5-flash')
            self.model = genai.GenerativeModel(model_name=model_name)
        elif self.provider == 'claude':
            # Claude initialization would go here
            pass

    def call_api(self, prompt: str) -> Dict:
        """Makes an API call to the configured provider."""
        try:
            if self.provider == 'gemini':
                generation_config = {
                    "response_mime_type": "application/json",
                    "max_output_tokens": self.api_config.get('max_tokens', 4096),
                    "temperature": self.api_config.get('temperature', 0.3)
                }
                response = self.model.generate_content(prompt, generation_config=generation_config)
                return self._parse_response(response.text)
            elif self.provider == 'claude':
                # Claude API call logic would go here
                return {}
        except Exception as e:
            logging.error(f"API call failed: {e}", exc_info=True)
            return {"error": str(e)}

    def _parse_response(self, raw_text: str) -> Dict:
        """Parses the JSON response from the AI."""
        try:
            match = re.search(r'```json\s*(\{.*?\})\s*```', raw_text, re.DOTALL)
            if match:
                json_str = match.group(1)
                return json.loads(json_str)
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse API response as JSON. Raw text was: {raw_text}. Error: {e}")
            return {"error": "Failed to parse JSON response"}

class ChatProcessor:
    """Main chat processing system with context-aware capabilities."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.path_manager = PathManager(config_path)
        self.config = self.path_manager.config
        self._setup_logging()
        self.api_manager = APIManager(self.config)
        
        self.query_analyzer = ContextualQueryAnalyzer()
        self.index_searcher = ChatIndexSearcher(self.path_manager.get_chat_index_path())
        self.context_extractor = ContextExtractor(self.path_manager.get_chats_dir(), self.path_manager.get_project_root())

        self.path_manager.ensure_directories()
        logging.info("ChatProcessor initialized with Deep Context Engine")

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

    def process_prompt(self, prompt: str, provider: str):
        """Processes a user prompt, applying context awareness if necessary."""
        try:
            logging.info(f"Processing prompt for {provider}: '{prompt}'")
            analysis = self.query_analyzer.analyze(prompt)
            final_prompt = prompt

            if analysis["is_contextual"]:
                logging.info("Contextual query detected. Searching for relevant history...")
                
                bchat_context = self.context_extractor.extract_chat_logs(
                    [log['file_path'] for log in self.index_searcher.search(analysis["search_keywords"], analysis["provider_filter"])]
                )
                
                advanced_context = self.context_extractor.extract_advanced_context(analysis.get("provider_filter", provider))

                claude_md_context = self.context_extractor.claude_md_parser.parse_hierarchy(self.path_manager.get_project_root())

                full_context = f"{bchat_context}\n{advanced_context}\n{claude_md_context}".strip()

                if full_context:
                    logging.info("Context found. Injecting into prompt...")
                    final_prompt = f"""Based on the following context from our previous conversations:\n\n{full_context}\n\nPlease answer the user's question: "{prompt}"""
                else:
                    logging.info("No relevant context found.")

            summarization_prompt = self._create_summarization_prompt(final_prompt, provider)
            summary_data = self.api_manager.call_api(summarization_prompt)
            self._save_new_chat(prompt, final_prompt, summary_data, provider)
            
            # Provide user feedback
            context_status = "✓ Context injected" if analysis["is_contextual"] else "○ No context needed"
            print(f"✅ bchat processed successfully")
            print(f"   Provider: {provider.title()}")
            print(f"   Context: {context_status}")
            if summary_data and "error" not in summary_data:
                print(f"   Summary: {summary_data.get('summary', 'Processing complete')}")
            else:
                print(f"   Status: Logged to chat history")

        except Exception as e:
            logging.error(f"Error processing prompt: {e}", exc_info=True)

    def consolidate_existing_data(self):
        """Consolidate existing chat data and update indices."""
        try:
            logging.info("Starting data consolidation...")
            
            # Process any existing raw log files
            chats_dir = self.path_manager.get_chats_dir()
            raw_files = list(chats_dir.glob("*_raw.log"))
            
            if raw_files:
                logging.info(f"Found {len(raw_files)} raw log files to process")
                for raw_file in raw_files:
                    self._process_raw_log_file(raw_file)
            else:
                logging.info("No raw log files found")
            
            # Update context summary
            self._update_context_summary()
            
            logging.info("Data consolidation completed successfully")
            print("✅ bchat consolidation complete")
            print(f"   Raw files processed: {len(raw_files)}")
            print("   Chat history indexed and ready for context queries")
            
        except Exception as e:
            logging.error(f"Error during consolidation: {e}", exc_info=True)
            print(f"❌ Consolidation failed: {e}")

    def _process_raw_log_file(self, raw_file: Path):
        """Process a single raw log file."""
        try:
            provider = "gemini" if "gemini" in raw_file.name else "claude"
            
            with open(raw_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if content:
                # Create a consolidation prompt for the raw content
                consolidation_prompt = f"Consolidated chat history from {raw_file.name}"
                summarization_prompt = self._create_summarization_prompt(content, provider)
                summary_data = self.api_manager.call_api(summarization_prompt)
                
                if summary_data and "error" not in summary_data:
                    self._save_new_chat(consolidation_prompt, content, summary_data, provider)
                    logging.info(f"Successfully processed {raw_file.name}")
                else:
                    logging.warning(f"Failed to process {raw_file.name}: API error")
            
        except Exception as e:
            logging.warning(f"Could not process raw file {raw_file}: {e}")

    def _update_context_summary(self):
        """Update the global context summary file."""
        try:
            index_file = self.path_manager.get_chat_index_path()
            summary_file = self.path_manager.get_chats_dir() / "context_summary.json"
            
            if not index_file.exists():
                return
                
            with open(index_file, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            # Generate high-level summary
            total_sessions = len(index_data)
            recent_sessions = [entry for entry in index_data if entry.get('date') >= (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")]
            all_keywords = []
            all_decisions = []
            
            for entry in index_data:
                all_keywords.extend(entry.get('keywords', []))
                if 'entities' in entry:
                    all_decisions.extend(entry['entities'].get('decisions', []))
            
            context_summary = {
                "last_updated": datetime.now().isoformat(),
                "total_sessions": total_sessions,
                "recent_sessions_count": len(recent_sessions),
                "top_keywords": list(set(all_keywords))[:20],
                "key_decisions": list(set(all_decisions))[:10],
                "summary": f"Processed {total_sessions} chat sessions with {len(recent_sessions)} recent sessions in the last week"
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(context_summary, f, indent=2)
                
            logging.info("Context summary updated successfully")
            
        except Exception as e:
            logging.warning(f"Could not update context summary: {e}")

    def _create_summarization_prompt(self, content: str, ai_source: str) -> str:
        """Create a prompt for content summarization."""
        return f"""
    Analyze the following chat content. Your task is to generate a structured JSON summary.

    **IMPORTANT**: Your response MUST be a single, valid JSON object and nothing else. Do not include any conversational text, greetings, or explanations before or after the JSON. The entire response should be only the JSON object, enclosed in triple backticks (```json ... ```).

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
    """

    def _save_new_chat(self, original_prompt: str, final_prompt: str, summary_data: Dict, ai_source: str):
        """Saves the new chat session to the logs and index."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = f"{ai_source.lower()}_{timestamp}"
            
            log_data = {
                "id": session_id,
                "timestamp": datetime.now().isoformat(),
                "stage": "stage_03_context_awareness",
                "ai_source": ai_source,
                "session_id": session_id,
                "original_prompt": original_prompt,
                "final_prompt": final_prompt,
                "content_hash": hashlib.md5(final_prompt.encode()).hexdigest(),
                "keywords": summary_data.get("key_topics", []),
                "summary": summary_data.get("summary", "No summary available"),
                "sections": [
                    {"title": "Key Achievements", "type": "list", "items": summary_data.get("decisions", [])},
                    {"title": "Errors", "type": "list", "items": summary_data.get("errors", [])},
                    {"title": "Configurations", "type": "list", "items": summary_data.get("configurations", [])},
                ],
                "metadata": {
                    "processed_at": datetime.now().isoformat(),
                    "content_length": len(final_prompt)
                }
            }
            
            self._save_session_log(log_data)
            self._update_chat_index(log_data)
            logging.info(f"Successfully processed and saved new chat - Session: {session_id}")

        except Exception as e:
            logging.error(f"Error saving new chat from {ai_source}: {e}", exc_info=True)

    def _save_session_log(self, log_data: Dict):
        """Save individual session log."""
        chats_dir = self.path_manager.get_chats_dir()
        filename = f"chat_log_{log_data['id']}.json"
        filepath = chats_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)

    def _update_chat_index(self, log_data: Dict):
        """Update the chat index."""
        index_file = self.path_manager.get_chat_index_path()
        index = []
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
            except json.JSONDecodeError:
                index = []
        
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
            "relevance_score": len(log_data['keywords']) * 0.1 + 1.0
        }
        index.append(index_entry)
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)

def main():
    """Main entry point for the chat processor."""
    import argparse
    
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='bchat: AI Chat Processor with Context-Awareness')
    parser.add_argument('prompt', nargs='?', help='The user prompt to process. If not provided, triggers consolidation.')
    parser.add_argument('--provider', default='gemini', choices=['gemini', 'claude'], help='The AI provider to use.')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--consolidate', action='store_true', help='Trigger manual consolidation of existing chat data')
    
    args = parser.parse_args()
    
    try:
        processor = ChatProcessor(args.config)
        
        if args.consolidate or not args.prompt:
            # Trigger consolidation when --consolidate flag is used or no prompt provided
            processor.consolidate_existing_data()
        else:
            # Process the user prompt
            processor.process_prompt(args.prompt, args.provider)
    except Exception as e:
        logging.error(f"A fatal error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()