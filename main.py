import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import system_prompt, model_name

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")



# Error handeling if apikey is wrong or broken
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")
    exit()

client = genai.Client(api_key=api_key)

# Error handeling if wrong amount of argument(s) given to console
if len(sys.argv) < 2:
    print("You forgot to add a question with quotes")
    sys.exit(1)
elif len(sys.argv) > 3:
    print("Too many arguments given")
    sys.exit(3)

# Generates content using Gemini api and display tokens used
def main():
    messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
)
    usage_metadata = response.usage_metadata
    prompt_tokens = usage_metadata.prompt_token_count
    response_tokens = usage_metadata.candidates_token_count
    if len(sys.argv) == 3:
        if sys.argv[2] == "--verbose":
            print(f"User prompt: {response.text}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
