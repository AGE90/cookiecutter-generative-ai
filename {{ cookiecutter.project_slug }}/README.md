# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

<!-- Add a brief overview of the project here. -->

A tool-calling agent built with [LangGraph](https://langchain-ai.github.io/langgraph/), served over HTTP with [FastAPI](https://fastapi.tiangolo.com/).

---

## Installation

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/). uv installs Python {{ cookiecutter.python_version }} for you if it is missing.

```bash
git clone <repository-url>
cd {{ cookiecutter.project_slug }}
make install                  # uv sync --all-groups: creates .venv with every dependency group
cp .env.example .env          # if .env doesn't exist yet
uv run pre-commit install     # optional: lint and format on every commit
```

Then configure the model in `.env`:

```bash
LLM_MODEL={{ cookiecutter._default_models[cookiecutter.llm_provider] }}
{%- if cookiecutter._api_key_vars[cookiecutter.llm_provider] %}
{{ cookiecutter._api_key_vars[cookiecutter.llm_provider] }}=<your key>
{%- endif %}
```
{%- if cookiecutter.llm_provider == "ollama" %}

Ollama runs locally: [install it](https://ollama.com/download), then `ollama pull {{ cookiecutter._default_models[cookiecutter.llm_provider].split(":")[1] }}`.
{%- endif %}

`LLM_MODEL` is `"<provider>:<model>"`, passed to LangChain's `init_chat_model`. To switch provider, install its package (e.g. `uv add langchain-openai`) and change `LLM_MODEL` and the API key.

---

## Usage

```bash
make run Q="What time is it?"   # ask the agent from the command line
make serve                      # API on http://127.0.0.1:8000, interactive docs at /docs
```

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What time is it?"}'
# {"answer": "..."}
```

From Python or a notebook:

```python
from {{ cookiecutter.module_name }}.graph import ask, build_graph
from {{ cookiecutter.module_name }}.llm import get_llm

agent = build_graph(get_llm())
print(ask(agent, "What time is it?"))
```

### How it works

`graph.py` builds a LangGraph loop: the model gets the conversation and the tools; if it asks for a tool, `ToolNode` runs it and the result goes back to the model, until it answers.

```text
START -> agent -> (tool calls?) -> tools -> agent -> ... -> END
```

### Adding a tool

Add a function to `tools.py` and list it in `TOOLS`. The docstring is the description the model sees:

```python
@tool
def word_count(text: str) -> int:
    """Count the words in a text."""
    return len(text.split())


TOOLS: list[BaseTool] = [current_time, word_count]
```

### Code quality and tests

```bash
make check    # ruff format + ruff check + mypy
make test     # pytest with coverage; offline, using a scripted fake LLM
```

`tests/conftest.py` has a `fake_llm` fixture that replays scripted messages (including tool calls), so tests never call a real model or need an API key.

---

## Project Structure

```text
├── CLAUDE.md               <- Project conventions for Claude Code
├── Makefile                <- Tasks: `make help`
├── pyproject.toml          <- Metadata, dependency groups and tool configuration
├── .env.example            <- Environment variables (copy to .env)
├── config/                 <- Configuration files
├── data/                   <- Data for the agent (documents, datasets)
├── docs/                   <- Developer guide and code of conduct
├── examples/               <- Example scripts
├── logs/                   <- Log files
├── notebooks/              <- Exploration notebooks
├── references/             <- Papers, manuals, notes
├── reports/figures/        <- Generated figures
├── src/{{ cookiecutter.module_name }}/
│   ├── __main__.py         <- CLI: `uv run {{ cookiecutter.project_slug }} "question"`
│   ├── api.py              <- FastAPI app: GET /health, POST /chat
│   ├── config.py           <- Settings from .env
│   ├── graph.py            <- LangGraph agent: build_graph(), ask()
│   ├── llm.py              <- Chat model factory: get_llm()
│   ├── tools.py            <- Tools the agent can call
│   └── utils/paths.py      <- Project-relative path helpers
└── tests/                  <- Offline tests with a fake LLM
```

---

## Documentation

- [Developer Guide](docs/developer_guide.md): code style, testing, Git workflow and contributing
- [Code of Conduct](docs/code_of_conduct.md)
{%- if cookiecutter.license != "No license file" %}

---

## License

This project is licensed under the {{ cookiecutter.license }} License. See the [LICENSE](LICENSE) file for details.
{%- endif %}
