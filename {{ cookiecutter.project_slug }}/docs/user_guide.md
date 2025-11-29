# User Guide

Welcome to the {{ cookiecutter.project_name }} user guide. This document will help you get started and make the most of this AI agent framework.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Core Concepts](#core-concepts)
3. [Building Your First Agent](#building-your-first-agent)
4. [Working with LangGraph](#working-with-langgraph)
5. [Using the API](#using-the-api)
6. [Configuration](#configuration)
7. [Data Management](#data-management)
8. [Logging and Debugging](#logging-and-debugging)
9. [Best Practices](#best-practices)
10. [Common Patterns](#common-patterns)

---

## Getting Started

### Prerequisites

Before you begin, ensure you have completed the [installation](install.md) and have:

- Python {{ cookiecutter.python_version }}+ installed
- All dependencies installed
- API keys configured (if using external LLM services)

### Environment Setup

1. **Copy the environment template:**

   ```bash
   cp .env.example .env
   ```

2. **Add your API keys:**

   ```bash
   # .env file
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Verify setup:**

   ```python
   from {{ cookiecutter.module_name }}.config import load_config
   config = load_config()
   print("Configuration loaded successfully!")
   ```

---

## Core Concepts

### Project Architecture

{{ cookiecutter.project_name }} is built around several key concepts:

#### 1. **Agents**

Autonomous entities that can plan, execute tasks, and use tools to accomplish goals.

#### 2. **Planners**

Components that break down complex tasks into manageable steps.

#### 3. **Executors**

Components that carry out the planned steps using available tools.

#### 4. **Tools**

Reusable functions that agents can call to interact with external systems or perform specific actions.

#### 5. **Memory**

Systems for storing and retrieving conversation history and context.

#### 6. **Graphs**

LangGraph-based workflows that define how agents interact and process information.

---

## Building Your First Agent

### Basic Agent

Create a simple agent:

```python
from {{ cookiecutter.module_name }}.agents import BaseAgent
from {{ cookiecutter.module_name }}.models import LLMClient

# Initialize LLM client
llm = LLMClient(model="gpt-4", temperature=0.7)

# Create agent
agent = BaseAgent(
    name="assistant",
    llm=llm,
    system_prompt="You are a helpful AI assistant."
)

# Run the agent
response = agent.run("What is the capital of France?")
print(response)
```

### Agent with Tools

Add tools to your agent:

```python
from {{ cookiecutter.module_name }}.agents import BaseAgent
from {{ cookiecutter.module_name }}.agents.tools import BaseTool

class CalculatorTool(BaseTool):
    """A simple calculator tool."""
    
    name = "calculator"
    description = "Performs basic arithmetic operations"
    
    def execute(self, expression: str) -> str:
        try:
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

# Create agent with tools
agent = BaseAgent(
    name="math_assistant",
    llm=llm,
    tools=[CalculatorTool()],
    system_prompt="You are a math assistant. Use the calculator tool when needed."
)

response = agent.run("What is 25 * 47?")
print(response)
```

### Agent with Memory

Enable conversation memory:

```python
from {{ cookiecutter.module_name }}.agents import BaseAgent
from {{ cookiecutter.module_name }}.agents.memory import ConversationMemory

# Create agent with memory
memory = ConversationMemory(max_tokens=2000)
agent = BaseAgent(
    name="conversational_assistant",
    llm=llm,
    memory=memory
)

# Have a conversation
agent.run("My name is Alice.")
agent.run("What's my name?")  # Agent will remember
```

---

## Working with LangGraph

### Simple Workflow

Create a basic LangGraph workflow:

```python
from {{ cookiecutter.module_name }}.graphs import AgentGraph
from {{ cookiecutter.module_name }}.graphs.state_definitions import AgentState

# Define your workflow
def create_research_workflow():
    graph = AgentGraph()
    
    # Add nodes
    graph.add_node("research", research_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("summarize", summarize_node)
    
    # Add edges
    graph.add_edge("research", "analyze")
    graph.add_edge("analyze", "summarize")
    
    # Set entry and exit points
    graph.set_entry_point("research")
    graph.set_finish_point("summarize")
    
    return graph.compile()

# Use the workflow
workflow = create_research_workflow()
result = workflow.invoke({"query": "AI trends in 2025"})
```

### Multi-Agent Workflow

Coordinate multiple agents:

```python
from {{ cookiecutter.module_name }}.graphs import MultiAgentGraph
from {{ cookiecutter.module_name }}.agents import BaseAgent

# Create specialized agents
researcher = BaseAgent(name="researcher", llm=llm)
writer = BaseAgent(name="writer", llm=llm)
editor = BaseAgent(name="editor", llm=llm)

# Build multi-agent graph
graph = MultiAgentGraph()
graph.add_agent("research", researcher)
graph.add_agent("write", writer)
graph.add_agent("edit", editor)

# Define workflow
graph.add_edge("research", "write")
graph.add_edge("write", "edit")

# Execute
compiled_graph = graph.compile()
result = compiled_graph.invoke({
    "input": "Write an article about quantum computing"
})
```

### Conditional Routing

Add decision logic to your workflow:

```python
def should_continue(state: AgentState) -> str:
    """Decide next step based on state."""
    if state.get("needs_review"):
        return "review"
    return "complete"

graph.add_conditional_edges(
    "process",
    should_continue,
    {
        "review": "review_node",
        "complete": "end"
    }
)
```

---

## Using the API

### HTTP API

Start the HTTP server:

```bash
{%- if cookiecutter.package_manager == "uv" %}
uv run uvicorn {{ cookiecutter.module_name }}.api.http.main:app --reload
{%- elif cookiecutter.package_manager == "poetry" %}
poetry run uvicorn {{ cookiecutter.module_name }}.api.http.main:app --reload
{%- else %}
uvicorn {{ cookiecutter.module_name }}.api.http.main:app --reload
{%- endif %}
```

Make requests:

```python
import requests

# Send a query
response = requests.post(
    "http://localhost:8000/api/v1/agent/query",
    json={"message": "Hello, agent!"}
)
print(response.json())
```

### WebSocket API

Connect via WebSocket for real-time interaction:

```python
import asyncio
import websockets

async def chat():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        # Send message
        await websocket.send("Hello, agent!")
        
        # Receive response
        response = await websocket.recv()
        print(f"Agent: {response}")

asyncio.run(chat())
```

---

## Configuration

### Configuration Files

Store settings in YAML or JSON:

```yaml
# config/app.yaml
llm:
  model: gpt-4
  temperature: 0.7
  max_tokens: 2000

agent:
  system_prompt: "You are a helpful assistant."
  max_iterations: 10

api:
  host: 0.0.0.0
  port: 8000
  cors_origins:
    - http://localhost:3000
```

Load configuration:

```python
from {{ cookiecutter.module_name }}.utils.paths import config_dir
import yaml

with open(config_dir("app.yaml")) as f:
    config = yaml.safe_load(f)

model = config["llm"]["model"]
```

### Environment Variables

Use environment variables for sensitive data:

```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

---

## Data Management

### Using Path Utilities

The project includes utilities for consistent path handling:

```python
from {{ cookiecutter.module_name }}.utils.paths import (
    data_dir,
    config_dir,
    logs_dir,
    reports_figures_dir
)

# Save data
import pandas as pd
df = pd.DataFrame({"col": [1, 2, 3]})
df.to_csv(data_dir("output.csv"), index=False)

# Load data
df = pd.read_csv(data_dir("input.csv"))

# Save reports
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.savefig(reports_figures_dir("chart.png"))
```

### Data Organization

Follow this structure:

```text
data/
├── raw/           # Original, immutable data
├── interim/       # Intermediate transformed data
├── processed/     # Final, canonical data sets
└── external/      # Data from external sources
```

---

## Logging and Debugging

### Setting Up Logging

Configure logging:

```python
import logging
from {{ cookiecutter.module_name }}.utils.paths import logs_dir

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_dir("app.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

### Debugging Agents

Enable verbose output:

```python
agent = BaseAgent(
    name="debug_agent",
    llm=llm,
    verbose=True,  # Print all interactions
    debug=True     # Enable debug mode
)
```

### Tracing with LangSmith

Enable LangSmith tracing:

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "{{ cookiecutter.project_slug }}"
```

---

## Best Practices

### 1. Error Handling

Always handle errors gracefully:

```python
try:
    result = agent.run(user_input)
except Exception as e:
    logger.error(f"Agent error: {e}")
    result = "I apologize, but I encountered an error."
```

### 2. Prompt Engineering

Create effective prompts:

```python
system_prompt = """
You are a {role} with expertise in {domain}.

Your responsibilities:
1. {responsibility_1}
2. {responsibility_2}

Guidelines:
- Be concise and accurate
- Cite sources when possible
- Ask for clarification if needed
"""
```

### 3. Token Management

Monitor token usage:

```python
from {{ cookiecutter.module_name }}.models import count_tokens

text = "Your text here"
tokens = count_tokens(text)
if tokens > 8000:
    text = text[:8000]  # Truncate
```

### 4. Caching

Cache expensive operations:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(input_data):
    # Your expensive operation
    return result
```

---

## Common Patterns

### Pattern 1: Research Agent

```python
def create_research_agent():
    tools = [
        SearchTool(),
        WebScraperTool(),
        SummarizerTool()
    ]
    
    return BaseAgent(
        name="researcher",
        llm=llm,
        tools=tools,
        system_prompt="Research topics thoroughly and provide citations."
    )
```

### Pattern 2: Data Analysis Agent

```python
def create_analyst_agent():
    tools = [
        PandasTool(),
        VisualizationTool(),
        StatisticsTool()
    ]
    
    return BaseAgent(
        name="analyst",
        llm=llm,
        tools=tools,
        system_prompt="Analyze data and create visualizations."
    )
```

### Pattern 3: Multi-Step Workflow

```python
def create_content_pipeline():
    # Research -> Outline -> Write -> Edit
    graph = MultiAgentGraph()
    
    graph.add_agent("research", research_agent)
    graph.add_agent("outline", outline_agent)
    graph.add_agent("write", writing_agent)
    graph.add_agent("edit", editing_agent)
    
    graph.add_sequential_edges([
        "research", "outline", "write", "edit"
    ])
    
    return graph.compile()
```

---

## Troubleshooting

### Common Issues

**Issue: Agent not responding**

- Check API keys are set correctly
- Verify network connectivity
- Check rate limits

**Issue: Out of context window**

- Reduce conversation history
- Summarize previous messages
- Use a model with larger context

**Issue: Tool execution failing**

- Verify tool inputs
- Check tool permissions
- Enable debug mode

### Getting Help

- Check the [FAQ](faq.md)
- Review [examples](../examples/)
- Open an issue on GitHub
- Email: {{ cookiecutter.author_email }}

---

## Next Steps

- Explore the [Developer Guide](developer_guide.md) for advanced topics
- Check out the [API Reference](api_reference.md)
- Review [example projects](../examples/)
- Join our community discussions

---

*Last updated: {{ cookiecutter.project_version }}*
