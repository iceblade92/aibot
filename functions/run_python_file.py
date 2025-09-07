import os
import sys
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=f"Runs a python file at selected path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Second description witch i dont know why it needs so this is a test string.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    fullpath = os.path.join(working_directory, file_path)
    abs_file = os.path.abspath(fullpath)
    abs_workdir = os.path.abspath(working_directory)

    try:
        if not abs_file.startswith(abs_workdir + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file):
            return f'Error: File "{file_path}" not found.'
        if not abs_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        cp = subprocess.run(
            [sys.executable, abs_file, *args],
            cwd=abs_workdir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        out = []
        if cp.stdout:
            out.append(f"STDOUT:\n{cp.stdout}".rstrip())
        if cp.stderr:
            out.append(f"STDERR:\n{cp.stderr}".rstrip())
        if cp.returncode != 0:
            out.append(f"Process exited with code {cp.returncode}")
        return "\n".join(out) if out else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"