#!/usr/bin/env python3
"""
Auto-detection and configuration module for bchat
Detects available AI CLI tools and suggests optimal configuration
"""

import os
import subprocess
import json
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

class AIToolDetector:
    """Detects available AI CLI tools and suggests configuration"""
    
    def __init__(self):
        self.detected_tools = {}
        self.available_apis = {}
    
    def detect_cli_tools(self) -> Dict[str, Dict]:
        """Detect installed AI CLI tools"""
        tools = {}
        
        # Check Claude Code CLI
        if self._check_command_exists('claude'):
            version = self._get_command_output(['claude', '--version'])
            tools['claude'] = {
                'installed': True,
                'version': version,
                'path': self._get_command_path('claude')
            }
        
        # Check Gemini CLI  
        if self._check_command_exists('gemini'):
            version = self._get_command_output(['gemini', '--version'])
            tools['gemini'] = {
                'installed': True,
                'version': version,
                'path': self._get_command_path('gemini')
            }
        
        self.detected_tools = tools
        return tools
    
    def detect_api_keys(self) -> Dict[str, bool]:
        """Detect available API keys in environment"""
        # Load environment variables from .env file
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
        load_dotenv(dotenv_path=dotenv_path)

        apis = {}
        
        # Check for API keys
        apis['anthropic'] = bool(os.getenv('ANTHROPIC_API_KEY'))
        apis['google'] = bool(os.getenv('GOOGLE_API_KEY'))
        
        self.available_apis = apis
        return apis
    
    def detect_active_sessions(self) -> Dict[str, List]:
        """Detect currently running AI CLI sessions"""
        sessions = {'claude': [], 'gemini': []}
        
        try:
            # Get all processes
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            lines = result.stdout.split('\\n')
            
            for line in lines:
                if 'claude' in line.lower() and 'grep' not in line:
                    sessions['claude'].append(line.strip())
                elif 'gemini' in line.lower() and 'grep' not in line:
                    sessions['gemini'].append(line.strip())
                    
        except Exception as e:
            print(f"Warning: Could not detect active sessions: {e}")
        
        return sessions
    
    def find_existing_logs(self) -> Dict[str, List]:
        """Find existing AI chat logs in common locations"""
        log_locations = {}
        
        # Common log patterns to search for
        patterns = [
            ('claude', '*claude*log*'),
            ('gemini', '*gemini*log*')
        ]
        
        for tool, pattern in patterns:
            log_locations[tool] = []
            
            # Search in home directory and common locations
            search_paths = [
                os.path.expanduser('~/Documents'),
                os.path.expanduser('~/Library/Application Support'),
                os.getcwd()
            ]
            
            for search_path in search_paths:
                try:
                    result = subprocess.run([
                        'find', search_path, '-name', pattern, '-type', 'f'
                    ], capture_output=True, text=True, timeout=5)
                    
                    if result.returncode == 0:
                        files = [f.strip() for f in result.stdout.split('\\n') if f.strip()]
                        log_locations[tool].extend(files)
                        
                except Exception:
                    continue  # Skip inaccessible directories
        
        return log_locations
    
    def suggest_configuration(self) -> Dict:
        """Suggest optimal configuration based on detection results"""
        tools = self.detect_cli_tools()
        apis = self.detect_api_keys()
        sessions = self.detect_active_sessions()
        logs = self.find_existing_logs()
        
        config = {
            'detection_results': {
                'tools_installed': tools,
                'api_keys_available': apis,
                'active_sessions': sessions,
                'existing_logs': logs
            },
            'recommended_config': {},
            'confidence': 'low'
        }
        
        # Determine recommended provider
        if apis.get('anthropic') and tools.get('claude'):
            config['recommended_config']['provider'] = 'claude'
            config['confidence'] = 'high'
        elif apis.get('google') and tools.get('gemini'):
            config['recommended_config']['provider'] = 'gemini'
            config['confidence'] = 'medium'
        elif apis.get('anthropic'):
            config['recommended_config']['provider'] = 'claude'
            config['confidence'] = 'medium'
        elif apis.get('google'):
            config['recommended_config']['provider'] = 'gemini'
            config['confidence'] = 'medium'
        else:
            config['recommended_config']['provider'] = 'claude'  # Default
            config['confidence'] = 'low'
            config['warning'] = 'No API keys detected. Please configure .env file.'
        
        return config
    
    def auto_configure(self, config_path: str = 'config/config.json') -> bool:
        """Automatically update configuration based on detection"""
        try:
            suggestion = self.suggest_configuration()
            
            # Only auto-configure if confidence is medium or high
            if suggestion['confidence'] in ['medium', 'high']:
                # Load existing config
                with open(config_path, 'r') as f:
                    current_config = json.load(f)
                
                # Update provider
                current_config['api']['provider'] = suggestion['recommended_config']['provider']
                
                # Save updated config
                with open(config_path, 'w') as f:
                    json.dump(current_config, f, indent=2)
                
                print(f"✅ Auto-configured provider to: {suggestion['recommended_config']['provider']}")
                return True
            else:
                print("⚠️  Auto-configuration skipped (low confidence)")
                return False
                
        except Exception as e:
            print(f"❌ Auto-configuration failed: {e}")
            return False
    
    def _check_command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        try:
            subprocess.run(['which', command], 
                         capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _get_command_output(self, command: List[str]) -> Optional[str]:
        """Get output from a command safely"""
        try:
            result = subprocess.run(command, 
                                  capture_output=True, text=True, 
                                  timeout=5)
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return None
    
    def _get_command_path(self, command: str) -> Optional[str]:
        """Get full path of a command"""
        try:
            result = subprocess.run(['which', command], 
                                  capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return None


def main():
    """CLI interface for auto-detection"""
    detector = AIToolDetector()
    config = detector.suggest_configuration()
    
    print("🔍 bchat Auto-Configuration Results")
    print("=" * 40)
    
    # Show detection results
    tools = config['detection_results']['tools_installed']
    apis = config['detection_results']['api_keys_available']
    
    print("\\n📱 Installed CLI Tools:")
    for tool, info in tools.items():
        print(f"  ✅ {tool.title()}: {info['version']} ({info['path']})")
    
    if not tools:
        print("  ❌ No AI CLI tools detected")
    
    print("\\n🔑 API Keys:")
    for api, available in apis.items():
        status = "✅ Available" if available else "❌ Not found"
        print(f"  {api.title()}: {status}")
    
    print("\\n🎯 Recommended Configuration:")
    print(f"  Provider: {config['recommended_config']['provider']}")
    print(f"  Confidence: {config['confidence']}")
    
    if 'warning' in config:
        print(f"\\n⚠️  {config['warning']}")
    
    return config


if __name__ == '__main__':
    main()