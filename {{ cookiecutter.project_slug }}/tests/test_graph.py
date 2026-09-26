from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, ToolMessage

from {{ cookiecutter.module_name }}.graph import build_graph


def test_agent_calls_tool_then_answers(fake_llm: BaseChatModel) -> None:
    result = build_graph(fake_llm).invoke(
        {"messages": [HumanMessage("What time is it?")]}
    )

    tool_messages = [m for m in result["messages"] if isinstance(m, ToolMessage)]
    assert [m.name for m in tool_messages] == ["current_time"]
    assert result["messages"][-1].text == "It is noon."
