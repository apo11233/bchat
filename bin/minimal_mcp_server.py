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
