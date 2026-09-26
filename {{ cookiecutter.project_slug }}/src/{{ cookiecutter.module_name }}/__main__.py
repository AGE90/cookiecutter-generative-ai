"""
Command line entry point: `uv run {{ cookiecutter.project_slug }} "your question"`.
"""

import sys

from {{ cookiecutter.module_name }}.graph import ask, build_graph
from {{ cookiecutter.module_name }}.llm import get_llm


def main() -> None:
    """Ask the agent the question given on the command line."""
    question = " ".join(sys.argv[1:]) or "What time is it?"
    print(ask(build_graph(get_llm()), question))


if __name__ == "__main__":
    main()
