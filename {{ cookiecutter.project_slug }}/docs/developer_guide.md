# Developer Guide

This guide provides information for developers who want to contribute to or extend {{ cookiecutter.project_name }}.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Extending the Framework](#extending-the-framework)
7. [Performance Optimization](#performance-optimization)
8. [Debugging](#debugging)
9. [Release Process](#release-process)

---

## Development Setup

### Initial Setup

1. **Clone and install:**

   ```bash
   git clone {{ cookiecutter.project_url }}
   cd {{ cookiecutter.project_slug }}
   
   {%- if cookiecutter.package_manager == "uv" %}
   uv sync --group dev
   {%- elif cookiecutter.package_manager == "poetry" %}
   poetry install --with dev
   {%- else %}
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements-dev.txt
   {%- endif %}
   ```

2. **Install pre-commit hooks:**

   ```bash
   {%- if cookiecutter.package_manager == "uv" %}
   uv run pre-commit install
   {%- elif cookiecutter.package_manager == "poetry" %}
   poetry run pre-commit install
   {%- else %}
   pre-commit install
   {%- endif %}
   ```

3. **Verify installation:**

   ```bash
   {%- if cookiecutter.package_manager == "uv" %}
   uv run pytest
   {%- elif cookiecutter.package_manager == "poetry" %}
   poetry run pytest
   {%- else %}
   pytest
   {%- endif %}
   ```

### Development Tools

We use the following tools:

- **Ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks for code quality
- **Coverage**: Code coverage reporting

---

## Project Structure

### Directory Layout

```text
{{ cookiecutter.project_slug }}/
├── src/{{ cookiecutter.module_name }}/
│   ├── agents/              # Agent implementations
│   │   ├── base_agent.py    # Base agent class
│   │   ├── executor.py      # Task executor
│   │   ├── planner.py       # Task planner
│   │   ├── memory/          # Memory systems
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # Memory interface
│   │   │   └── conversation.py
│   │   └── tools/           # Agent tools
│   │       ├── __init__.py
│   │       └── base.py      # Tool interface
│   ├── api/                 # API implementations
│   │   ├── http/            # REST API
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py
│   │   │   ├── main.py
│   │   │   ├── models/      # Pydantic models
│   │   │   └── routers/     # API routes
│   │   └── websocket/       # WebSocket API
│   ├── config/              # Configuration modules
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── graphs/              # LangGraph workflows
│   │   ├── __init__.py
│   │   ├── agent_graph.py
│   │   ├── multi_agent_graph.py
│   │   └── state_definitions.py
│   ├── models/              # LLM clients
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   └── prompts/         # Prompt templates
│   ├── utils/               # Utilities
│   │   ├── __init__.py
│   │   └── paths.py
│   └── workflows/           # Workflow definitions
├── tests/                   # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── conftest.py          # Pytest fixtures
├── config/                  # Configuration files
├── docs/                    # Documentation
├── examples/                # Usage examples
└── notebooks/               # Jupyter notebooks
```

### Key Components

#### Base Agent (`agents/base_agent.py`)

The foundation for all agents. Provides:

- LLM integration
- Tool management
- Memory handling
- Execution loop

#### Agent Graph (`graphs/agent_graph.py`)

LangGraph-based workflow orchestration. Handles:

- Node definitions
- Edge connections
- State management
- Conditional routing

#### LLM Client (`models/llm_client.py`)

Unified interface for different LLM providers:

- OpenAI
- Anthropic
- Local models
- Custom implementations

---

## Coding Standards

### Style Guide

Follow [PEP 8](https://pep8.org/) with these specifics:

- **Line length**: 100 characters
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Sorted with isort

### Type Hints

Use type hints for all function signatures:

```python
from typing import Dict, List, Optional, Union

def process_data(
    data: List[Dict[str, str]],
    config: Optional[Dict[str, Union[str, int]]] = None
) -> List[str]:
    """Process data with optional configuration.
    
    Args:
        data: List of data dictionaries
        config: Optional configuration dictionary
        
    Returns:
        List of processed strings
    """
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def create_agent(
    name: str,
    model: str = "gpt-4",
    tools: Optional[List[BaseTool]] = None
) -> BaseAgent:
    """Create a new agent instance.
    
    Args:
        name: Agent name identifier
        model: LLM model to use (default: gpt-4)
        tools: Optional list of tools for the agent
        
    Returns:
        Configured BaseAgent instance
        
    Raises:
        ValueError: If name is empty or model is invalid
        
    Example:
        >>> agent = create_agent("assistant", model="gpt-3.5-turbo")
        >>> response = agent.run("Hello")
    """
    ...
```

### Code Formatting

Format code with Ruff:

```bash
{%- if cookiecutter.package_manager == "uv" %}
uv run ruff format .
uv run ruff check . --fix
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run ruff format .
poetry run ruff check . --fix
{%- else %}
ruff format .
ruff check . --fix
{%- endif %}
```

### Type Checking

Run mypy for static type checking:

```bash
{%- if cookiecutter.package_manager == "uv" %}
uv run mypy src/
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run mypy src/
{%- else %}
mypy src/
{%- endif %}
```

---

## Testing

### Test Structure

```text
tests/
├── unit/                    # Unit tests
│   ├── test_agents.py
│   ├── test_models.py
│   └── test_utils.py
├── integration/             # Integration tests
│   ├── test_api.py
│   └── test_workflows.py
└── conftest.py             # Shared fixtures
```

### Writing Tests

#### Unit Test Example

```python
import pytest
from {{ cookiecutter.module_name }}.agents import BaseAgent

def test_agent_creation():
    """Test creating a basic agent."""
    agent = BaseAgent(name="test")
    assert agent.name == "test"
    assert agent.tools == []

def test_agent_with_tools():
    """Test agent with custom tools."""
    tools = [MockTool()]
    agent = BaseAgent(name="test", tools=tools)
    assert len(agent.tools) == 1

@pytest.mark.asyncio
async def test_agent_async_run():
    """Test asynchronous agent execution."""
    agent = BaseAgent(name="test")
    result = await agent.arun("Hello")
    assert isinstance(result, str)
```

#### Integration Test Example

```python
from fastapi.testclient import TestClient
from {{ cookiecutter.module_name }}.api.http.main import app

client = TestClient(app)

def test_api_health():
    """Test API health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_agent_query():
    """Test agent query endpoint."""
    response = client.post(
        "/api/v1/agent/query",
        json={"message": "Hello"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
```

### Running Tests

```bash
# Run all tests
{%- if cookiecutter.package_manager == "uv" %}
uv run pytest
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run pytest
{%- else %}
pytest
{%- endif %}

# Run with coverage
{%- if cookiecutter.package_manager == "uv" %}
uv run pytest --cov={{ cookiecutter.module_name }} --cov-report=html
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run pytest --cov={{ cookiecutter.module_name }} --cov-report=html
{%- else %}
pytest --cov={{ cookiecutter.module_name }} --cov-report=html
{%- endif %}

# Run specific test file
{%- if cookiecutter.package_manager == "uv" %}
uv run pytest tests/unit/test_agents.py
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run pytest tests/unit/test_agents.py
{%- else %}
pytest tests/unit/test_agents.py
{%- endif %}

# Run tests matching pattern
{%- if cookiecutter.package_manager == "uv" %}
uv run pytest -k "test_agent"
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run pytest -k "test_agent"
{%- else %}
pytest -k "test_agent"
{%- endif %}
```

### Fixtures

Create reusable fixtures in `conftest.py`:

```python
import pytest
from {{ cookiecutter.module_name }}.models import LLMClient
from {{ cookiecutter.module_name }}.agents import BaseAgent

@pytest.fixture
def llm_client():
    """Provide a test LLM client."""
    return LLMClient(model="gpt-3.5-turbo", api_key="test-key")

@pytest.fixture
def test_agent(llm_client):
    """Provide a test agent."""
    return BaseAgent(name="test", llm=llm_client)
```

---

## Documentation

### Building Documentation

If using Sphinx or similar:

```bash
cd docs/
make html
```

### Documentation Standards

- Keep documentation up-to-date with code changes
- Include examples for complex features
- Document all public APIs
- Use diagrams where helpful

### API Documentation

Document all public functions and classes:

```python
class BaseAgent:
    """Base class for all agents.
    
    This class provides the foundation for building AI agents with
    LLM integration, tool usage, and memory management.
    
    Attributes:
        name: Unique identifier for the agent
        llm: Language model client
        tools: List of available tools
        memory: Conversation memory system
        
    Example:
        >>> agent = BaseAgent(name="assistant")
        >>> response = agent.run("Hello!")
        >>> print(response)
    """
```

---

## Extending the Framework

### Creating Custom Agents

```python
from {{ cookiecutter.module_name }}.agents import BaseAgent

class CustomAgent(BaseAgent):
    """Custom agent with specialized behavior."""
    
    def __init__(self, *args, custom_param: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_param = custom_param
    
    def process_input(self, input_text: str) -> str:
        """Custom input processing."""
        # Your custom logic
        return processed_text
```

### Creating Custom Tools

```python
from {{ cookiecutter.module_name }}.agents.tools import BaseTool

class CustomTool(BaseTool):
    """Custom tool for specific functionality."""
    
    name = "custom_tool"
    description = "Does something specific"
    
    def __init__(self, param: str):
        self.param = param
    
    def execute(self, input_data: str) -> str:
        """Execute the tool."""
        # Your tool logic
        return result
```

### Creating Custom Workflows

```python
from {{ cookiecutter.module_name }}.graphs import AgentGraph

def create_custom_workflow():
    """Create a custom multi-step workflow."""
    graph = AgentGraph()
    
    # Define custom nodes
    def custom_node(state):
        # Your custom logic
        return updated_state
    
    # Build graph
    graph.add_node("step1", custom_node)
    graph.add_node("step2", another_node)
    graph.add_edge("step1", "step2")
    
    return graph.compile()
```

---

## Performance Optimization

### Profiling

Profile your code:

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(10)
```

### Caching

Use caching for expensive operations:

```python
from functools import lru_cache
from typing import List

@lru_cache(maxsize=128)
def expensive_computation(input_data: str) -> List[str]:
    """Cached expensive computation."""
    # Your expensive operation
    return result
```

### Async Operations

Use async for I/O-bound operations:

```python
import asyncio
from typing import List

async def process_multiple_queries(queries: List[str]) -> List[str]:
    """Process multiple queries concurrently."""
    tasks = [agent.arun(query) for query in queries]
    results = await asyncio.gather(*tasks)
    return results
```

---

## Debugging

### Debug Mode

Enable debug logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

agent = BaseAgent(name="debug", verbose=True, debug=True)
```

### VS Code Debugging

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["-v"],
            "console": "integratedTerminal"
        }
    ]
}
```

---

## Release Process

### Version Bumping

Update version in:

- `pyproject.toml` or `setup.py`
- `{{ cookiecutter.module_name }}/__init__.py`
- `README.md`

### Creating a Release

1. **Update changelog**
2. **Run all tests**
3. **Tag the release:**

   ```bash
   git tag -a v{{ cookiecutter.project_version }} -m "Release version {{ cookiecutter.project_version }}"
   git push origin v{{ cookiecutter.project_version }}
   ```

### Publishing

For PyPI:

```bash
{%- if cookiecutter.package_manager == "poetry" %}
poetry build
poetry publish
{%- else %}
python -m build
python -m twine upload dist/*
{%- endif %}
```

---

## Additional Resources

- [Contributing Guide](contributing.md)
- [Code of Conduct](code_of_conduct.md)
- [Architecture Documentation](architecture.md)
- [API Reference](api_reference.md)

---

*For questions, contact: {{ cookiecutter.author_email }}*
