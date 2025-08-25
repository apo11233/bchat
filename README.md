bchat — Local AI CLI Context Memory & Workflow for VS Code Developers
====================================================================

[https://github.com/apo11233/bchat/releases](https://github.com/apo11233/bchat/releases)  
[![Releases](https://img.shields.io/badge/Releases-Download-brightgreen)](https://github.com/apo11233/bchat/releases)

Badges
------
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/) [![VSCode](https://img.shields.io/badge/VS%20Code-Extension-blueviolet)](https://code.visualstudio.com/)  
[![Topics](https://img.shields.io/badge/topics-ai--tools%20%7C%20bchat%20%7C%20cli-lightgrey)](https://github.com/apo11233/bchat)  
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

What is bchat? 🧠
----------------
bchat is a local Python utility that adds AI-powered context memory to CLI sessions inside Visual Studio Code. It stores and reuses chat context, integrates with MCP Server for Gemini-CLI and Claude Code, and bundles a stage-based project meta-workflow from seed to MVP. The project follows a local-first design so you keep control of data and workflow.

Status: the repo is being refactored. Not all features work. Use releases for runnable builds.

Quick start — Releases
----------------------
Download a release asset and execute it. Pick the release that matches your OS, download the file, and run it. For example:

- Linux/macOS: download the asset, then run
  - chmod +x ./bchat-linux && ./bchat-linux
- Windows: download the .exe and run it from PowerShell or CMD

Visit and download from the releases page: https://github.com/apo11233/bchat/releases  
[![Releases](https://img.shields.io/badge/Get%20Release-Open%20Releases-blue)](https://github.com/apo11233/bchat/releases)

Core concepts
-------------
- Local-first: store context on disk. Avoid external dependencies for core memory.
- CLI context memory: capture terminal sessions, prompts, and responses. Attach memory to projects.
- MCP Server: a small server that routes requests for Gemini-CLI and Claude Code integrations.
- Stage-based workflow: seed → prototype → MVP → production. Each stage has tasks and checkpoints.
- LLM approach: modular LLM wrappers to swap models or providers without changing the CLI.

What bchat provides
-------------------
- Persistent chat logs per project and per terminal session.
- Fast retrieval of recent context to prime LLMs.
- MCP Server for local routing and automation with Gemini-CLI and Claude Code.
- A meta-workflow file structure that maps project stages and tasks.
- CLI utilities to view, trim, and export chat logs.
- VS Code helpers that integrate memory into the terminal and editor.

Features
--------
- Chat logs stored as JSON/NDJSON for easy parsing.
- CLI commands to attach/detach memory contexts to shells.
- Plugins for Gemini-CLI and Claude Code (via MCP Server).
- Search and live tail for chat logs.
- Basic monitoring and automation hooks to trigger workflows.
- Example workflows for seed → MVP with task templates.

Architecture overview
---------------------
- bchat core (Python): handles storage, indexing, and CLI commands.
- MCP Server (Python/HTTP): routes requests from local clients (Gemini-CLI / Claude Code).
- Storage layer: lightweight JSON files, optional SQLite index for fast lookups.
- VS Code integration: extension or terminal helper scripts that inject context into prompts.
- Plugins: small adapters that define how to call an LLM provider or CLI tool.

File and folder layout
----------------------
- bin/ — release binaries and helper scripts (download from Releases and run)
- bchat/ — Python package (core modules)
- mcp_server/ — MCP Server implementation
- docs/ — architecture sketches and workflow templates
- examples/ — CLI usage and VS Code snippets
- workflows/ — seed → prototype → MVP templates
- tests/ — unit and integration tests

Install from source
-------------------
1. Clone repository
   - git clone https://github.com/apo11233/bchat.git
2. Create venv and install
   - python -m venv .venv
   - source .venv/bin/activate
   - pip install -r requirements.txt
3. Start MCP Server
   - python -m mcp_server.app --port 8080
4. Run bchat CLI
   - python -m bchat.cli init
   - python -m bchat.cli attach

If you prefer a runnable build, download the packaged asset on the Releases page, then run that file. For platform-specific instructions, check the release notes.

Basic CLI usage
---------------
- Initialize a project workspace
  - bchat init --project my-app
- Attach memory to current shell
  - bchat attach --session dev-shell
- Save an entry manually
  - bchat log --session dev-shell --message "Ran unit tests; fixed failing import"
- Query recent context
  - bchat recall --session dev-shell --n 5
- Export logs
  - bchat export --session dev-shell --format ndjson --out logs.ndjson
- Trim old logs
  - bchat trim --older-than 30d

MCP Server usage (Gemini-CLI, Claude Code)
------------------------------------------
- Start the server locally:
  - python -m mcp_server.app --port 8080
- Point Gemini-CLI or Claude Code adapter to:
  - http://localhost:8080/v1
- MCP Server accepts requests, enriches them with project context, and forwards them to the configured LLM endpoint or local adapter.

Example: call from a shell
- Export endpoint
  - export BCHAT_MCP_ENDPOINT=http://localhost:8080/v1
- Send a prompt (pseudo)
  - curl -X POST $BCHAT_MCP_ENDPOINT/gemini -d '{"prompt":"Explain this bug"}'

Project meta-workflow (seed → MVP)
----------------------------------
bchat includes a stage-based meta-workflow to guide development. Each stage has tasks, acceptance criteria, and checkpoints.

- Seed
  - Define core idea, user stories, and minimal tech stack.
  - Tasks: write 3 stories, create initial repository, install bchat locally.
- Prototype
  - Build a fast demo using local LLM or small model.
  - Tasks: add basic memory capture, create demo script for VS Code terminal.
- MVP
  - Harden storage, add MCP Server integration, add CI tests.
  - Tasks: integrate Claude Code adapter, test Gemini-CLI path, add UX improvements.
- Production
  - Add monitoring, scale tests, documentation, release automation.

Each workflow contains templates in workflows/ to copy into a project.

Storage and privacy
-------------------
bchat stores chat logs and context on disk under a per-project directory. Logs use plain JSON or NDJSON for portability. You can:

- Encrypt files with your key (recommended for sensitive projects).
- Configure retention and archival rules.
- Export logs in multiple formats.

Monitoring and automation
-------------------------
- Basic monitoring scripts watch log sizes and send alerts when thresholds trigger.
- Automation hooks run actions when specific patterns appear in chat logs (for example, when a task completes).
- Build your own monitor by subscribing to the logs directory and responding to NDJSON lines.

Examples and screenshots
------------------------
- VS Code terminal with bchat memory attached (conceptual):
  - ![VS Code Terminal](https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg)
- MCP Server diagram (conceptual):
  - ![Architecture](https://img.shields.io/badge/Architecture-MCP%20Server%20%7C%20Adapters-brightgreen)

Extending bchat
---------------
- Adapters: add new adapters for other LLMs or CLIs by implementing the adapter interface in bchat/adapters/.
- Storage: swap JSON for a binary store or encrypted vault by implementing the storage interface.
- VS Code: build a lightweight extension that calls bchat.recall when the terminal receives a prompt.

Configuration
-------------
bchat loads config from bchat.yaml in the project root or from environment variables.

Key config values:
- storage.path: path to store chat logs
- mcp.port: port for MCP Server
- adapters: list of enabled adapters (gemini, claude_code, local)
- retention.days: days to keep logs (0 to keep forever)

Sample bchat.yaml
- storage:
  - path: .bchat/logs
- mcp:
  - port: 8080
- adapters:
  - - gemini
  - - claude_code
- retention:
  - days: 30

Troubleshooting
---------------
- If MCP Server fails to start, verify the port is free and check logs in mcp_server/logs.
- If LLM calls time out, confirm adapters are configured and keys or local endpoints are reachable.
- If chat logs don’t appear, verify bchat attach completed and the session name matches.

Contributing
------------
- Fork repo and open pull requests against main.
- Add tests for new features under tests/.
- Follow the stage-based workflow: create an issue tagged with the stage you target.
- Keep changes modular: adapters, storage, and CLI code live in separate packages.

Roadmap
-------
- Full refactor to decouple core from adapters.
- Replace file-based index with optional SQLite index for faster recall.
- Add encrypted storage option.
- Provide a VS Code extension that uses bchat under the hood.
- Improve monitoring automation and add pre-made integrations.

License
-------
MIT. See the LICENSE file.

Releases and binaries
---------------------
Release binaries and packaged installers live on the Releases page. Download the asset that matches your platform and execute it. For example, download the Linux or macOS binary and run:

- chmod +x ./bchat-linux && ./bchat-linux

Find and get the releases here: https://github.com/apo11233/bchat/releases  
[![Download Releases](https://img.shields.io/badge/Release%20Page-Open-orange)](https://github.com/apo11233/bchat/releases)

Contact and links
-----------------
- Repo: https://github.com/apo11233/bchat
- Releases: https://github.com/apo11233/bchat/releases
- Issues: open an issue on GitHub for bugs or feature requests

License and credits
-------------------
This project uses open-source components. Check LICENSE for details.

Images and assets used in this README come from public sources and icons.