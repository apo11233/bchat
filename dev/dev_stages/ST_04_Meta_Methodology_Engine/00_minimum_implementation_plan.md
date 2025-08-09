# Minimum Implementation Plan: The Meta-Methodology Engine

**Date**: 2025-08-09
**Stage**: ST_04 (Meta-Methodology Engine)
**Author**: Gemini Assistant
**Status**: VISIONARY

## 1. Vision

To evolve `bchat` from a project-specific context tool into a "Meta-Methodology Engine" that can analyze the development process of a project and synthesize a reusable, AI-powered development methodology.

## 2. Core Components

This feature will require several new, high-level components.

### 2.1. The `ProjectAnalyzer`

*   **Purpose**: To analyze the complete `dev_stages` and `data/chats` history of a project.
*   **Functionality**:
    *   Parses all proposal documents, design documents, and summaries.
    *   Analyzes the sequence and duration of development stages.
    *   Identifies patterns in bug fixes and refactoring efforts.
    *   Correlates chat conversations with specific development tasks.
*   **Output**: A structured representation of the project's "development DNA".

### 2.2. The `MethodologySynthesizer`

*   **Purpose**: To take the output of the `ProjectAnalyzer` and synthesize a generic, reusable development methodology.
*   **Functionality**:
    *   Uses a powerful AI model (like Gemini or Claude) to perform a meta-analysis of the project's "DNA".
    *   Identifies best practices and successful patterns.
    *   Generates a set of `dev_directives` documents that capture the new methodology.
*   **Output**: A new, clean `dev_directives` folder.

### 2.3. The `ProcessGuardian` (Future)

*   **Purpose**: To act as an interactive assistant that helps development teams follow the generated methodology.
*   **Functionality**:
    *   Integrates with the user's shell or IDE.
    *   Provides real-time feedback and suggestions based on the methodology.
    *   (e.g., "It looks like you're starting a new feature. The methodology suggests creating a proposal document first. Would you like me to create one for you?")

## 3. Minimum Implementation Plan

This is a long-term vision. The minimum implementation will focus on the first two components.

1.  **Phase 1: The `ProjectAnalyzer`**:
    *   Develop the core logic for parsing and analyzing the full history of a `bchat`-enabled project.
    *   Focus on extracting a structured representation of the development journey.
    *   Test this component on our current project as the first use case.

2.  **Phase 2: The `MethodologySynthesizer`**:
    *   Develop the prompts and AI integration needed to synthesize a new methodology from the `ProjectAnalyzer`'s output.
    *   Implement the functionality to generate a new `dev_directives` folder.

3.  **Phase 3: The `ProcessGuardian`**:
    *   This is a future, state-of-the-art goal that will be tackled after the first two phases are complete and stable.

## 4. Next Steps

This document captures the long-term vision for this feature. The immediate focus remains on completing Phases 1, 2, and 3 of the "Deep Context Engine". This "Meta-Methodology Engine" represents a potential Phase 4 or 5.
