"""
The agent: a LangGraph loop that calls the model, runs any tools it asks for,
and repeats until the model answers.

    START -> agent -> (tool calls?) -> tools -> agent -> ... -> END
"""

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from {{ cookiecutter.module_name }}.tools import TOOLS

SYSTEM_PROMPT = "You are a helpful assistant. Use the available tools when they help."

Agent = CompiledStateGraph[Any, Any, Any, Any]


def build_graph(llm: BaseChatModel) -> Agent:
    """
    Build the agent graph.

    Parameters
    ----------
    llm : langchain_core.language_models.BaseChatModel
        Chat model that supports tool calling.

    Returns
    -------
    Agent
        Compiled graph; call `.invoke({"messages": [...]})`.
    """
    model = llm.bind_tools(TOOLS)

    def agent(state: MessagesState) -> dict[str, list[BaseMessage]]:
        messages = [SystemMessage(SYSTEM_PROMPT), *state["messages"]]
        return {"messages": [model.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    return graph.compile()


def ask(graph: Agent, question: str) -> str:
    """
    Run the agent on a single question and return its final answer.

    Parameters
    ----------
    graph : Agent
        Graph from `build_graph`.
    question : str
        User message.

    Returns
    -------
    str
        Text of the last message.
    """
    result = graph.invoke({"messages": [HumanMessage(question)]})
    return str(result["messages"][-1].text)
