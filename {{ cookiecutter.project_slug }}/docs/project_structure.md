# Project Structure

```text
{{ cookiecutter.project_slug }}/
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
