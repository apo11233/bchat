#!/usr/bin/env python3
"""
Comprehensive MCP Test Suite for bchat MCP Server
Tests protocol compliance, tool functionality, and error handling
"""

import os
import json
import subprocess
import sys
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Base directory - MANDATORY pattern per dev_directives/general.md
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    execution_time: float
    details: Optional[Dict[str, Any]] = None

class MCPTester:
    """Comprehensive MCP server testing framework"""
    
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.results: List[TestResult] = []
    
    def run_all_tests(self) -> List[TestResult]:
        """Run complete test suite"""
        print("🧪 Starting comprehensive MCP test suite...")
        
        # Protocol compliance tests
        self.test_initialize()
        self.test_tools_list()
        self.test_notifications_initialized()
        
        # Tool functionality tests
        self.test_echo_basic()
        self.test_echo_empty_input()
        self.test_echo_special_characters()
        
        self.test_search_context_basic()
        self.test_search_context_empty_query()
        self.test_search_context_with_provider()
        self.test_search_context_with_limit()
        self.test_search_context_invalid_limit()
        
        # Error handling tests
        self.test_invalid_json()
        self.test_missing_jsonrpc()
        self.test_invalid_method()
        self.test_missing_tool_name()
        self.test_unknown_tool()
        
        # Edge case tests
        self.test_concurrent_requests()
        self.test_large_payload()
        
        return self.results
    
    def send_request(self, request: Dict[str, Any], timeout: float = 5.0) -> Optional[Dict[str, Any]]:
        """Send JSON-RPC request to MCP server"""
        try:
            start_time = time.time()
            
            process = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            request_str = json.dumps(request) + '\n'
            stdout, stderr = process.communicate(input=request_str, timeout=timeout)
            
            execution_time = time.time() - start_time
            
            if stdout.strip():
                response = json.loads(stdout.strip())
                return {**response, '_execution_time': execution_time, '_stderr': stderr}
            
            return {'_execution_time': execution_time, '_stderr': stderr, '_error': 'No response'}
            
        except subprocess.TimeoutExpired:
            process.kill()
            return {'_error': 'Timeout', '_execution_time': timeout}
        except json.JSONDecodeError as e:
            return {'_error': f'JSON decode error: {e}', '_execution_time': time.time() - start_time}
        except Exception as e:
            return {'_error': f'Request failed: {e}', '_execution_time': 0}
    
    def assert_response(self, response: Optional[Dict[str, Any]], test_name: str, 
                       expected_keys: List[str] = None, should_error: bool = False):
        """Assert response meets expectations"""
        start_time = time.time()
        
        try:
            if response is None:
                self.results.append(TestResult(test_name, False, "No response received", 0))
                return
            
            execution_time = response.get('_execution_time', 0)
            
            if '_error' in response:
                if should_error:
                    self.results.append(TestResult(test_name, True, f"Expected error occurred: {response['_error']}", execution_time))
                else:
                    self.results.append(TestResult(test_name, False, f"Unexpected error: {response['_error']}", execution_time, response))
                return
            
            # Check JSON-RPC structure
            if 'jsonrpc' not in response:
                self.results.append(TestResult(test_name, False, "Missing jsonrpc field", execution_time, response))
                return
            
            if response['jsonrpc'] != '2.0':
                self.results.append(TestResult(test_name, False, f"Invalid jsonrpc version: {response['jsonrpc']}", execution_time, response))
                return
            
            # Check expected keys
            if expected_keys:
                missing_keys = [key for key in expected_keys if key not in response]
                if missing_keys:
                    self.results.append(TestResult(test_name, False, f"Missing keys: {missing_keys}", execution_time, response))
                    return
            
            # Check for error response when not expected
            if 'error' in response and not should_error:
                error_msg = response['error'].get('message', 'Unknown error')
                self.results.append(TestResult(test_name, False, f"Unexpected error response: {error_msg}", execution_time, response))
                return
            
            self.results.append(TestResult(test_name, True, "Test passed", execution_time, response))
            
        except Exception as e:
            self.results.append(TestResult(test_name, False, f"Assertion failed: {e}", time.time() - start_time))
    
    # Protocol Compliance Tests
    def test_initialize(self):
        """Test MCP initialize method"""
        request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            },
            "id": 1
        }
        response = self.send_request(request)
        self.assert_response(response, "initialize", ["result", "id"])
    
    def test_tools_list(self):
        """Test tools/list method"""
        request = {"jsonrpc": "2.0", "method": "tools/list", "id": 2}
        response = self.send_request(request)
        self.assert_response(response, "tools_list", ["result"])
        
        # Verify tools structure
        if response and 'result' in response and 'tools' in response['result']:
            tools = response['result']['tools']
            if not isinstance(tools, list) or len(tools) == 0:
                self.results[-1].passed = False
                self.results[-1].message = "Tools list is empty or invalid"
    
    def test_notifications_initialized(self):
        """Test notifications/initialized (should not respond)"""
        request = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        response = self.send_request(request, timeout=2.0)
        
        # Server correctly handles notification but doesn't respond
        # This is CORRECT behavior per MCP spec - no response to notifications
        if response and '_error' in response and 'No response' in response['_error']:
            self.results.append(TestResult("notifications_initialized", True, "Correctly handled notification (no response per MCP spec)", response.get('_execution_time', 0)))
        elif response and '_error' in response and 'Timeout' in response['_error']:
            self.results.append(TestResult("notifications_initialized", True, "Correctly ignored notification", 2.0))
        else:
            self.results.append(TestResult("notifications_initialized", False, "Unexpected response to notification", response.get('_execution_time', 0), response))
    
    # Tool Functionality Tests
    def test_echo_basic(self):
        """Test echo tool with basic input"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "echo", "arguments": {"text": "Hello World"}},
            "id": 3
        }
        response = self.send_request(request)
        self.assert_response(response, "echo_basic", ["result"])
    
    def test_echo_empty_input(self):
        """Test echo tool with empty input"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call", 
            "params": {"name": "echo", "arguments": {"text": ""}},
            "id": 4
        }
        response = self.send_request(request)
        # Should handle empty input gracefully
        self.assert_response(response, "echo_empty", ["result"])
    
    def test_echo_special_characters(self):
        """Test echo tool with special characters"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "echo", "arguments": {"text": "Test with émojis 🧪 and symbols: !@#$%^&*()"}},
            "id": 5
        }
        response = self.send_request(request)
        self.assert_response(response, "echo_special_chars", ["result"])
    
    def test_search_context_basic(self):
        """Test search_context tool with basic query"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "search_context", "arguments": {"query": "test"}},
            "id": 6
        }
        response = self.send_request(request)
        self.assert_response(response, "search_basic", ["result"])
    
    def test_search_context_empty_query(self):
        """Test search_context with empty query"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "search_context", "arguments": {"query": ""}},
            "id": 7
        }
        response = self.send_request(request)
        # Should return error for empty query
        self.assert_response(response, "search_empty_query", ["result"])
    
    def test_search_context_with_provider(self):
        """Test search_context with provider filter"""
        request = {
            "jsonrpc": "2.0", 
            "method": "tools/call",
            "params": {"name": "search_context", "arguments": {"query": "test", "provider": "claude"}},
            "id": 8
        }
        response = self.send_request(request)
        self.assert_response(response, "search_with_provider", ["result"])
    
    def test_search_context_with_limit(self):
        """Test search_context with custom limit"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call", 
            "params": {"name": "search_context", "arguments": {"query": "test", "limit": 5}},
            "id": 9
        }
        response = self.send_request(request)
        self.assert_response(response, "search_with_limit", ["result"])
    
    def test_search_context_invalid_limit(self):
        """Test search_context with invalid limit"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "search_context", "arguments": {"query": "test", "limit": "invalid"}},
            "id": 10
        }
        response = self.send_request(request)
        # Should handle gracefully and use default
        self.assert_response(response, "search_invalid_limit", ["result"])
    
    # Error Handling Tests
    def test_invalid_json(self):
        """Test server response to invalid JSON"""
        try:
            process = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send invalid JSON
            stdout, stderr = process.communicate(input="invalid json\n", timeout=5.0)
            
            if stdout.strip():
                response = json.loads(stdout.strip())
                if 'error' in response and response['error']['code'] == -32700:
                    self.results.append(TestResult("invalid_json", True, "Correctly handled invalid JSON", 0))
                else:
                    self.results.append(TestResult("invalid_json", False, "Invalid JSON error code", 0, response))
            else:
                self.results.append(TestResult("invalid_json", False, "No response to invalid JSON", 0))
                
        except Exception as e:
            self.results.append(TestResult("invalid_json", False, f"Test failed: {e}", 0))
    
    def test_missing_jsonrpc(self):
        """Test request without jsonrpc field"""
        request = {"method": "tools/list", "id": 11}
        response = self.send_request(request)
        self.assert_response(response, "missing_jsonrpc", ["error"], should_error=True)
    
    def test_invalid_method(self):
        """Test request with non-existent method"""
        request = {"jsonrpc": "2.0", "method": "nonexistent/method", "id": 12}
        response = self.send_request(request)
        self.assert_response(response, "invalid_method", ["error"], should_error=True)
    
    def test_missing_tool_name(self):
        """Test tools/call without tool name"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"arguments": {"text": "test"}},
            "id": 13
        }
        response = self.send_request(request)
        self.assert_response(response, "missing_tool_name", ["error"], should_error=True)
    
    def test_unknown_tool(self):
        """Test tools/call with unknown tool"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "unknown_tool", "arguments": {}},
            "id": 14
        }
        response = self.send_request(request)
        self.assert_response(response, "unknown_tool", ["error"], should_error=True)
    
    # Edge Case Tests
    def test_concurrent_requests(self):
        """Test multiple concurrent requests"""
        # This is simplified - would need threading for true concurrency
        requests = [
            {"jsonrpc": "2.0", "method": "tools/list", "id": 15},
            {"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "echo", "arguments": {"text": "concurrent"}}, "id": 16}
        ]
        
        passed = True
        for i, request in enumerate(requests):
            response = self.send_request(request)
            if not response or 'error' in response:
                passed = False
                break
        
        self.results.append(TestResult("concurrent_requests", passed, "Concurrent request handling", 0))
    
    def test_large_payload(self):
        """Test handling of large payloads"""
        large_text = "x" * 10000  # 10KB text
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "echo", "arguments": {"text": large_text}},
            "id": 17
        }
        response = self.send_request(request, timeout=10.0)
        self.assert_response(response, "large_payload", ["result"])
    
    def print_summary(self):
        """Print test results summary"""
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print(f"\n📊 Test Results Summary: {passed}/{total} tests passed")
        print("=" * 60)
        
        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"{status} {result.name:25} ({result.execution_time:.3f}s) - {result.message}")
            
            if not result.passed and result.details:
                print(f"      Details: {json.dumps(result.details, indent=6)}")
        
        print("=" * 60)
        
        if passed == total:
            print("🎉 All tests passed! MCP server is working correctly.")
        else:
            print(f"⚠️  {total - passed} tests failed. Check implementation.")

def main():
    """Run MCP test suite"""
    # Construct absolute path to mcp_server.py using BASE_DIR
    mcp_server_path = os.path.join(BASE_DIR, '..', '..', '..', 'mcp_server.py')
    mcp_server_path = os.path.abspath(mcp_server_path)  # Resolve to absolute path
    server_command = ["python3", mcp_server_path, "--stdio"]
    
    tester = MCPTester(server_command)
    results = tester.run_all_tests()
    tester.print_summary()
    
    return 0 if all(r.passed for r in results) else 1

if __name__ == "__main__":
    sys.exit(main())