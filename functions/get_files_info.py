import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        wd_path = os.path.abspath(working_directory)

        if not full_path.startswith(wd_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        entry = []
        for name in os.listdir(full_path):
            path = os.path.join(full_path, name)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            entry.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(entry)
    except Exception as e:
        return f"Erro: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The directory to list files from, relative to the working directory. "
                    "If not provided, lists files in the working directory itself."
                ),
            ),
        },
    ),
)