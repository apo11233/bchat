# Proposal: Context-Aware Prompting Engine

**Date**: 2025-08-09
**Stage**: ST_03 (Context Awareness Proposal)
**Author**: Gemini Assistant
**Status**: PROPOSED

## 1. Vision

To transform `bchat` from a passive logging tool into an active, intelligent assistant that can understand and utilize its own memory to answer contextual questions.

## 2. Feature Overview

The "Context-Aware Prompting" engine will intercept user prompts and, when necessary, automatically inject relevant historical context before sending the prompt to the AI.

### Cross-Provider Collaboration

A key capability of this engine will be to facilitate collaboration between different AI models. `bchat` will act as a shared memory, allowing you to ask one AI about a conversation you had with another.

**Example Cross-Provider Flow:**

1.  **User**: `bchat "what did Claude say about our logging function?"`
2.  **bchat (to Gemini)**:
    ```
    Based on the following context from a past conversation with Claude:
    ... (context from Claude's chat log) ...
    Please answer the user's question: "what did Claude say about our logging function?"
    ```

**Example User Flow:**

1.  **User**: `bchat "what was the final version of our SPL function?"`
2.  **bchat (internally)**:
    *   Searches `chat_index.json` for "SPL function".
    *   Finds relevant past conversations.
    *   Extracts code snippets and key decisions from the corresponding `chat_log_...json` files.
    *   Constructs a new, context-rich prompt.
3.  **bchat (to AI)**:
    ```
    Based on the following context from our previous conversations:
    ... (context) ...
    Please answer the user's question: "what was the final version of our SPL function?"
    ```
4.  **AI**: Provides a highly accurate and context-aware answer.

## 3. Technical Design

This feature will require several new components and modifications to the existing architecture.

### 3.1. The `ContextualQueryAnalyzer`

*   A new Python class responsible for analyzing the user's prompt to determine if it is a contextual query.
*   It will use a combination of keyword matching (e.g., "remember", "recall", "what was", "find") and possibly a small, local NLP model to classify the prompt.
*   **Input**: The user's prompt string.
*   **Output**: A boolean indicating if the prompt is contextual, and a list of extracted keywords to search for.

### 3.2. The `ChatIndexSearcher`

*   A new Python class responsible for searching the `data/chats/chat_index.json` file.
*   It will take the keywords from the `ContextualQueryAnalyzer` and find the most relevant chat log files.
*   It will use a simple scoring mechanism based on keyword matches, date, and relevance score to rank the results.
*   It will also be able to use keywords from the prompt (e.g., "Claude", "Gemini") to filter the search results by `ai_source`, enabling cross-provider queries.
*   **Input**: A list of keywords.
*   **Output**: A ranked list of `chat_log_...json` file paths.

### 3.3. The `ContextExtractor`

*   A new Python class responsible for extracting the relevant information from the chat log files identified by the `ChatIndexSearcher`.
*   It will read the JSON log files and extract the `summary`, `decisions`, `errors`, and `configurations` sections.
*   It will also need to be able to extract the raw conversation content associated with these findings.
*   **Input**: A list of chat log file paths.
*   **Output**: A formatted string containing the compiled context.

### 3.4. Refactoring of `ChatMonitor`

*   The `process_prompt` method will be updated to orchestrate the new workflow:
    1.  Call `ContextualQueryAnalyzer`.
    2.  If the query is contextual:
        *   Call `ChatIndexSearcher`.
        *   Call `ContextExtractor`.
        *   Construct the new, enhanced prompt.
    3.  Call `APIManager` with the final prompt (either the original or the enhanced one).
    4.  The rest of the process (saving the new chat) will remain the same.

## 4. Implementation Plan

This feature will be implemented in the following phases:

1.  **Phase 1: Core Components**:
    *   Implement the `ContextualQueryAnalyzer`, `ChatIndexSearcher`, and `ContextExtractor` classes with basic functionality.
    *   Write unit tests for each component.
2.  **Phase 2: Integration**:
    *   Refactor the `ChatMonitor` class to integrate the new components.
    *   Update the `bchat` command to handle the new contextual query workflow.
3.  **Phase 3: Testing and Refinement**:
    *   Perform end-to-end testing with a variety of contextual prompts.
    *   Refine the keyword extraction and context ranking algorithms.
    *   Update the user documentation.

## 5. Success Criteria

*   `bchat` can successfully answer simple contextual questions about past conversations.
*   The system can correctly identify and extract relevant context from the chat index.
*   The end-to-end workflow is reliable and provides a noticeable improvement in the quality of AI responses for contextual queries.

## 6. Next Steps

This proposal is ready for review. Upon approval, I will begin with the implementation of Phase 1.
