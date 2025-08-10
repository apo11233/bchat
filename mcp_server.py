#!/usr/bin/env python3
"""
bchat MCP Server - Model Context Protocol implementation
Exposes bchat's context capabilities to Claude Code and Gemini CLI
Professional STDIO-only architecture following MCP best practices
"""

import os
import sys
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Constants following professional MCP patterns
LOG_PREFIX = "[BCHAT-MCP]"

@dataclass
class ServerInfo:
    name: str = "bchat-context"
    version: str = "2.0.0"
    protocol_version: str = "2024-11-05"

@dataclass  
class ErrorCodes:
    PARSE_ERROR: int = -32700
    INVALID_REQUEST: int = -32600
    METHOD_NOT_FOUND: int = -32601
    INVALID_PARAMS: int = -32602
    INTERNAL_ERROR: int = -32603

class MCPLogger:
    """Professional logging class following gemini-mcp-tool patterns"""
    
    @staticmethod
    def _format_message(message: str) -> str:
        return f"{LOG_PREFIX} {message}"
    
    @staticmethod
    def info(message: str, *args) -> None:
        print(MCPLogger._format_message(message), *args, file=sys.stderr)
    
    @staticmethod
    def warn(message: str, *args) -> None:
        print(f"⚠️ {MCPLogger._format_message(message)}", *args, file=sys.stderr)
    
    @staticmethod
    def error(message: str, *args) -> None:
        print(f"❌ {MCPLogger._format_message(message)}", *args, file=sys.stderr)
    
    @staticmethod
    def debug(message: str, *args) -> None:
        print(f"🐛 {MCPLogger._format_message(message)}", *args, file=sys.stderr)
    
    @staticmethod
    def tool_invocation(tool_name: str, args: Dict[str, Any]) -> None:
        MCPLogger.info(f"Tool '{tool_name}' called with args: {json.dumps(args, indent=2)}")
    
    @staticmethod
    def request_received(method: str, request_id: Any) -> None:
        MCPLogger.info(f"📨 Request: {method} (id: {request_id})")
    
    @staticmethod
    def response_sent(request_id: Any, success: bool) -> None:
        status = "✅" if success else "❌"
        MCPLogger.info(f"📤 Response: {status} (id: {request_id})")

print(f"{LOG_PREFIX} Basic imports successful", file=sys.stderr)

# Add core modules to path
script_dir = os.path.dirname(os.path.abspath(__file__))
core_path = os.path.join(script_dir, 'core', 'src')
sys.path.append(core_path)
MCPLogger.info(f"Added to path: {core_path}")

try:
    from utils.path_manager import PathManager
    MCPLogger.info("✅ PathManager imported")
except Exception as e:
    MCPLogger.error(f"Failed to import PathManager: {e}")
    
try:
    from utils.context_engine import ChatIndexSearcher, ContextExtractor
    MCPLogger.info("✅ Context engine imported")
except Exception as e:
    MCPLogger.error(f"Failed to import context engine: {e}")

