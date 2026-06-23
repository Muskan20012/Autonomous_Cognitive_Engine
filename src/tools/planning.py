from langchain_core.tools import tool
from typing import List

@tool
def write_todos(todos: List[str]) -> str:
    """Call this tool to define a structured list of sub-tasks (TODOs) to achieve the goal."""
    return f"Successfully created {len(todos)} TODOs."
