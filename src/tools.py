import os
import re
import subprocess

# A tool is three things: a name, a description the model reads, and a function
# that does the work. The definitions below are exactly the shape the API wants.
tool_definitions = [
    {
        "name": "read_file",
        "description": "Read the contents of a file. Returns the file content with line numbers.",
        "input_schema": {
            "type": "object",
            "properties": {"file_path": {"type": "string", "description": "The path to the file to read"}},
            "required": ["file_path"],
        },
    },
]


# Dispatch a tool call by name. Unknown names return an error string instead of
# raising, so a hallucinated tool name lets the model self-correct.
#region dispatch
def execute_tool(name: str, inp: dict) -> str:
    if name == "read_file":
        return _read_file(inp)
    return f"Unknown tool: {name}"
#endregion


#region read_file
def _read_file(inp: dict) -> str:
    try:
        lines = open(inp["file_path"], encoding="utf-8").read().split("\n")
        return "\n".join(f"{i + 1:4d} | {line}" for i, line in enumerate(lines))
    except Exception as e:
        return f"Error reading file: {e}"
#endregion


