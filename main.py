import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import system_prompt, model_name

# Schemas
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


# Functions 
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Error handeling if apikey is wrong or broken
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
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

# Declerations for ai use of comands/rules
available_functions = types.Tool(
    function_declarations=[# Extra schemas go inside  this braket 
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,        
    ]
)

# Directory checking and rules
WORKING_DIR = "."
DISPATCH = {# Extra file functions in this curly braket
    "get_files_info": lambda args: get_files_info(WORKING_DIR, args.get("directory", ".")),
    "get_file_content": lambda args: get_file_content(WORKING_DIR, args["file_path"]),
    "write_file": lambda args: write_file(WORKING_DIR, args["file_path"], args["content"]),
    "run_python_file": lambda args: run_python_file(WORKING_DIR, args["file_path"]),
}

# Generates content using Gemini api and display tokens used
def main():
    messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
        
)
    
    usage_metadata = response.usage_metadata
    prompt_tokens = usage_metadata.prompt_token_count
    response_tokens = usage_metadata.candidates_token_count
    calls = getattr(response, "function_calls", []) or []

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
            print(f"User prompt: {response.text}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            return

    if calls:
        for call in calls:
            if call.args == []:
                print(f"Calling function: {call.name}")
            print(f"Calling function: {call.name}({call.args})")
            handler = DISPATCH.get(call.name)
            if handler:
                _ = handler(call.args)
    else:
        print(response.text)


if __name__ == "__main__":
    main()
