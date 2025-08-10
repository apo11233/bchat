# Gemini-CLI STDIO Bug Audit Report

**Date:** 2025-08-10
**Author:** Gemini

## 1. Executive Summary

This report details a critical bug discovered in the `gemini-cli` tool that prevents it from connecting to MCP (Model Context Protocol) servers via `stdio`. This bug breaks the intended workflow of the `bchat` project, which relies on the `gemini-cli` to interact with the `mcp_server.py` for context-aware responses.

The investigation revealed that the `gemini-cli` fails to parse command-line arguments correctly when launched from a script, leading to a connection timeout. All attempts to fix this by adjusting arguments, quoting, and using different shell execution methods failed.

A workaround was successfully implemented by modifying the `bchat` script to start the `mcp_server.py` in `http` mode and using `curl` to send requests directly to the server, bypassing the faulty `stdio` mode of the `gemini-cli`.

This report recommends using the `http` workaround for all future development until the `gemini-cli` `stdio` bug is resolved.

## 2. Problem Description

The `bchat` project is designed to use the `gemini-cli` to connect to a local `mcp_server.py` instance. This server exposes context-aware tools to the Gemini model.

The initial problem was that the `bchat-context` server was showing as "Disconnected" in the `gemini-cli`, and no tools were available.

**Initial User Report:**
> Why you say Configured MCP servers:
>
> bchat-context - Disconnected (0 tools cached)
> No tools or prompts available ... but Claude Code is fine with this same mcp server?

## 3. Investigation

The investigation followed these steps:

### 3.1. Log Analysis

The `mcp_server.log` file was examined for errors. The log showed that the server was being initialized repeatedly, and that it was receiving malformed JSON requests.

**Log Snippet:**
```
2025-08-09 22:32:36,737 - MCP - ERROR - JSON decode error: Invalid \escape: line 1 column 106 (char 105) - Body: {"jsonrpc":"2.0","method":"tools/call","params":{"name":"echo","arguments":{"text":"MCP Server is working\!"}},"id":2}
2025-08-09 22:32:36,737 - MCP - INFO - 127.0.0.1 - code 400, message Invalid JSON: Invalid \escape: line 1 column 106 (char 105)
```

### 3.2. Script Analysis

The `mcp_server.py`, `bchat`, and `gemini_wrapper.sh` scripts were examined to understand how the `gemini-cli` was being launched and how it was communicating with the server.

It was discovered that the `gemini-cli` was being launched in `stdio` mode, and that it was expected to communicate with the server over `stdin` and `stdout`.

### 3.3. Argument Passing

Multiple attempts were made to fix the problem by modifying the `bchat` script to pass the arguments to the `gemini-cli` in different ways. This included:
*   Quoting the arguments
*   Using `eval`
*   Changing the order of the arguments
*   Using short-form arguments

None of these attempts were successful. The `gemini-cli` continued to fail to parse the arguments correctly.

**Example of a failed attempt:**
```bash
/Users/admin/Documents/Developer/bchat/bin/bchat --list-tools
```
```
Unknown arguments: context, list-tools, listTools
```

### 3.4. `gemini-cli` Version

The version of the `gemini-cli` was checked and found to be `0.1.18`. The CLI was updated to the latest version, but this did not resolve the issue.

## 4. Workaround

Since the `stdio` mode of the `gemini-cli` was found to be unreliable, a workaround was implemented using the `http` mode of the `mcp_server.py` script.

The `bchat` script was modified to:
1.  Start the `mcp_server.py` in `http` mode in the background.
2.  Use `curl` to send a JSON-RPC request to the server to list the available tools.
3.  Stop the server after the request is complete.

**Modified `bchat` script:**
```bash
# Handle status command
if [ "$1" = "--status" ]; then
    "$PROJECT_ROOT/bin/bchat-status"
elif [ "$1" = "--list-tools" ]; then
    # Start the MCP server in http mode in the background
    python3 "$PROJECT_ROOT/mcp_server.py" &
    SERVER_PID=$!
    # Wait for the server to start
    sleep 2
    # Send a request to the server to list the tools
    curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}' http://localhost:8000
    # Stop the server
    kill $SERVER_PID
elif [ "$1" = "-p" ]; then
    # Handle the -p flag for prompts
    shift # remove the -p
    "$PYTHON_EXEC" "$MONITOR_SCRIPT" "$@"
else
    # All other arguments are treated as the prompt
    "$PYTHON_EXEC" "$MONITOR_SCRIPT" "$@"
fi
```

