import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    fullpath = os.path.join(working_directory, directory)
    absolute_path_1 = os.path.abspath(fullpath)
    absolute_path_2 = os.path.abspath(working_directory)

    try:
        if not absolute_path_1.startswith(absolute_path_2):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(fullpath):
            return f'Error: "{directory}" is not a directory'
        else:
            result_lines = []
            for item in os.listdir(fullpath):
                item_path = os.path.join(fullpath, item)
                result_lines.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
            return "\n".join(result_lines)


    except Exception as e:
        return f"Error: {str(e)}"