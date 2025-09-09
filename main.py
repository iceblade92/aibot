import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import system_prompt, model_name, WORKING_DIR

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

# Declerations for ai functions avalible to it
available_functions = types.Tool(
    function_declarations=[# Extra schemas go inside  this braket 
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,        
    ]
)

# Directory checking and rules
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
    verbose = len(sys.argv) == 3 and sys.argv[2] == "--verbose"

    for i in range(20):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
        )
            if response.text:
                print(response.text)
                break
            for cand in response.candidates:
                messages.append(cand.content)
                for part in cand.content.parts:
                    fc = getattr(part, "function_call", None)
                    if fc:
                        if verbose:
                            print(f"model called: {fc.name} with args {fc.args}")
                        tool_msg = call_function(fc, verbose)
                        messages.append(tool_msg)               
            usage_metadata = response.usage_metadata
            prompt_tokens = usage_metadata.prompt_token_count
            response_tokens = usage_metadata.candidates_token_count

            if verbose:
                    print(f"User prompt: {response.text}")
                    print(f"Prompt tokens: {prompt_tokens}")
                    print(f"Response tokens: {response_tokens}")

        except Exception as e:
            print(f"Error: {str(e)}")
            break


def call_function(function_call_part, verbose=False):
    if function_call_part.name not in DISPATCH:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)

    some_function = DISPATCH[function_call_part.name]
    function_result = some_function(function_call_part.args)

    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
        )
    ],
)

if __name__ == "__main__":
    main()
