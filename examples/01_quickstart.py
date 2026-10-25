"""
01_quickstart.py - Basic AgentGraph Workflow
Demonstrates core StateGraph setup, node definition, edge connection, and compilation.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    query: str
    processed_query: str
    response: str


def input_processor(state: AgentState) -> dict:
    """Node 1: Normalizes and prepares the incoming user query."""
    raw = state["query"].strip()
    return {"processed_query": f"[PROCESSED] {raw}"}


def reasoning_engine(state: AgentState) -> dict:
    """Node 2: Simulates agent reasoning and core logic."""
    processed = state["processed_query"]
    return {"response": f"AgentGraph analyzed '{processed}' and generated targeted response."}


def output_formatter(state: AgentState) -> dict:
    """Node 3: Finalizes output for client consumption."""
    final = f"=== AgentGraph Result ===\n{state['response']}\nStatus: Completed Successfully"
    return {"response": final}


def main():
    # 1. Initialize StateGraph with the state schema
    builder = StateGraph(AgentState)

    # 2. Add nodes
    builder.add_node("processor", input_processor)
    builder.add_node("reasoning", reasoning_engine)
    builder.add_node("formatter", output_formatter)

    # 3. Add edges defining workflow sequence
    builder.add_edge(START, "processor")
    builder.add_edge("processor", "reasoning")
    builder.add_edge("reasoning", "formatter")
    builder.add_edge("formatter", END)

    # 4. Compile into an executable graph
    app = builder.compile()

    # 5. Execute with initial state
    print("Executing Quickstart AgentGraph Workflow...")
    result = app.invoke({"query": "Schedule a product demonstration for enterprise client."})
    print(result["response"])


if __name__ == "__main__":
    main()