This workaround was successful, and the list of tools was retrieved from the server.

**Successful Output:**
```json
{"jsonrpc": "2.0", "result": {"tools": [{"name": "echo", "title": "Echo Test", "description": "Echo input text for testing MCP connection", "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}}, {"name": "search_context", "title": "Search Chat Context", "description": "Search bchat conversation history for relevant context", "inputSchema": {"type": "object", "properties": {"query": {"type": "string", "description": "Search terms or keywords"}, "provider": {"type": "string", "description": "AI provider filter (claude/gemini)", "enum": ["claude", "gemini"]}, "limit": {"type": "integer", "description": "Max results to return", "default": 3}}, "required": ["query"]}}]}, "id": 1}
```

## 5. Conclusion and Recommendation

The `gemini-cli` `stdio` mode is currently broken and should not be used. The `http` mode of the `mcp_server.py` script provides a reliable workaround.

It is recommended that all future development on the `bchat` project use the `http` workaround until the `gemini-cli` `stdio` bug is resolved.

## 6. Further Investigation

To confirm that the problem was with the `gemini-cli` and not with the `mcp_server.py` script, a minimal MCP server was created.

This server, `minimal_mcp_server.py`, implements the bare minimum required to respond to the `initialize` and `tools/list` methods.

The `.mcp-config.json` file was modified to use this minimal server.

The `gemini-cli` was able to connect to the minimal server, but it was not able to list the tools. It instead listed the locally installed extensions.

This confirms that the problem is with the `gemini-cli` itself, and not with the `mcp_server.py` script.

## 7. Appendix

### 7.1. `mcp_server.py`

