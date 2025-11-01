import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        wd_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not full_path.startswith(wd_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
           return f'Error: File "{file_path}" not found.'

        if not file_path.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        cmd = ["python3", full_path] + args

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=wd_path,
            timeout=30
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        output_lines = []

        if stdout:
            output_lines.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_lines.append(f"STDERR:\n{stderr}")
        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")

        if not output_lines:
            return "No output produced."

        return "\n".join(output_lines) 

    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Arguments to pass to the Python file.",
            ),
        },
    ),
)