import os
from langchain_core.tools import tool

WORKSPACE_DIR = os.path.join(os.getcwd(), "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def _get_path(filename: str) -> str:
    filepath = os.path.join(WORKSPACE_DIR, filename)
    if not os.path.abspath(filepath).startswith(os.path.abspath(WORKSPACE_DIR)):
        raise ValueError("Cannot access paths outside the workspace directory.")
    return filepath

@tool
def read_file(filename: str) -> str:
    """Reads the contents of a file in the virtual file system."""
    try:
        with open(_get_path(filename), 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File {filename} not found."
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def write_file(filename: str, content: str) -> str:
    """Writes content to a file in the virtual file system. Overwrites if exists."""
    try:
        with open(_get_path(filename), 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filename}."
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def edit_file(filename: str, old_string: str, new_string: str) -> str:
    """Replaces old_string with new_string in a file in the virtual file system."""
    try:
        filepath = _get_path(filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_string not in content:
            return f"Error: '{old_string}' not found in {filename}."
        content = content.replace(old_string, new_string)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully edited {filename}."
    except FileNotFoundError:
        return f"Error: File {filename} not found."
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def ls() -> str:
    """Lists all files in the virtual file system."""
    try:
        files = os.listdir(WORKSPACE_DIR)
        if not files:
            return "Workspace is empty."
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"
