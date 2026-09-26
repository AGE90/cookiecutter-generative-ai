# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Layout

- `src/{{ cookiecutter.module_name }}/graph.py`: the LangGraph agent (`build_graph`, `ask`). Change the flow here.
- `src/{{ cookiecutter.module_name }}/tools.py`: tools the agent can call. Add `@tool` functions and list them in `TOOLS`; the docstring is the description the model sees.
- `src/{{ cookiecutter.module_name }}/llm.py` + `config.py`: the model comes from `LLM_MODEL` in `.env` (`"<provider>:<model>"`, LangChain `init_chat_model`). Default provider: {{ cookiecutter.llm_provider }}.
- `src/{{ cookiecutter.module_name }}/api.py`: FastAPI app (`GET /health`, `POST /chat`). The graph is injected with `Depends(get_graph)`.
- `src/{{ cookiecutter.module_name }}/__main__.py`: CLI entry point.

## Conventions

- Environment: uv. Run everything with `uv run <cmd>`; add deps with `uv add <pkg>` (or `uv add --group <dev|test> <pkg>`). Never use pip directly.
- Secrets live in `.env` (git-ignored); document new variables in `.env.example`.
- Tests must not call a real LLM: use the `fake_llm` fixture in `tests/conftest.py` (scripted `AIMessage`s, including tool calls) and `app.dependency_overrides[get_graph]` for the API.
- Paths: use `{{ cookiecutter.module_name }}.utils.paths` helpers, never hardcoded paths.
- Docstrings: numpy style. Type hints on public functions.

## Commands

- `make install`: install all dependency groups
- `make run Q="..."`: ask the agent from the command line (needs an API key in `.env`)
- `make serve`: run the API at http://127.0.0.1:8000 (docs at `/docs`)
- `make check`: ruff format + ruff check + mypy
- `make test`: pytest (offline)
- `make help`: list every target
