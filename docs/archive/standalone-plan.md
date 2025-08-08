# Plan: Standalone bchat Application

## Executive Summary
This document outlines the plan to evolve the `chat_monitor.py` system from a project-specific tool into a self-contained, standalone application. The goal is to create a package that can be easily installed into any project workspace, automatically managing its own dependencies and configuration. This will enhance portability, prevent dependency conflicts, and simplify deployment across different projects.

## What
We will refactor the existing bchat scripts and configuration into a standard Python package structure. This package will include an installer script that handles all setup, including dependency installation and initial configuration, making the tool project-agnostic.

## Why
- **Portability:** Easily deploy bchat in any project without manual setup.
- **Dependency Isolation:** Avoids conflicts with project-specific dependencies by using a dedicated virtual environment.
- **Simplified Deployment:** A single command will install and configure the entire application.
- **Maintainability:** A standardized structure makes the codebase easier to manage and update.

## How: Proposed Architecture

The application will be restructured into a formal Python package. An installation script will orchestrate the setup, creating a self-contained environment within the target project's workspace.

### Proposed Directory Structure

The application will be organized into the following structure within the `bchat` directory:

```
bchat/
├── install.sh
├── README.md
├── requirements.txt
├── config.template.json
└── src/
    ├── __init__.py
    ├── main.py
    ├── monitor/
    │   ├── __init__.py
    │   ├── monitor.py
    │   ├── api_manager.py
    │   └── file_handler.py
    └── utils/
        ├── __init__.py
        └── path_manager.py
```

### Key Components

1.  **`install.sh`**: The main installation script. This will be the single entry point for setting up the application.
2.  **`src/`**: The main application code, structured as a Python package.
    *   `main.py`: The entry point for running the monitor.
    *   `monitor/`: The core logic for file watching, API calls, and event handling.
    *   `utils/`: Shared utilities like the `PathManager`.
3.  **`requirements.txt`**: A file listing all required Python dependencies (`watchdog`, `google-generativeai`, `python-dotenv`).
4.  **`config.template.json`**: A template of the `config.json` file. The installer will copy this to the project's root or a `.config/` directory.

## Implementation Phases

### Phase 1: Code Refactoring & Packaging

1.  **Restructure Files:** Move all Python code into the `src/` directory, organizing it into the `monitor` and `utils` sub-packages as shown above.
2.  **Create `main.py`:** Consolidate the script's entry point logic (argument parsing, starting the monitor) into `src/main.py`.
3.  **Update Imports:** Modify all internal imports to be relative within the `src` package (e.g., `from monitor.monitor import ChatMonitor`).
4.  **Create `requirements.txt`:** List all Python dependencies in this file.

### Phase 2: Create the Installation Script (`install.sh`)

This script will perform the following steps:

1.  **Create a Virtual Environment:** Create a local Python virtual environment (e.g., in `.venv-chat-monitor`) to isolate dependencies.
2.  **Install Python Dependencies:** Activate the virtual environment and install the packages from `requirements.txt` using `pip install -r requirements.txt`.
3.  **Check for Gemini CLI:**
    *   Check if the `gemini` command is available in the system's PATH.
    *   If not found, prompt the user to install it globally with `npm install -g @google/gemini-cli` and provide instructions.
4.  **Copy Configuration:**
    *   Check if a `config.json` for the monitor already exists in the project root.
    *   If not, copy the `config.template.json` to the project root as `config.json`.
5.  **Provide Instructions:** Display a message confirming the installation is complete and show the command to run the monitor:
    ```bash
    source .venv-chat-monitor/bin/activate
    python3 bchat/src/main.py
    ```

### Phase 3: Documentation

1.  **Update `README.md`:** Create a new `README.md` inside the `chat_monitor_app` directory with clear instructions on how to use the `install.sh` script and run the application.
2.  **Update Existing Documentation:** Ensure all other documentation files are updated to reference the new installation process and structure.

## Usage After Installation

Once the `install.sh` script has been run in a project, the user can start the monitor with the following commands:

```bash
# Activate the dedicated virtual environment
source .venv-chat-monitor/bin/activate

# Run the monitor in the background
python3 bchat/src/main.py &
```

This plan will result in a truly portable and self-contained bchat application, making it a valuable and easily reusable tool for any development workspace.