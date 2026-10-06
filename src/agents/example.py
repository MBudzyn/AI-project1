"""Minimal LangGraph example that does not call an LLM."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph


class EchoState(TypedDict):
    """State for the example graph."""

    message: str


def echo(state: EchoState) -> dict[str, str]:
    """Return the incoming message unchanged."""
    return {"message": state["message"]}


def build_example_graph() -> CompiledStateGraph:
    """Compile a one-node graph that echoes its input message."""
    graph: StateGraph = StateGraph(EchoState)
    graph.add_node("echo", echo)
    graph.add_edge(START, "echo")
    graph.add_edge("echo", END)
    return graph.compile()
