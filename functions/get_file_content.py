import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    fullpath = os.path.join(working_directory, file_path)
    abs_file = os.path.abspath(fullpath)
    abs_workdir = os.path.abspath(working_directory)
    
    try:
        if not abs_file.startswith(abs_workdir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(abs_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(abs_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                extra = f.read(1)
                has_more = extra != ""
                if has_more:
                    return f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content_string
    
    
    except Exception as e:
        return f"Error: {str(e)}"