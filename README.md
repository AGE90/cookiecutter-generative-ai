# Cookiecutter Generative AI Project Template

A **Cookiecutter** template to jumpstart generative AI projects: a working tool-calling agent built with **LangGraph**, served with **FastAPI**, tested offline, and managed with **uv**.

---

## Features

- **Working Agent**: A LangGraph loop (model -> tools -> model) with an example tool, ready to extend
- **Any LLM Provider**: Anthropic, OpenAI or a local Ollama model, switchable with one `LLM_MODEL` setting
- **HTTP API and CLI**: FastAPI app (`POST /chat`, interactive docs at `/docs`) and a command-line entry point
- **Offline Tests**: A scripted fake LLM (including tool calls), so tests never need an API key or network
- **Modern Python Development**: [uv](https://docs.astral.sh/uv/) for fast, reproducible dependency management
- **Code Quality**: ruff (lint + format), mypy and pre-commit, passing out of the box
- **Claude Code Skill**: Scaffold a project by asking Claude, in one command, without Claude writing the files ([see below](#claude-code-skill))

---

## Requirements

- **[uv](https://docs.astral.sh/uv/getting-started/installation/)**: runs Cookiecutter (via `uvx`), installs Python and manages the project's dependencies
- **Git** (optional, for version control)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

No separate Cookiecutter install is needed: `uvx cookiecutter ...` runs it in a throwaway environment.

---

## How to Start a New Project

### Interactive

```bash
uvx cookiecutter gh:AGE90/cookiecutter-generative-ai
```

Cookiecutter asks for each option and creates the project. The post-generation hook then pins Python, adds every dependency group with `uv add`, creates `.env` from `.env.example` and initializes Git if selected.

### Non-interactive

Pass the options on the command line and skip the prompts. Any option you leave out uses its default:

```bash
uvx cookiecutter gh:AGE90/cookiecutter-generative-ai --no-input \
  project_name="Support Agent" \
  author_name="Jane Doe" author_email="jane@example.com" \
  llm_provider=openai
```

### Next steps

```bash
cd support-agent
# add your API key to .env, then:
make run Q="What time is it?"   # ask the agent from the command line
make serve                      # API on http://127.0.0.1:8000 (docs at /docs)
make check && make test         # lint, type-check and run the offline tests
```

---

## Claude Code Skill

The repo ships a [Claude Code](https://claude.com/claude-code) skill in [`skill/genai-project/SKILL.md`](skill/genai-project/SKILL.md) that lets Claude create projects from this template.

### How it works

The skill does **not** contain the template files. It tells Claude to work out the options from your request and run the single non-interactive `cookiecutter` command shown above. Cookiecutter writes the files, not Claude, so:

- **Low token cost:** Claude reads one short skill file and runs one command, instead of writing every file.
- **Same result every time:** projects are identical to the ones you'd get by running Cookiecutter yourself.
- **One source of truth:** improving the template improves the skill; there is nothing to keep in sync.

Every generated project also includes a `CLAUDE.md` with the project layout and conventions (where tools go, how the model is configured, offline tests with the fake LLM), so Claude follows them when working inside the project later.

### Install

Link the skill into your personal skills folder, so it updates whenever you `git pull` this repo:

```bash
git clone https://github.com/AGE90/cookiecutter-generative-ai.git
ln -s "$PWD/cookiecutter-generative-ai/skill/genai-project" ~/.claude/skills/genai-project
```

### Use

Start Claude Code in the folder where the project should go and ask for it, e.g.:

> Create an LLM agent project called "Support Agent" that answers customer questions, using Claude.

Or invoke it directly with `/genai-project`. Claude asks only for what it can't infer (usually just the name), takes your author details from `git config`, runs the command and reports the created path. You add the API key to `.env` yourself.

---

## Generated Project Structure

```text
your-project/
├── CLAUDE.md               <- Project conventions for Claude Code
├── LICENSE                 <- Omitted when "No license file" is selected
├── Makefile                <- Tasks: install, run, serve, check, test (`make help`)
├── README.md               <- Install, configuration, usage and structure
├── pyproject.toml          <- Metadata, dependency groups and tool configuration
├── uv.lock                 <- Locked dependency versions (commit it)
├── .python-version         <- Python version pinned by uv
├── .env.example            <- LLM_MODEL and the provider's API key variable
├── .env                    <- Your local copy (git-ignored)
├── .pre-commit-config.yaml <- ruff + mypy hooks
├── config/                 <- Configuration files
├── data/                   <- Data for the agent (documents, datasets)
├── docs/
│   ├── developer_guide.md  <- Architecture, testing, Git workflow and contributing
│   └── code_of_conduct.md
├── examples/               <- Example scripts
├── logs/                   <- Log files
├── notebooks/              <- Exploration notebooks
├── references/             <- Papers, manuals, notes
├── reports/figures/        <- Generated figures
├── src/your_module/
│   ├── __main__.py         <- CLI: `uv run your-project "question"`
│   ├── api.py              <- FastAPI app: GET /health, POST /chat
│   ├── config.py           <- Settings from .env
│   ├── graph.py            <- LangGraph agent: build_graph(), ask()
│   ├── llm.py              <- Chat model factory: get_llm()
│   ├── tools.py            <- Tools the agent can call
│   └── utils/paths.py      <- Project-relative path helpers
└── tests/
    ├── conftest.py         <- `fake_llm` fixture: scripted messages, no network
    ├── test_api.py
    └── test_graph.py
```

---

## Project Setup Options

### Project Name, Slug and Module Name

`project_name` is the human-readable title. `project_slug` (the directory name and CLI command) and `module_name` (the Python package) are derived from it: "Support Agent" becomes `support-agent` and `support_agent`. The slug must be lowercase letters, digits and single hyphens; the module name must be a valid Python identifier.

### Author, Description, URL and Version

`author_name`, `author_email`, `project_description`, `project_url` and `project_version` fill in `pyproject.toml` and the README. The email and URL are validated before anything is generated.

### Python Version

`python_version` is the minimum Python version (`requires-python`), the ruff target version and the version pinned by uv in `.python-version`. It must have the format `3.X` and be at least `3.11`. By default it is set to `3.12`.

### License

One of `MIT`, `Apache-2.0`, `BSD-3-Clause`, `GPL-3.0-or-later`, or `No license file` (no `LICENSE` file and no `license` field in `pyproject.toml`).

### LLM Provider

`llm_provider` picks the LangChain integration package, the default `LLM_MODEL` and the API key variable in `.env.example`:

| Provider | Package | Default `LLM_MODEL` | Key |
|---|---|---|---|
| `anthropic` (default) | `langchain-anthropic` | `anthropic:claude-opus-5` | `ANTHROPIC_API_KEY` |
| `openai` | `langchain-openai` | `openai:gpt-5` | `OPENAI_API_KEY` |
| `ollama` | `langchain-ollama` | `ollama:llama3.2` | none (runs locally) |

The model can be changed at any time by editing `LLM_MODEL` in `.env`.

### Initialize Environment

If `initialize_env` is `yes`, the post-generation hook pins the Python version and adds every dependency group below with `uv add` (creating `.venv` and `uv.lock`). Select `no` to only generate the files; you can run `make install` later.

### Dependencies

| Option | Group | Default |
|---|---|---|
| `project_dependencies` | main | `langchain, langgraph, fastapi, uvicorn[standard], python-dotenv, pyprojroot` (plus the provider package) |
| `extra_dependencies` | main | empty: packages added **on top of** the defaults, e.g. `"langchain-community, chromadb"` |
| `development_dependencies` | `dev` | `mypy, ruff, pre-commit, ipykernel` |
| `testing_dependencies` | `test` | `pytest, pytest-cov, httpx` |

The template code uses every default main dependency, so add packages with `extra_dependencies` rather than replacing `project_dependencies`.

### Initialize Git Repository

If `initialize_git_repository` is `yes`, the hook runs `git init` and commits the generated project.

---

## Contributing

Contributions are welcome! If you'd like to improve this template, feel free to submit a pull request.

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Run the template tests (they render the template with several option combinations and check the output):

    ```bash
    uvx --with cookiecutter pytest tests/
    ```

5. Submit a pull request.

CI also generates real projects for several providers and runs `make check && make test` inside each.

---

## License

This template itself is MIT licensed. Generated projects use the license you select during setup.

---

## Resources

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [uv Documentation](https://docs.astral.sh/uv/)
