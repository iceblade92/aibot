import os
import sys
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Error handeling if apikey is wrong or broken
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")
    exit()

client = genai.Client(api_key=api_key)

# Error handeling if no argument given to konsole
if len(sys.argv) < 2:
    print("You forgot to add a question with quotes")
    sys.exit(1)

# Generates content using Gemini api and display tokens used
def main():
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=sys.argv[1]
    )
    usage_metadata = response.usage_metadata
    prompt_tokens = usage_metadata.prompt_token_count
    response_tokens = usage_metadata.candidates_token_count
    print(response.text)
    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

if __name__ == "__main__":
    main()
