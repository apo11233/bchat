# Gemini-Specific Development Guidelines

This document contains specific directives for the Gemini assistant, based on lessons learned during the development of the `bchat` project.

## 1. File Modification Strategy

*   **Directive**: When performing significant modifications to an existing file, Gemini should avoid using the `replace` tool for large, complex changes, as it has proven to be error-prone.
*   **Preferred Method**: The preferred method is the "rename and create new" strategy:
    1.  Rename the existing file (e.g., `file.py` -> `file.py.old`).
    2.  Write the new, modified content to a fresh file with the original name (`file.py`).
*   **Rationale**: This approach is more robust and less prone to state-tracking errors, ensuring a higher likelihood of success.
