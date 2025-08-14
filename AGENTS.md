# Context Engineering Instructions for Jules

This document provides the necessary context and instructions for working on the `bchat` project.

## 1. Project Overview

**Project Name**: `bchat` (AI CLI Chat Logger)

**Goal**: To create a world-class, context-aware AI assistant that can understand and leverage the full history of a project to provide intelligent and insightful responses. The project is evolving into **BChat MCP**, a comprehensive AI collaboration platform.

**Core Idea**: The project is built on the principle of "technical context preservation". It captures not just *what* was decided in AI development sessions, but the crucial *how* and *why*.

**Current Status**: The project has a functional MCP server with enhanced search capabilities. The development follows a staged workflow, and the current focus is on "Advanced Implementation". For the most up-to-date status, refer to `@/Users/admin/Documents/Developer/bchat/dev/dev_stages/stages_workflow.md`.

## 2. Core Development Methodology: Layered Contextual Memory Development

The `bchat` project follows a strict, staged development methodology designed for complex AI systems. Understanding this is crucial for any task.

**Key Principles**:
- **Iterative Progression**: Each stage builds on the previous, validated stage.
- **Contextual Memory**: All decisions, rationale, and history are preserved in documentation within each stage.
- **User Control**: Explicit user approval is required for any significant changes.
- **Safety First**: Never break working functionality.

**Layered Structure**:
- **Stage Layer (`/dev/dev_stages/ST_XX_*`)**: Defines WHAT to implement and WHEN. This is the primary source of truth for project status and history.
- **Directive Layer (`/dev/dev_directives/`)**: Defines HOW to implement safely and consistently.
- **Context Layer (`CLAUDE.md`, `llm.txt`)**: Explains WHY decisions were made.
- **System Layer (logs, filemap, git)**: Provides operational memory and traceability.

For a complete understanding of the workflow, you **MUST** refer to `@/Users/admin/Documents/Developer/bchat/dev/dev_directives/staged_development_workflow.md`.

## 3. Key Project Files for Context

To accomplish any task related to this project, you must first understand the context provided in these key files:

- **`@/Users/admin/Documents/Developer/bchat/README.md`**: High-level overview, features, and quick start.
- **`@/Users/admin/Documents/Developer/bchat/dev/INITIAL.md`**: The document that marked the beginning of the current development initiative.
- **`@/Users/admin/Documents/Developer/bchat/CLAUDE.md`**: The project's high-level goals and vision.
- **`@/Users/admin/Documents/Developer/bchat/dev/dev_stages/stages_workflow.md`**: The **most important file** for understanding the project's current status, completed stages, and future roadmap.
- **`@/Users/admin/Documents/Developer/bchat/dev/dev_directives/general.md`**: General development guidelines that **MUST** be followed.
- **`@/Users/admin/Documents/Developer/bchat/dev/dev_directives/gemini_specific_guidelines.md`**: Specific instructions for Gemini.
- **`@/Users/admin/Documents/Developer/bchat/dev/dev_directives/staged_development_workflow.md`**: The detailed protocol for the development workflow.

## 4. Development Directives Summary

All work on this project **MUST** adhere to the following directives:

- **File Management**: Prefer editing existing files over creating new ones. Never create documentation files unless explicitly asked.
- **Code Quality**: Follow existing conventions and patterns. Do not add new dependencies without verification.
- **Security**: Never expose or commit secrets.
- **Project Structure**: Respect the existing architecture. Use the `dev/dev_stages` directory for all work.
- **Path Management**: **NEVER** use relative paths. Always use the `BASE_DIR` pattern with `os.path.join()` as defined in `general.md`.
- **Safety First**: Follow the safety and rollback procedures in `@/Users/admin/Documents/Developer/bchat/dev/dev_directives/implementation_safety.md`.

## 5. How to Approach a Task

To accomplish any task, follow the **Layered Contextual Memory Development Methodology**:

1.  **Stage Discovery**: Identify the correct stage for your work in `/dev/dev_stages/`. Do not create new stages without permission.
2.  **Context Loading**: Read all the documentation in the relevant stage directory, especially the `llm.txt` file.
3.  **System Verification**: Check the current status of the system with `./bchat --status`.
4.  **Planning**: For complex tasks, create a plan using `TodoWrite`.
5.  **User Approval**: **GET EXPLICIT USER APPROVAL** before creating, updating, or deleting any files.
6.  **Implementation**: Make small, incremental changes and test after each one.
7.  **Validation**: Run all available checks and tests.
8.  **Documentation**: Update all relevant documentation, including a new stage work document (`NN-YYMMDD-descriptive_name.md`), the stage's `llm.txt`, and the main `filemap.md` if the file structure has changed.

By following these instructions, you will be able to work on the `bchat` project effectively, safely, and in a way that preserves the project's valuable context.
