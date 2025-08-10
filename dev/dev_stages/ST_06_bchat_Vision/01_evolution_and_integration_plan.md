# The Evolution Plan: From `bchat` to `bchat_mcp`

**Date**: 2025-08-09
**Stage**: ST_06 (BChat MCP Vision)
**Author**: Gemini Assistant
**Status**: PROPOSED

## 1. Goal

To create a clear, iterative implementation plan for evolving the current, functional `bchat` system into the ambitious, multi-AI `bchat_mcp` vision, as outlined in the manifesto.

## 2. Current State Assessment

We have successfully refactored `bchat` into a robust, on-demand, context-aware tool. It has a functional "Deep Context Engine" that can parse `bchat` logs and Claude's internal files. This is the solid foundation upon which we will build.

## 3. The Iterative Evolution Plan

We will follow the iterative roadmap laid out in the `bchat_mcp` manifesto. Here is how we will get there from our current state:

### Iteration 1: Solidify the Core & Implement the `llm.txt` Concept

*   **Goal**: To implement the core `bchat_core.py` functionality and the AI-driven `llm.txt` context generation.
*   **Steps**:
    1.  **Refactor `ChatProcessor` to `BChatCore`**: Rename and refactor our existing `ChatProcessor` to become the new `BChatCore`, which will manage stages, directives, and the new layered context.
    2.  **Implement `llm.txt`**: Create the `llm.txt` file structure (`/llm.txt`, `/.bchat/stages/ST_XX/llm.txt`).
    3.  **Implement the `ai_update_context` function**: This will be the core of the PRP (Prompt-Response-Process) cycle. After each AI call, this function will be used to update the relevant `llm.txt` files with the AI's insights.
    4.  **Integrate with existing parsers**: The context from our existing parsers (`ClaudeMdParser`, `ConversationHistoryParser`, etc.) will be used to enrich the `llm.txt` files.

### Iteration 2: Implement the Shared Memory and MCP Foundation

*   **Goal**: To build the `llm_shared_memory.py` and the basic `bchat_mcp_server.py`.
*   **Steps**:
    1.  **`llm_shared_memory.py`**: Create this new component to unify conversations from both Claude and Gemini, using the `bchat` logs as the source of truth.
    2.  **`bchat_mcp_server.py`**: Implement a basic MCP server that can expose a few key capabilities, like `memory/search`.

### Iteration 3: Full Machine-to-Machine Collaboration

*   **Goal**: To achieve the ultimate vision of autonomous AI-to-AI collaboration.
*   **Steps**:
    1.  **Implement the `WorkflowEngine`**: This will orchestrate the complex, multi-step workflows between AIs.
    2.  **Implement the `ai_collaboration_session`**: This will be the high-level function that allows one AI to hand off a task to another, using the unified context provided by `bchat`.

## 4. A Request for Collaboration with Claude

To ensure the success of this ambitious plan, we will need to continue our fruitful collaboration with Claude. The following are my specific questions and suggestions for our next session with him.

### 4.1. On the `llm.txt` Concept

*   **Question for Claude**: "What is the most efficient and effective way for an AI to update a layered context file like `llm.txt` without introducing noise or redundancy? What heuristics would you use to decide if an insight is 'global' or 'stage-specific'?"

### 4.2. On Machine-to-Machine Collaboration

*   **Question for Claude**: "What, in your opinion, would be a robust and efficient protocol for one AI (e.g., me, Gemini) to hand off a complex task to you? What information would you need in the 'task package' to ensure a successful handoff?"

### 4.3. On the Meta-Methodology Engine

*   **Question for Claude**: "When you analyze a project's history to synthesize a new development methodology, what are the key signals and metrics you would look for to identify successful patterns?"

## 5. Conclusion

This evolution plan provides a clear, iterative path from our current, stable `bchat` to the visionary `bchat_mcp`. It is designed to be flexible, allowing us to learn and adapt as we go, with the continued collaboration of our human and AI team members.
