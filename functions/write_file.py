import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f"Write a new file at selected path with contense.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Second description witch i dont know why it needs so this is a test string.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Second description witch i dont know why it needs so this is a test string.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        fullpath = os.path.join(working_directory, file_path)
        abs_file = os.path.abspath(fullpath)
        abs_workdir = os.path.abspath(working_directory)
        directoryname = os.path.dirname(abs_file)
        if not (abs_file == abs_workdir or abs_file.startswith(abs_workdir + os.sep)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        else:
            if directoryname and not os.path.exists(directoryname):
                os.makedirs(directoryname, exist_ok=True)
            with open(abs_file, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"