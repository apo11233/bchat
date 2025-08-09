# Gemini Bchat MVP

This MVP demonstrates the proposed new architecture for `bchat`, where it reads a chat file directly and sends it for summarization.

## How to Run

1.  **Ensure you have an API key** in the `.env` file at the root of the `bchat` project.
2.  **Navigate to this directory** (`dev_stages/ST_04/gemini_bchat`).
3.  **Run the script**:
    ```bash
    python3 main.py
    ```

The script will read the `dummy_chat.txt` file, send its content to the Gemini API for summarization, and print the resulting summary.
