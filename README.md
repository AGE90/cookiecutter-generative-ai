# Cookiecutter Generative AI Project Template

A **Cookiecutter** template to jumpstart generative AI projects with a well-organized structure. This template is designed to help data scientists and machine learning engineers create consistent and scalable AI agent projects using modern tools like LangChain and LangGraph.

---

## Features

- **Multiple Package Managers**: Choose between `uv`, `poetry`, `pip-tools`, or `pip` for dependency management
- **Pre-configured for Generative AI**: Includes LangChain, LangGraph, and essential AI libraries
- **AI Agent Architecture**: Ready-to-use structure for building agents with planners, executors, and memory
- **Multi-Agent Graph Support**: Pre-configured templates for complex agent workflows
- **Modular Structure**: Organized directories for data, models, notebooks, APIs, and scripts
- **Testing Framework**: Integrated pytest setup with coverage and mocking
- **Code Quality Tools**: Pre-configured with Ruff, Black, isort, and mypy
- **API Ready**: HTTP and WebSocket API templates included
- **Best Practices**: Follows industry standards for project organization and code management
- **License Options**: Choose from MIT, Apache-2.0, BSD-3-Clause, or GPL-3.0
- **Extensible**: Easily customizable to fit specific project needs

---

## Requirements

- **Python 3.9+**
- **[Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)** >= 2.0.0
- **Package Manager** (optional, chosen during setup):
  - [uv](https://docs.astral.sh/uv/) - Recommended for modern Python projects
  - [Poetry](https://python-poetry.org/) - For traditional dependency management
  - [pip-tools](https://pip-tools.readthedocs.io/) - For requirements.txt workflows
  - pip - Standard Python package installer

---

## Quick Start

### 1. Install Cookiecutter

```bash
pip install cookiecutter
```

### 2. Generate Your Project

```bash
cookiecutter https://github.com/AGE90/cookiecutter-generative-ai.git
```

Or use a local path:

```bash
cookiecutter /path/to/cookiecutter-generative-ai
```

### 3. Answer the Prompts

You'll be asked to provide:

- **project_name**: Your project's display name (e.g., "My AI Agent")
- **project_slug**: URL-friendly name (auto-generated, e.g., "my-ai-agent")
- **module_name**: Python module name (auto-generated, e.g., "my_ai_agent")
- **project_short_description**: One-line project summary
- **author_name**: Your name or organization
- **author_email**: Contact email
- **project_version**: Initial version (default: "0.1.0")
- **project_url**: Project homepage URL
- **python_version**: Python version (default: "3.11")
- **license**: Choose from MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, or none
- **package_manager**: Choose uv, poetry, pip-tools, pip, or none
- **project_dependencies**: Comma-separated list (default includes langchain, langgraph)
- **dev_dependencies**: Development tools (default includes ruff, pytest, mypy)
- **testing_dependencies**: Testing libraries (default includes pytest-cov, pytest-mock)
- **initialize_git_repository**: Create git repo automatically (yes/no)

### 4. Project Setup Complete

The post-generation hook will automatically:

- Create the project structure
- Initialize your chosen package manager
- Install dependencies (if package manager is selected)
- Set up git repository (if selected)
- Generate `pyproject.toml` (for uv/poetry) or `requirements.txt` (for pip-tools/pip)

---

## Generated Project Structure

```text
your-project/
├── .gitignore                          # Python-specific ignores
├── LICENSE                             # Your chosen license
├── README.md                           # Project documentation
├── pyproject.toml                      # Package config (uv/poetry)
├── config/                             # Configuration files
├── data/                               # Data storage
├── docs/                               # Documentation
├── examples/                           # Usage examples
├── logs/                               # Application logs
├── notebooks/                          # Jupyter notebooks
├── references/                         # Reference materials
├── reports/
│   └── figures/                        # Report visualizations
├── src/
│   └── your_module/
│       ├── __init__.py
│       ├── agents/                     # Agent implementations
│       │   ├── base_agent.py
│       │   ├── executor.py
│       │   ├── planner.py
│       │   ├── memory/                 # Agent memory systems
│       │   └── tools/                  # Agent tools
│       ├── api/
│       │   ├── http/                   # REST API
│       │   │   ├── dependencies.py
│       │   │   ├── models/
│       │   │   └── routers/
│       │   └── websocket/              # WebSocket API
│       ├── config/                     # Configuration modules
│       ├── graphs/                     # LangGraph definitions
│       │   ├── agent_graph.py
│       │   ├── multi_agent_graph.py
│       │   └── state_definitions.py
│       ├── models/                     # LLM clients
│       │   ├── llm_client.py
│       │   └── prompts/
│       ├── utils/
│       │   └── paths.py                # Path utilities
│       └── workflows/                  # Workflow definitions
└── tests/                              # Unit tests
```

---

## Package Manager Details

### Using `uv` (Recommended)

```bash
cd your-project
uv sync                                 # Sync dependencies
uv add package-name                     # Add new package
uv add --dev package-name               # Add dev package
uv run python script.py                 # Run with uv
```

### Using `poetry`

```bash
cd your-project
poetry install                          # Install dependencies
poetry add package-name                 # Add new package
poetry add --group dev package-name     # Add dev package
poetry run python script.py             # Run with poetry
```

### Using `pip-tools`

```bash
cd your-project
pip-sync requirements-dev.txt           # Sync environment
# Edit requirements.in, then:
pip-compile requirements.in             # Compile requirements
pip-compile requirements-dev.in         # Compile dev requirements
```

### Using `pip`

```bash
cd your-project
pip install -r requirements.txt         # Install dependencies
```

---

## What Gets Configured Automatically

The template includes intelligent post-generation hooks that:

1. **Validate inputs** (pre-generation):
   - Ensures module names are valid Python identifiers
   - Validates project slug format
   - Checks email and URL formats
   - Verifies Python version compatibility

2. **Set up package management** (post-generation):
   - Creates `pyproject.toml` with your chosen dependencies (uv/poetry)
   - Generates `requirements.in` and compiles to `.txt` (pip-tools)
   - Creates basic `requirements.txt` (pip)
   - Installs all specified dependencies automatically

3. **Initialize version control** (optional):
   - Creates git repository
   - Makes initial commit with all generated files

---

## Customization

### Adding Custom Dependencies

Edit `cookiecutter.json` to change default dependencies:

```json
{
  "project_dependencies": "langchain,langgraph,openai,anthropic",
  "dev_dependencies": "ruff,black,pytest,mypy"
}
```

### Modifying Project Structure

Add or remove directories in `{{ cookiecutter.project_slug }}/` before generating projects.

### Customizing Hooks

Edit `hooks/pre_gen_project.py` or `hooks/post_gen_project.py` to add validation or setup steps.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## License

This template itself is MIT licensed. Generated projects will use the license you select during setup.

---

## Resources

- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Poetry Documentation](https://python-poetry.org/docs/)