class MCPServer:
    """Professional MCP Server implementation for bchat context capabilities"""
    
    def __init__(self):
        self.server_info = ServerInfo()
        self.error_codes = ErrorCodes()
        self.logger = MCPLogger()
        
        # Initialize bchat components
        try:
            self.path_manager = PathManager()
            self.path_manager.ensure_directories()
            
            # Initialize context components
            self.index_searcher = ChatIndexSearcher(self.path_manager.get_chat_index_path())
            self.context_extractor = ContextExtractor(
                self.path_manager.get_chats_dir(), 
                self.path_manager.get_project_root()
            )
            
            # Setup logging
            self._setup_logging()
            logging.info("bchat MCP Server initialized with context capabilities")
            MCPLogger.info("🚀 Server initialization complete")
            
        except Exception as e:
            MCPLogger.error(f"Failed to initialize server: {e}")
            raise
    
    def _setup_logging(self):
        """Configure structured logging"""
        logs_dir = self.path_manager.get_logs_dir()
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - MCP - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(logs_dir / 'mcp_server.log'),
                logging.StreamHandler()
            ]
        )
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle JSON-RPC request with professional error handling
        Following MCP SDK patterns from gemini-mcp-tool
        """
        request_id = request.get("id")
        method = request.get("method", "unknown")
        
        try:
            MCPLogger.request_received(method, request_id)
            
            # Validate JSON-RPC structure
            if "jsonrpc" not in request:
                return self._create_error_response(
                    self.error_codes.INVALID_REQUEST,
                    "Missing jsonrpc field",
                    request_id
                )
            
            if request.get("jsonrpc") != "2.0":
                return self._create_error_response(
                    self.error_codes.INVALID_REQUEST,
                    "Invalid jsonrpc version",
                    request_id
                )
            
            # Route method calls
            result = self._route_method(method, request.get("params", {}), request_id)
            
            if result is None:
                # Handle notifications (no response needed)
                return None
            
            # Create success response
            response = {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            }
            
            MCPLogger.response_sent(request_id, True)
            return response
            
        except Exception as e:
            MCPLogger.error(f"Error handling request: {e}")
            response = self._create_error_response(
                self.error_codes.INTERNAL_ERROR,
                f"Internal server error: {str(e)}",
                request_id
            )
            MCPLogger.response_sent(request_id, False)
            return response
    
    def _route_method(self, method: str, params: Dict[str, Any], request_id: Any) -> Optional[Dict[str, Any]]:
        """Route method calls to appropriate handlers"""
        
        if method == "initialize":
            return self._handle_initialize(params)
        
        elif method == "tools/list":
            return self._handle_tools_list()
        
        elif method == "tools/call":
            return self._handle_tools_call(params)
        
        elif method == "notifications/initialized":
            # MCP initialization notification - acknowledge silently
            MCPLogger.info("Client initialization notification received")
            return None  # No response for notifications
        
        elif method.startswith("notifications/"):
            # Handle other notifications silently
            MCPLogger.info(f"Notification received: {method}")
            return None
        
        else:
            raise Exception(f"Method not found: {method}")
    
    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request"""
        return {
            "protocolVersion": self.server_info.protocol_version,
            "capabilities": {
                "tools": {},
                "logging": {},
                "progress": True  # Support progress notifications
            },
            "serverInfo": {
                "name": self.server_info.name,
                "version": self.server_info.version
            }
        }
    
    def _handle_tools_list(self) -> Dict[str, Any]:
        """List available MCP tools with proper schema"""
        return {
            "tools": [
                {
                    "name": "echo",
                    "description": "Echo input text for testing MCP connection",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to echo back"
                            }
                        },
                        "required": ["text"]
                    }
                },
                {
                    "name": "search_context", 
                    "description": "Search bchat conversation history for relevant context",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search terms or keywords"
                            },
                            "provider": {
                                "type": "string", 
                                "description": "AI provider filter",
                                "enum": ["claude", "gemini"]
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum results to return",
                                "default": 3,
                                "minimum": 1,
                                "maximum": 10
                            }
                        },
                        "required": ["query"]
                    }
                }
            ]
        }
    
    def _handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool execution with professional error handling"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if not tool_name:
            raise Exception("Tool name is required")
        
        MCPLogger.tool_invocation(tool_name, arguments)
        
        # Route to specific tool handlers
        if tool_name == "echo":
            return self._tool_echo(arguments)
        elif tool_name == "search_context":
            return self._tool_search_context(arguments)
        else:
            raise Exception(f"Unknown tool: {tool_name}")
    
    def _tool_echo(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Echo tool implementation"""
        text = arguments.get("text", "")
        
        if not text:
            return {
                "content": [{"type": "text", "text": "Error: No text provided"}],
                "isError": True
            }
        
        return {
            "content": [{"type": "text", "text": f"Echo: {text}"}],
            "isError": False
        }
    
    def _tool_search_context(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Context search tool with enhanced error handling"""
        query = arguments.get("query", "").strip()
        provider = arguments.get("provider")
        limit = arguments.get("limit", 3)
        
        # Validate arguments
        if not query:
            return {
                "content": [{"type": "text", "text": "Error: Search query is required"}],
                "isError": True
            }
        
        try:
            # Validate limit
            limit = max(1, min(int(limit), 10))
        except (ValueError, TypeError):
            limit = 3
        
        try:
            # Perform search with enhanced logging
            index_path = self.path_manager.get_chat_index_path()
            MCPLogger.info(f"Searching: '{query}' (provider: {provider}, limit: {limit})")
            MCPLogger.debug(f"Index path: {index_path} (exists: {index_path.exists()})")
            
            # Reload index data for latest results
            self.index_searcher = ChatIndexSearcher(index_path)
            
            # Execute search
            keywords = query.split()
            results = self.index_searcher.search(keywords, provider, limit)
            
            MCPLogger.info(f"Search results: {len(results)} found")
            
            if not results:
                # Provide helpful debug information
                debug_info = self._get_search_debug_info()
                return {
                    "content": [
                        {"type": "text", "text": f"No relevant context found for: {query}"},
                        {"type": "text", "text": debug_info}
                    ],
                    "isError": False
                }
            
            # Extract detailed context
            file_paths = [result['file_path'] for result in results]
            context = self.context_extractor.extract_chat_logs(file_paths)
            
            return {
                "content": [
                    {"type": "text", "text": f"Found {len(results)} relevant conversations:"},
                    {"type": "text", "text": context}
                ],
                "isError": False
            }
            
        except Exception as e:
            MCPLogger.error(f"Search failed: {e}")
            return {
                "content": [{"type": "text", "text": f"Search error: {str(e)}"}],
                "isError": True
            }
    
    def _get_search_debug_info(self) -> str:
        """Get helpful debug information for empty search results"""
        try:
            if hasattr(self.index_searcher, 'index_data') and self.index_searcher.index_data:
                available_keywords = set()
                for entry in self.index_searcher.index_data:
                    available_keywords.update(entry.get('keywords', []))
                
                if available_keywords:
                    keyword_sample = list(available_keywords)[:10]
                    return f"Available topics: {', '.join(keyword_sample)}{'...' if len(available_keywords) > 10 else ''}"
            
            return "No indexed conversations available. Try running bchat first to generate context."
            
        except Exception:
            return "Debug information unavailable"
    
    def _create_error_response(self, code: int, message: str, request_id: Any) -> Dict[str, Any]:
        """Create standardized JSON-RPC error response"""
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message
            },
            "id": request_id
        }

