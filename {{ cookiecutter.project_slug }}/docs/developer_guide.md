# Developer Guide

How to work on **{{ cookiecutter.project_name }}**. Installation and usage are in the [README](../README.md).

## Setup

```bash
make install                  # all dependency groups into .venv
uv run pre-commit install     # ruff + mypy on every commit
```

Run commands inside the environment with `uv run <command>`. Add dependencies with `uv add <package>`, or `uv add --group dev <package>` / `uv add --group test <package>` for tooling.

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/); lines up to 88 characters.
- Type hints on all public functions; `make typecheck` runs mypy.
- Numpy-style docstrings on modules, classes and functions. A tool's docstring is also its description for the model, so write it for the model.
- `make check` formats (`ruff format`), lints (`ruff check`) and type-checks (`mypy`).

## Architecture

| Module | Responsibility |
|---|---|
| `config.py` | Reads settings (`LLM_MODEL`, API keys) from the environment / `.env` |
| `llm.py` | `get_llm()` builds the chat model with `init_chat_model` |
| `tools.py` | `@tool` functions and the `TOOLS` list |
| `graph.py` | `build_graph(llm)` wires model + tools into a LangGraph loop; `ask()` runs one question |
| `api.py` | FastAPI app; the graph comes from `Depends(get_graph)` so tests can override it |
| `__main__.py` | CLI entry point |

Keep the graph free of I/O and configuration: it takes a model and returns a compiled graph. That keeps it testable with a fake model and reusable from the CLI, the API and notebooks.

## Testing

Tests must run offline and without API keys.

- `tests/conftest.py` provides `fake_llm`, a chat model that replays scripted `AIMessage`s. Script tool calls with `AIMessage("", tool_calls=[{"name": ..., "args": {...}, "id": ...}])` followed by the final answer.
- Test the API by overriding the graph dependency: `app.dependency_overrides[get_graph] = lambda: build_graph(fake_llm)`.
- `make test` runs pytest with coverage; `make test-cov` adds a line-by-line report.

To check behavior against a real model, do it by hand (`make run Q="..."`) or in a separate, opt-in test suite; don't make the default suite depend on the network.

## Git Workflow

- Branch from `main` with a descriptive name (`feature/web-search-tool`, `fix/empty-answer`).
- Keep commits focused; write messages in the imperative ("Add web search tool").
- Before opening a pull request, run `make check && make test`.

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes with tests.
3. Run `make check && make test`.
4. Open a pull request describing the change.

Please follow the [Code of Conduct](code_of_conduct.md).
