"""
HTTP API for the agent. Run with `make serve`, then open http://127.0.0.1:8000/docs.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from {{ cookiecutter.module_name }}.graph import Agent, ask, build_graph
from {{ cookiecutter.module_name }}.llm import get_llm

app = FastAPI(title="{{ cookiecutter.project_name }}")


class ChatRequest(BaseModel):
    """Body of `POST /chat`."""

    message: str


class ChatResponse(BaseModel):
    """Response of `POST /chat`."""

    answer: str


@lru_cache
def get_graph() -> Agent:
    """Build the agent once and reuse it (override in tests)."""
    return build_graph(get_llm())


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok"}


@app.post("/chat")
def chat(
    request: ChatRequest, graph: Annotated[Agent, Depends(get_graph)]
) -> ChatResponse:
    """Send a message to the agent and return its answer."""
    return ChatResponse(answer=ask(graph, request.message))
