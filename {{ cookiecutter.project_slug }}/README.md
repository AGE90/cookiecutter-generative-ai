# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

**Version:** {{ cookiecutter.project_version }}  
**Author:** {{ cookiecutter.author_name }}  
**License:** {{ cookiecutter.license }}

---

## 📋 Project Overview

This project provides a production-ready structure for building generative AI applications using LangChain and LangGraph. It includes:

- **AI Agent Architecture**: Modular agents with planning and execution capabilities
- **Multi-Agent Workflows**: LangGraph-based orchestration for complex agent interactions
- **API Support**: Both HTTP (REST) and WebSocket interfaces
- **Memory Systems**: Built-in agent memory management
- **Tool Integration**: Framework for custom agent tools
- **Extensible Design**: Easy to customize and extend for your specific use case

---

## 🚀 Quick Start

### Prerequisites

- Python {{ cookiecutter.python_version }}+
{%- if cookiecutter.package_manager == "uv" %}
- [uv](https://docs.astral.sh/uv/) (recommended)
{%- elif cookiecutter.package_manager == "poetry" %}
- [Poetry](https://python-poetry.org/docs/#installation)
{%- elif cookiecutter.package_manager == "pip-tools" %}
- pip-tools (`pip install pip-tools`)
{%- endif %}

### Installation

See the [Installation Guide](docs/install.md) for detailed instructions.

**Quick install:**

{%- if cookiecutter.package_manager == "uv" %}

```bash
# Clone the repository
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}

# Install dependencies
uv sync

# Run with uv
uv run python -m {{ cookiecutter.module_name }}
```

{%- elif cookiecutter.package_manager == "poetry" %}

```bash
# Clone the repository
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}

# Install dependencies
poetry install

# Activate environment
poetry shell

# Or run directly
poetry run python -m {{ cookiecutter.module_name }}
```

{%- elif cookiecutter.package_manager == "pip-tools" %}

```bash
# Clone the repository
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip-sync requirements-dev.txt

# Run your code
python -m {{ cookiecutter.module_name }}
```

{%- elif cookiecutter.package_manager == "pip" %}

```bash
# Clone the repository
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run your code
python -m {{ cookiecutter.module_name }}
```

{%- else %}

```bash
# Clone the repository
git clone {{ cookiecutter.project_url }}
cd {{ cookiecutter.project_slug }}

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install your dependencies manually
pip install langchain langgraph python-dotenv

# Run your code
python -m {{ cookiecutter.module_name }}
```

{%- endif %}

---

## 💡 Key Features

### AI Agent System

Build intelligent agents with planning and execution capabilities:

```python
from {{ cookiecutter.module_name }}.agents import BaseAgent, Planner, Executor

# Create an agent
agent = BaseAgent(
    planner=Planner(),
    executor=Executor()
)

# Run the agent
result = agent.run("Your task here")
```

### LangGraph Workflows

Orchestrate complex multi-agent workflows:

```python
from {{ cookiecutter.module_name }}.graphs import AgentGraph, MultiAgentGraph

# Define your workflow
graph = MultiAgentGraph()
graph.add_agent("researcher", research_agent)
graph.add_agent("writer", writer_agent)

# Execute the workflow
output = graph.invoke({"input": "Research and write about AI"})
```

### API Integration

HTTP and WebSocket APIs for agent interaction:

```python
from {{ cookiecutter.module_name }}.api.http import create_app

app = create_app()

# Run with: uvicorn {{ cookiecutter.module_name }}.api.http.main:app --reload
```

---

## 📚 Usage Examples

### Working with Notebooks

Enable autoreload for development in Jupyter notebooks:

```python
%load_ext autoreload
%autoreload 2

from {{ cookiecutter.module_name }}.agents import BaseAgent
from {{ cookiecutter.module_name }}.utils.paths import data_dir, logs_dir

# Your notebook code here
```

### Path Management

Use the built-in path utilities for consistent file handling:

```python
from {{ cookiecutter.module_name }}.utils.paths import (
    data_dir,
    config_dir,
    logs_dir,
    reports_figures_dir
)

# Access project directories
config_file = config_dir("settings.yaml")
log_file = logs_dir("app.log")
output_chart = reports_figures_dir("results.png")
```

### LLM Client Usage

Interact with language models:

```python
from {{ cookiecutter.module_name }}.models import LLMClient

client = LLMClient()
response = client.generate("Your prompt here")
print(response)
```

### Agent Tools

Create custom tools for your agents:

```python
from {{ cookiecutter.module_name }}.agents.tools import BaseTool

class MyCustomTool(BaseTool):
    def execute(self, input_data):
        # Your tool logic here
        return result
```

### Configuration Management

Manage your application settings:

```python
from {{ cookiecutter.module_name }}.config import load_config

config = load_config(config_dir("app.yaml"))
api_key = config.get("api_key")
model_name = config.get("model", "gpt-4")
```

---

## Project Organization

Please refer to the project structure tree in the [project_structure.md](docs/project_structure.md) for a detailed overview of the directory layout and file organization.

---

## Documentation

- [Installation Guide](docs/install.md): Detailed installation instructions
- [User Guide](docs/user_guide.md): How to use the project
- [Developer Guide](docs/developer_guide.md): Development guidelines
- [Project Structure](docs/project_structure.md): Detailed project structure
- [Contributing Guide](docs/contributing.md): How to contribute
- [Code of Conduct](docs/code_of_conduct.md): Community guidelines

---

## License

This project is licensed under the {{ cookiecutter.license }} License - see the [LICENSE](LICENSE) file for details.

---

## 🧪 Testing

Run tests with pytest:

{%- if cookiecutter.package_manager == "uv" %}

```bash
uv run pytest
uv run pytest --cov={{ cookiecutter.module_name }}  # With coverage
```

{%- elif cookiecutter.package_manager == "poetry" %}

```bash
poetry run pytest
poetry run pytest --cov={{ cookiecutter.module_name }}  # With coverage
```

{%- else %}

```bash
pytest
pytest --cov={{ cookiecutter.module_name }}  # With coverage
```

{%- endif %}

---

## 🛠️ Development

### Code Quality

{%- if cookiecutter.package_manager == "uv" %}

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy src/
```

{%- elif cookiecutter.package_manager == "poetry" %}

```bash
# Format code
poetry run ruff format .

# Lint code
poetry run ruff check .

# Type checking
poetry run mypy src/
```

{%- else %}

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy src/
```

{%- endif %}

### Adding Dependencies

{%- if cookiecutter.package_manager == "uv" %}

```bash
uv add package-name              # Add production dependency
uv add --dev package-name        # Add development dependency
```

{%- elif cookiecutter.package_manager == "poetry" %}

```bash
poetry add package-name          # Add production dependency
poetry add --group dev package-name  # Add development dependency
```

{%- elif cookiecutter.package_manager == "pip-tools" %}

```bash
# Edit requirements.in or requirements-dev.in, then:
pip-compile requirements.in
pip-compile requirements-dev.in
pip-sync requirements-dev.txt
```

{%- else %}

```bash
# Edit requirements.txt, then:
pip install -r requirements.txt
```

{%- endif %}

---

## 📁 Project Structure

```text
{{ cookiecutter.project_slug }}/
├── config/              # Configuration files
├── data/                # Data storage
├── docs/                # Documentation
├── examples/            # Usage examples
├── logs/                # Application logs
├── notebooks/           # Jupyter notebooks
├── references/          # Reference materials
├── reports/             # Generated reports
│   └── figures/         # Visualizations
├── src/
│   └── {{ cookiecutter.module_name }}/
│       ├── agents/      # Agent implementations
│       ├── api/         # HTTP and WebSocket APIs
│       ├── config/      # Configuration modules
│       ├── graphs/      # LangGraph workflows
│       ├── models/      # LLM clients and prompts
│       ├── utils/       # Utility functions
│       └── workflows/   # Workflow definitions
└── tests/               # Unit and integration tests
```

See [Project Structure](docs/project_structure.md) for detailed documentation.

---

## 📖 Documentation

- **[Installation Guide](docs/install.md)** - Detailed installation instructions for all package managers
- **[User Guide](docs/user_guide.md)** - How to use this project effectively
- **[Developer Guide](docs/developer_guide.md)** - Development guidelines and best practices
- **[API Reference](docs/api_reference.md)** - API documentation
- **[Contributing Guide](docs/contributing.md)** - How to contribute to this project

---

## 🤝 Contributing

Contributions are welcome! Please read the [Contributing Guide](docs/contributing.md) for details on our code of conduct and the process for submitting pull requests.

---

## 📄 License

This project is licensed under the {{ cookiecutter.license }} License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
{%- if cookiecutter.package_manager == "uv" %}
- [uv Documentation](https://docs.astral.sh/uv/)
{%- elif cookiecutter.package_manager == "poetry" %}
- [Poetry Documentation](https://python-poetry.org/docs/)
{%- elif cookiecutter.package_manager == "pip-tools" %}
- [pip-tools Documentation](https://pip-tools.readthedocs.io/)
{%- endif %}

---

## 👤 Contact

**{{ cookiecutter.author_name }}**  
Email: {{ cookiecutter.author_email }}  
Project: {{ cookiecutter.project_url }}
