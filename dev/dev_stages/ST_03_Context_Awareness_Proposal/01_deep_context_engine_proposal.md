# Proposal: The Phased Development of the Deep Context Engine

**Date**: 2025-08-09
**Stage**: ST_03 (Context Awareness Proposal)
**Author**: Gemini Assistant
**Status**: PROPOSED

## 1. Vision

To iteratively develop `bchat` into a state-of-the-art, context-aware AI collaboration hub, starting with a simple, robust MVP and progressively adding more advanced capabilities.

## 2. The Phased Roadmap

This project will be developed in three distinct phases, following a "crawl, walk, run" methodology.

### Phase 1: Basic Context Engine (The MVP)

*   **Goal**: To create a simple, working end-to-end system for answering basic contextual questions.
*   **Data Source**: This phase will **only** use the existing `bchat` logs (`chat_index.json` and `chat_log_...json`).
*   **Core Tasks**:
    1.  Fix the existing syntax error in `core/src/chat_monitor.py`.
    2.  Complete the implementation of the `ContextualQueryAnalyzer`, `ChatIndexSearcher`, and `ContextExtractor` to work with the `bchat` logs.
    3.  Ensure the end-to-end flow of a contextual query is working reliably for a single AI provider.
*   **Architectural Consideration**: The `ContextExtractor` will be designed in a modular way to easily accommodate new data sources in the future.

### Phase 2: Advanced Context - Claude's Internal Files

*   **Goal**: To dramatically enhance the context by tapping into the AI's own internal working files.
*   **Data Source**: The `~/.claude/shell-snapshots` and `~/.claude/todos` directories.
*   **Core Tasks**:
    1.  **Investigation**: Analyze the file formats in these new directories.
    2.  **Parsers**: Implement new parser modules for each new data type.
    3.  **Integration**: Enhance the `ContextExtractor` to use these new parsers, adding this new, rich data to the context that is injected into prompts.

### Phase 3: Ultimate Vision - Cross-Provider Deep Context

*   **Goal**: To achieve the ultimate vision of `bchat` as a true multi-AI collaboration hub.
*   **Core Tasks**:
    1.  **Enhanced Search**: Update the `ChatIndexSearcher` to correlate information across different AI providers and the new data sources.
    2.  **Unified Context**: Enhance the `ContextExtractor` to create a single, unified view of a project's history, drawing from all available sources.
    3.  **Advanced Querying**: Enable `bchat` to answer complex, cross-provider questions like, "What was the shell command that Claude ran when we were discussing the Gemini API?"

## 3. Next Steps

This proposal is now ready for review. Upon your approval, I will immediately begin with **Phase 1**: fixing the existing bug and completing the MVP for the Basic Context Engine.