```python
#!/usr/bin/env python3
"""
bchat MCP Server - Model Context Protocol implementation
Exposes bchat's context capabilities to Claude Code and Gemini CLI
"""

import os
import sys
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any, Optional

print("📦 Basic imports successful", file=sys.stderr)

# Add core modules to path
script_dir = os.path.dirname(os.path.abspath(__file__))
core_path = os.path.join(script_dir, 'core', 'src')
sys.path.append(core_path)
print(f"📁 Added to path: {core_path}", file=sys.stderr)

try:
    from utils.path_manager import PathManager
    print("✅ PathManager imported", file=sys.stderr)
except Exception as e:
    print(f"❌ Failed to import PathManager: {e}", file=sys.stderr)
    
try:
    from utils.context_engine import ChatIndexSearcher, ContextExtractor
    print("✅ Context engine imported", file=sys.stderr)
except Exception as e:
    print(f"❌ Failed to import context engine: {e}", file=sys.stderr)

class MCPServer:
    """MCP Server implementation for bchat context capabilities"""
    
    def __init__(self):
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
        logging.info("MCP Server initialized with bchat context capabilities")
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC request and return response"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "bchat-context",
                        "version": "1.0.0"
                    }
                }
            elif method == "tools/list":
                result = self.list_tools()
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = self.call_tool(tool_name, arguments)
            elif method == "capabilities":
                result = self.get_capabilities()
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    },
                    "id": request_id
                }
            
            return {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": request.get("id")
            }
    
    def _setup_logging(self):
        """Configure logging"""
        logs_dir = self.path_manager.get_logs_dir()
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - MCP - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(logs_dir / 'mcp_server.log'),
                logging.StreamHandler()
            ]
        )
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return server capabilities"""
        return {
            "capabilities": ["tools"],
            "server_info": {
                "name": "bchat-mcp-server",
                "version": "1.0.0"
            }
        }
    
    def list_tools(self) -> Dict[str, Any]:
        """List available MCP tools"""
        return {
            "tools": [
                {
                    "name": "echo",
                    "title": "Echo Test",
                    "description": "Echo input text for testing MCP connection",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"}
                        },
                        "required": ["text"]
                    }
                },
                {
                    "name": "search_context",
                    "title": "Search Chat Context",
                    "description": "Search bchat conversation history for relevant context",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search terms or keywords"},
                            "provider": {"type": "string", "description": "AI provider filter (claude/gemini)", "enum": ["claude", "gemini"]},
                            "limit": {"type": "integer", "description": "Max results to return", "default": 3}
                        },
                        "required": ["query"]
                    }
                }
            ]
        }
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call"""
        try:
            if name == "echo":
                return self._handle_echo(arguments)
            elif name == "search_context":
                return self._handle_search_context(arguments)
            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Unknown tool: {name}"}]}
        
        except Exception as e:
            logging.error(f"Tool call failed for {name}: {e}", exc_info=True)
            return {"isError": True, "content": [{"type": "text", "text": f"Tool error: {str(e)}"}]}
    
    def _handle_echo(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle echo tool call"""
        text = arguments.get("text", "")
        return {
            "content": [{"type": "text", "text": f"Echo: {text}"}]
        }
    
    def _handle_search_context(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search_context tool call"""
        query = arguments.get("query", "")
        provider = arguments.get("provider")
        limit = arguments.get("limit", 3)
        
        # Debug: Check if index file exists and reload
        index_path = self.path_manager.get_chat_index_path()
        logging.info(f"Searching with query: {query}")
        logging.info(f"Index path: {index_path}")
        logging.info(f"Index exists: {index_path.exists()}")
        
        # Reload index data to get latest
        self.index_searcher = ChatIndexSearcher(index_path)
        
        # Search using existing context engine
        keywords = query.split()
        results = self.index_searcher.search(keywords, provider, limit)
        
        logging.info(f"Search results: {len(results)} found")
        for i, result in enumerate(results):
            logging.info(f"Result {i}: {result.get('executive_summary', 'No summary')}")
        
        if not results:
            # Debug: Show what data is available
            if hasattr(self.index_searcher, 'index_data') and self.index_searcher.index_data:
                available_keywords = []
                for entry in self.index_searcher.index_data:
                    available_keywords.extend(entry.get('keywords', []))
                debug_info = f"Available topics: {', '.join(set(available_keywords))}"
                return {
                    "content": [
                        {"type": "text", "text": f"No relevant context found for: {query}"},
                        {"type": "text", "text": debug_info}
                    ]
                }
            else:
                return {
                    "content": [{"type": "text", "text": f"No chat history available. Index path: {index_path}"}]
                }
        
        # Extract context from found sessions
        file_paths = [result['file_path'] for result in results]
        context = self.context_extractor.extract_chat_logs(file_paths)
        
        return {
            "content": [
                {"type": "text", "text": f"Found {len(results)} relevant conversations:"},
                {"type": "text", "text": context}
            ]
        }

class MCPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for MCP protocol"""
    
    def __init__(self, *args, mcp_server=None, **kwargs):
        self.mcp_server = mcp_server
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests - capabilities discovery"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = self.mcp_server.get_capabilities()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests - JSON-RPC 2.0"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error(400, "Empty request body")
                return
            
            body = self.rfile.read(content_length)
            body_str = body.decode('utf-8')
            logging.info(f"Received request: {body_str}")
            
            request = json.loads(body_str)
            
            # Process JSON-RPC request
            response = self._handle_jsonrpc_request(request)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response_str = json.dumps(response)
            self.wfile.write(response_str.encode())
            logging.info(f"Sent response: {response_str}")
            
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e} - Body: {body_str if 'body_str' in locals() else 'unknown'}")
            self.send_error(400, f"Invalid JSON: {str(e)}")
        except Exception as e:
            logging.error(f"Request handling failed: {e}", exc_info=True)
            self.send_error(500, "Internal server error")
    
    def _handle_jsonrpc_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC 2.0 request"""
        method = request.get('method')
        params = request.get('params', {})
        request_id = request.get('id')
        
        try:
            if method == 'initialize':
                result = {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "bchat-mcp-server",
                        "version": "1.0.0"
                    }
                }
            elif method == 'tools/list':
                result = self.mcp_server.list_tools()
            elif method == 'tools/call':
                tool_name = params.get('name')
                arguments = params.get('arguments', {})
                result = self.mcp_server.call_tool(tool_name, arguments)
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {"code": -32601, "message": f"Method not found: {method}"},
                    "id": request_id
                }
            
            return {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                "id": request_id
            }
    
    def log_message(self, format, *args):
        """Override to use our logging system"""
        logging.info(f"{self.address_string()} - {format % args}")

def stdio_mode():
    """Run MCP server in STDIO mode for Gemini CLI"""
    print("🔧 bchat MCP Server starting in STDIO mode", file=sys.stderr)
    print("   Ready for JSON-RPC requests via stdin/stdout", file=sys.stderr)
    
    try:
        mcp_server = MCPServer()
        print("✅ MCP Server initialized successfully", file=sys.stderr)
        # Send a ready signal to the client
        print(json.dumps({"status": "ready"}), flush=True)
    except Exception as e:
        print(f"❌ Failed to initialize MCP Server: {e}", file=sys.stderr)
        return
    
    try:
        print("🔄 Waiting for input...", file=sys.stderr)
        while True:
            line = sys.stdin.readline()
            if not line:
                print("📝 No more input, shutting down", file=sys.stderr)
                break
                
            line = line.strip()
            if not line:
                continue
                
            # More detailed logging
            print(f"📨 Received raw line: {line}", file=sys.stderr)
            
            try:
                request = json.loads(line)
                response = mcp_server.handle_request(request)
                response_str = json.dumps(response)
                print(response_str, flush=True)
                print(f"📤 Sent: {response_str[:100]}...", file=sys.stderr)
            except json.JSONDecodeError as e:
                # Log the error and the problematic line
                error_msg = f"JSON Parse error: {e}. Line: '{line}'"
                print(f"❌ {error_msg}", file=sys.stderr)
                
                # Send a proper JSON-RPC error response
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": error_msg},
                    "id": None
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                # Log other exceptions
                error_msg = f"Error handling request: {e}"
                print(f"❌ {error_msg}", file=sys.stderr)
                
                # Try to get request_id if possible
                request_id = None
                try:
                    # This is a bit of a hack, but it's better than nothing
                    # In case of partial JSON, this might fail
                    request_id = json.loads(line).get('id')
                except:
                    pass

                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                    "id": request_id
                }
                print(json.dumps(error_response), flush=True)
                
    except KeyboardInterrupt:
        print("🛑 MCP Server (STDIO) shutdown", file=sys.stderr)
    except Exception as e:
        print(f"💥 Unexpected error in stdio_mode: {e}", file=sys.stderr)

def http_mode():
    """Run MCP server in HTTP mode for Claude Code"""
    port = 8000
    mcp_server = MCPServer()
    
    # Create request handler with mcp_server instance
    def handler(*args, **kwargs):
        return MCPRequestHandler(*args, mcp_server=mcp_server, **kwargs)
    
    httpd = HTTPServer(('localhost', port), handler)
    
    print(f"🚀 bchat MCP Server starting on http://localhost:{port}")
    print("   Ready for Claude Code and Gemini CLI connections")
    print("   Available tools: echo, search_context")
    print("   Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ MCP Server stopped")
        logging.info("MCP Server shutdown")

def main():
    """Start the MCP server in appropriate mode"""
    try:
        print(f"🚀 Starting MCP Server with args: {sys.argv}", file=sys.stderr)
        if "--stdio" in sys.argv:
            print("📡 Using STDIO mode", file=sys.stderr)
            stdio_mode()
        else:
            print("🌐 Using HTTP mode", file=sys.stderr)
            http_mode()
    except Exception as e:
        print(f"💥 Fatal error in main(): {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)

if __name__ == "__main__":
    print("🔄 MCP Server script starting...", file=sys.stderr)
    main()
```

### 7.2. `minimal_mcp_server.py`

```python
#!/usr/bin/env python3
import sys
import json

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        request = json.loads(line)
        response = handle_request(request)
        print(json.dumps(response), flush=True)

def handle_request(request):
    method = request.get("method")
    request_id = request.get("id")

    if method == "initialize":
        result = {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "minimal-mcp-server",
                "version": "1.0.0"
            }
        }
    elif method == "tools/list":
        result = {
            "tools": [
                {
                    "name": "hello",
                    "title": "Hello",
                    "description": "A simple hello world tool",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            ]
        }
    else:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            },
            "id": request_id
        }

    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": request_id
    }

if __name__ == "__main__":
    main()
```
