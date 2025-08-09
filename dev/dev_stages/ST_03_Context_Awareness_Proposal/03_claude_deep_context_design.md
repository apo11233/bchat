# Design: The Claude Deep Context Engine

**Date**: 2025-08-09
**Stage**: ST_03 (Context Awareness Proposal)
**Author**: Gemini Assistant
**Status**: PROPOSED

## 1. Overview

This document outlines the new, correct technical design for parsing Claude's internal context files. It is based on the detailed information in `docs/claude_context_architecture.md` and supersedes all previous designs.

**Collaboration Note**: The AI assistant working on this implementation can request a "deep_research" action from the user. This involves asking the user to have Claude perform a detailed analysis of its own internal files and to provide the results. This is a powerful tool for resolving ambiguities and for getting the most accurate and up-to-date information.

## 2. The New Approach: Official Context Sources

Instead of parsing internal, undocumented files like `shell-snapshots`, we will now focus on the official, stable sources of Claude's context:

1.  **`CLAUDE.md` files**: For persistent instructions and project context.
2.  **Conversation History**: For the direct record of past interactions.

## 3. Parser and Extractor Design

We will create two new parsers and a new extractor method.

### 3.1. `ClaudeMdParser`

*   **Purpose**: To parse the `CLAUDE.md` files.
*   **Functionality**:
    *   Will be able to read a `.md` file and extract key sections (e.g., based on headings).
    *   Will need to handle the `@path/to/file` import syntax, with a recursion limit to prevent infinite loops.
    *   Will need to be able to find and load the full hierarchy of `CLAUDE.md` files (user, project, etc.).

### 3.2. `ConversationHistoryParser`

*   **Purpose**: To parse the chat transcript files from `~/.claude/conversations/`.
*   **Functionality**:
    *   Will need to identify the format of these files (likely JSON or JSONL).
    *   Will extract the user and assistant messages from the transcripts.

### 3.3. `ContextExtractor` Enhancement

The `ContextExtractor` will be updated with a new method:

```python
class ContextExtractor:
    # ... (existing code) ...

    def extract_claude_deep_context(self) -> str:
        """
        Extracts and combines context from CLAUDE.md and conversation history.
        """
        # 1. Find and parse the CLAUDE.md file hierarchy
        # 2. Find and parse the most recent conversation history files
        # 3. Combine the extracted context into a single, formatted string
        pass
```

## 4. Implementation Plan

1.  **Implement `ClaudeMdParser`**: Including the logic for handling imports and the file hierarchy.
2.  **Implement `ConversationHistoryParser`**: After we have analyzed the format of the conversation files.
3.  **Integrate into `ContextExtractor`**: Implement the `extract_claude_deep_context` method.
4.  **Update `ChatProcessor`**: Update the main `ChatProcessor` to use this new, richer context source.

## 5. Next Steps

This design is ready for review. Upon approval, I will begin with the implementation of the `ClaudeMdParser`.
