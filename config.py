WORKING_DIR = "./calculator"
MAX_CHARS = 10000
quote = "I'M JUST A ROBOT"
system_prompt = """
You are a helpful AI coding agent.
Always begin by calling get_files_info on '.'.
Then use get_file_content on files under calculator/pkg/ (especially render.py).
Don’t ask the user for filenames; discover them with tools.
Do not describe your plan; emit function calls. Only output final text when finished.
All paths are relative to the working directory.
"""
model_name = "gemini-2.0-flash-001"