### Core Functionalities of MCP Servers for Gemini CLI and Claude Code

Based on in-depth analysis of the Model Context Protocol (MCP), which is the standardized protocol used by both Gemini CLI (Google's AI agentic CLI tool) and Claude Code (Anthropic's CLI tool, often referred to as Claude CLI), the core functionalities revolve around enabling AI agents to access external data, tools, and context in a secure, standardized manner. MCP servers act as intermediaries, exposing capabilities like tools, resources, and prompts that the CLIs can discover and invoke during their reason-and-act (ReAct) loops for tasks such as code generation, bug fixing, or data retrieval.

MCP was introduced by Anthropic but adopted by Google for Gemini CLI, making it a shared standard. The CLIs "recognize" they are in an MCP environment when configured to connect to an MCP server URL (local or remote), and the server responds to capability queries, tool lists, and invocations via the protocol's transports (e.g., HTTP, Server-Sent Events (SSE), or STDIO). Recognition typically involves the CLI sending an initial connection request, discovering capabilities (e.g., "tools" support), and receiving valid responses without errors like unauthorized access.

#### Core Functionalities Requested by Gemini CLI
Gemini CLI uses MCP servers to extend its ReAct loop, allowing the AI to interact with external systems for complex workflows (e.g., fixing bugs in codebases or integrating with tools like GitHub). Key requirements:
- **Tool Discovery and Invocation**: The server must expose tools (e.g., for querying data or performing actions) that Gemini CLI can list and call dynamically.
- **Context Provision**: Servers provide resources (e.g., file contents, database queries) to give the AI relevant context without manual input.
- **Authentication**: Supports OAuth 2.1 for secure access, with Gemini CLI handling token flows for restricted tools.
- **Transports**: Primarily HTTP/SSE for local/remote servers; STDIO for simple local testing.
- **Capabilities**: Must declare support for "tools", "resources", and optionally "prompts" or notifications (e.g., for tool list changes).
- **Error Handling and Security**: Handles JSON-RPC errors, validates inputs, and ensures human oversight prompts for sensitive actions.
- **Integration**: Gemini CLI configures MCP servers via settings (e.g., ~/.gemini/settings.json), and uses them to pull context from sources like Google Drive or custom tools.

Official Documentation for Further Research:
- Gemini CLI Overview: https://cloud.google.com/gemini/docs/codeassist/gemini-cli
- Google Blog on Gemini CLI and MCP: https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/

#### Core Functionalities Requested by Claude Code (Claude CLI)
Claude Code integrates MCP servers to enhance terminal-based coding, allowing the AI to access external datasources (e.g., Google Drive, Jira, Slack) and custom tools. It recognizes the MCP environment similarly, via successful connection and capability discovery. Key requirements:
- **Tool and Resource Access**: Exposes tools for actions (e.g., updating tickets) and resources for reading data (e.g., design docs), invoked in the ReAct loop.
- **Notifications and Updates**: Supports notifications for changes (e.g., tool list updates) to keep the AI informed.
- **Authentication**: OAuth 2.1-based, with CLI flags like --permission-prompt-tool for handling auth prompts.
- **Transports**: HTTP/SSE for broader integration; STDIO for local dev.
- **Capabilities**: Declares "tools", "resources", and optionally "listChanged" for dynamic updates.
- **Security and Oversight**: Includes user confirmation for invocations, input validation, and error reporting (e.g., isError flag).
- **Integration**: Configured via CLI flags (e.g., claude -p --permission-prompt-tool mcp_auth_tool "query"), with support for resuming sessions and custom tools.

Official Documentation for Further Research:
- Claude Code Overview: https://docs.anthropic.com/en/docs/claude-code/overview
- Claude Code CLI Reference: https://docs.anthropic.com/en/docs/claude-code/cli-reference
- Anthropic MCP Docs: https://docs.anthropic.com/en/docs/mcp
- MCP Announcement by Anthropic: https://www.anthropic.com/news/model-context-protocol

#### Merged Requirements and Specifications for Developing an MCP Server from Scratch
Since both CLIs adhere to the same MCP standard, the merged requirements are essentially the full MCP protocol specification. This allows a single server to support both Gemini CLI and Claude Code without separate implementations. Focus on local deployment (e.g., running on localhost), using HTTP/SSE transports for compatibility, and optional STDIO for testing. Key merged specs:

- **Capabilities**: Servers must advertise supported features (e.g., "tools", "resources", "prompts") via a capabilities response on connection.
- **Tools**:
  - Definition: JSON objects with name, title, description, inputSchema/outputSchema (JSON Schema), and annotations.
  - Discovery: Via "tools/list" method (JSON-RPC), with pagination support (cursor/nextCursor).
  - Invocation: Via "tools/call" method, with arguments matching inputSchema; responses include content (unstructured: text/image/audio/resource links) or structuredContent (JSON).
  - Notifications: Optional "notifications/tools/list_changed" for updates.
- **Resources**: Similar to tools but read-only (e.g., "resources/read" method for fetching data like files).
- **Prompts**: Reusable templates (e.g., "prompts/call" for generating text based on inputs).
- **Authentication**: Optional but required for restricted access; uses OAuth 2.1 with:
  - Grants: Authorization Code (for user auth) and Client Credentials (app-to-app).
  - Tokens: Bearer in headers; validate per RFC.
  - Dynamic Registration: Support RFC7591 for client IDs.
