import os
import sys
import json
from pathlib import Path

# Third-party imports
from dotenv import load_dotenv
import google.generativeai as genai

# Add project root to sys.path to allow importing from core
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

# Load environment variables from the project root .env file
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

def create_summarization_prompt(content: str) -> str:
    """Create a prompt for content summarization."""
    return f"""
    Analyze the following chat history. Your task is to generate a structured JSON summary.

    **IMPORTANT**: Your response MUST be a single, valid JSON object and nothing else. Do not include any conversational text, greetings, or explanations before or after the JSON. The entire response should be only the JSON object, enclosed in triple backticks (```json ... ```).

    Content:
    {content}

    Please provide a JSON response with the following structure:
    {{
        "summary": "Brief executive summary of the session",
        "decisions": ["Key decisions made during the session"],
        "errors": ["Errors encountered and their solutions"],
        "configurations": ["Configuration changes or settings modified"],
        "key_topics": ["Main topics discussed"],
        "files_modified": ["Files that were created, modified, or deleted"],
        "commands_executed": ["Important commands or operations performed"]
    }}
    """

def main():
    """Main function for the MVP."""
    # 1. Configure API Key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return

    genai.configure(api_key=api_key)

    # 2. Read the dummy chat file
    try:
        with open("dummy_chat.txt", "r") as f:
            chat_content = f.read()
    except FileNotFoundError:
        print("Error: dummy_chat.txt not found.")
        return

    # 3. Create the prompt
    prompt = create_summarization_prompt(chat_content)

    # 4. Call the Gemini API
    print("Calling Gemini API for summarization...")
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)

        # 5. Print the response
        print("\n--- Gemini API Response ---")
        print(response.text)
        print("---------------------------")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