def main():
    """Main STDIO mode entry point with professional error handling"""
    MCPLogger.info("🔧 bchat MCP Server starting in STDIO mode")
    MCPLogger.info("   Protocol: JSON-RPC 2.0 via stdin/stdout")
    MCPLogger.info("   Architecture: Professional STDIO-only")
    
    try:
        server = MCPServer()
        MCPLogger.info("✅ Server initialized successfully")
    except Exception as e:
        MCPLogger.error(f"Server initialization failed: {e}")
        return 1
    
    try:
        MCPLogger.info("🔄 Waiting for JSON-RPC requests...")
        
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    MCPLogger.info("📝 Input stream closed, shutting down")
                    break
                    
                line = line.strip()
                if not line:
                    continue
                
                # Parse and handle request
                try:
                    request = json.loads(line)
                    response = server.handle_request(request)
                    
                    # Send response (if not a notification)
                    if response is not None:
                        response_str = json.dumps(response)
                        print(response_str, flush=True)
                        
                except json.JSONDecodeError as e:
                    MCPLogger.error(f"JSON parse error: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": server.error_codes.PARSE_ERROR,
                            "message": f"Parse error: {str(e)}"
                        },
                        "id": None
                    }
                    print(json.dumps(error_response), flush=True)
                    
            except EOFError:
                MCPLogger.info("📝 EOF reached, shutting down")
                break
            except KeyboardInterrupt:
                MCPLogger.info("🛑 Keyboard interrupt, shutting down")
                break
            except Exception as e:
                MCPLogger.error(f"Unexpected error in main loop: {e}")
                # Continue running despite errors
                continue
                
    except Exception as e:
        MCPLogger.error(f"Fatal error: {e}")
        return 1
    
    MCPLogger.info("👋 bchat MCP Server shutdown complete")
    return 0

if __name__ == "__main__":
    MCPLogger.info("🔄 bchat MCP Server starting (Professional STDIO-only)...")
    exit_code = main()
    sys.exit(exit_code)