- **Transports and Protocol**:
  - JSON-RPC 2.0 over HTTP (POST for requests), SSE (for streaming/notifications), or STDIO (stdin/stdout for local).
  - Error Codes: Standard JSON-RPC (e.g., -32601 for unknown method) plus MCP-specific (e.g., isError for tool failures).
- **Security**: HTTPS required; validate schemas, rate limit, log invocations; CLIs handle user prompts for oversight.
- **Minimal Dependencies**: Implement using Python standard library (http.server for HTTP, json for parsing, no external libs like FastAPI). For OAuth, use stdlib urllib for token handling; avoid full SDKs.

Official Documentation for Further Research on MCP Specs:
- MCP Main Site: https://modelcontextprotocol.io/
- Tools Spec: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- Authorization Spec: https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization
- Python SDK (for reference/examples, not required): https://github.com/modelcontextprotocol/python-sdk
- MCP Servers Repo (examples): https://github.com/modelcontextprotocol/servers

### Implementation Plan: Actionable Workflow from Core to MVP
Develop the server in Python 3.x using only standard library modules (e.g., http.server, json, threading for SSE, urllib for OAuth basics) to meet the "minimal or none external dependency" goal. Run locally on localhost:8000. Total estimated time: 5-10 hours for a beginner, assuming basic Python knowledge.

#### Phase 1: Core (Basic Server Without Auth – 1-2 hours)
- **Steps**:
  1. Set up a basic HTTP server using http.server.HTTPServer.
  2. Handle POST requests to a single endpoint (e.g., /mcp) for JSON-RPC methods.
  3. Implement capabilities response: On connection (initial GET or POST), return {"capabilities": ["tools"]}.
  4. Add "tools/list": Return a list with one dummy tool (e.g., {"name": "echo", "description": "Echo input", "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}}}}).
  5. Add "tools/call": For "echo", return {"content": [{"type": "text", "text": input_text}]}.
- **Checkpoints/Tests**:
  - Run server: python server.py – should listen on localhost:8000.
  - Test connection: Use curl POST with JSON-RPC {"method": "tools/list"} – expect 200 OK with tool list.
  - Test invocation: curl POST {"method": "tools/call", "params": {"name": "echo", "arguments": {"text": "hello"}}} – expect echoed response.
  - No external deps; verify with sys.modules inspection.

#### Phase 2: Add Transports and Basic Auth (2-3 hours)
- **Steps**:
  1. Add SSE support: Use threading to handle /events endpoint, sending event: data JSON for notifications.
  2. Implement STDIO transport: Optional loop reading from stdin, writing to stdout for local testing.
  3. Add basic OAuth: Hardcode a token verifier (e.g., check for Authorization: Bearer test_token header). Return 401 if missing.
  4. Expand tools: Add a resource (e.g., "resources/read" for dummy file content) and a prompt (e.g., "prompts/call" for templated text).
- **Checkpoints/Tests**:
  - SSE test: Connect with curl --no-buffer -H "Accept: text/event-stream" http://localhost:8000/events – send a test notification.
  - Auth test: curl without header – expect 401; with header – expect success.
  - STDIO test: Pipe input JSON to python server.py --stdio – verify output.

#### Phase 3: Full OAuth and Security (2-3 hours)
- **Steps**:
  1. Implement OAuth endpoints: /authorize (redirect for code grant), /token (issue access_token), /register (dynamic client reg).
  2. Use stdlib urllib to simulate AS discovery and token validation (hardcode metadata for local).
  3. Add input/output schema validation using json (manual checks, no external validator).
  4. Implement error handling: JSON-RPC codes, isError flag.
  5. Add security: Timeout invocations (threading.Timer), log requests (print to console).
- **Checkpoints/Tests**:
  - OAuth flow: Simulate auth code grant with browser redirect – obtain token, use in header.
  - Validation: Send invalid schema args – expect error response.
  - Security: Test timeout on long-running tool – expect abort.

#### Phase 4: MVP (Integration with CLIs – 1-2 hours)
- **Steps**:
  1. Add real tools: E.g., a local file reader (resources/read from disk), calculator tool.
  2. Configure CLIs: For Gemini CLI, edit ~/.gemini/settings.json with "mcp_servers": [{"url": "http://localhost:8000"}]. For Claude Code, use CLI flag --mcp-url http://localhost:8000.
  3. Handle notifications: Send list_changed on tool updates.
- **Checkpoints/Tests**:
  - Gemini CLI test: Run gemini "fix bug using MCP tool" – verify server logs invocation.
  - Claude Code test: Run claude "query file via MCP" – verify tool call and response.
  - Cross-CLI: Use same server for both – confirm no conflicts.
  - Local-only: No internet calls; all data from disk.

Once MVP is reached, iterate by adding more tools based on CLI needs (e.g., Git integration using subprocess for local commands). For production-like, self-sign HTTPS cert with stdlib ssl, but keep local. If stdlib limits arise (e.g., full OAuth), note as optional extension.