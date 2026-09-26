from typing import Any

import pytest
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage


class FakeToolCallingLLM(GenericFakeChatModel):
    """Offline stand-in for a chat model: replays scripted messages."""

    def bind_tools(self, tools: Any, **kwargs: Any) -> Any:
        return self


@pytest.fixture
def fake_llm() -> FakeToolCallingLLM:
    """A model that calls `current_time` once, then answers."""
    return FakeToolCallingLLM(
        messages=iter(
            [
                AIMessage(
                    "",
                    tool_calls=[{"name": "current_time", "args": {}, "id": "call_1"}],
                ),
                AIMessage("It is noon."),
            ]
        )
    )
