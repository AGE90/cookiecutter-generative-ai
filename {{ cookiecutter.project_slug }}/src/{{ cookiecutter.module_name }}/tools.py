"""
Tools the agent can call. Add a function with `@tool` and list it in `TOOLS`.

The docstring is the description the model sees, so make it clear.
"""

from datetime import UTC, datetime

from langchain_core.tools import BaseTool, tool


@tool
def current_time() -> str:
    """Return the current UTC date and time in ISO 8601 format."""
    return datetime.now(UTC).isoformat()


TOOLS: list[BaseTool] = [current_time]
