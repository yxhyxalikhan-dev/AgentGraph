"""
03_persistent_memory.py - Checkpointing & Stateful Memory in AgentGraph
Demonstrates using MemorySaver checkpointing to preserve conversation state across multiple turns.
"""

from typing import Annotated, TypedDict
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


class ConversationState(TypedDict):
    messages: Annotated[list[str], operator.add]


def chat_node(state: ConversationState) -> dict:
    last_msg = state["messages"][-1]
    reply = f"Agent: Acknowledged message '{last_msg}'. Current conversation length: {len(state['messages'])}"
    return {"messages": [reply]}


def main():
    checkpointer = MemorySaver()
    builder = StateGraph(ConversationState)

    builder.add_node("chat", chat_node)
    builder.add_edge(START, "chat")
    builder.add_edge("chat", END)

    app = builder.compile(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "session-yahya-001"}}

    print("=== Multi-Turn Session with Checkpointer (thread_id: session-yahya-001) ===")
    
    # Turn 1
    res1 = app.invoke({"messages": ["Hi, I want to explore AgentGraph features."]}, config=thread_config)
    print("Turn 1 State Messages:")
    for m in res1["messages"]:
        print(f" - {m}")

    # Turn 2 (resuming same thread_id)
    print("\n--- Sending Turn 2 to Same Thread ---")
    res2 = app.invoke({"messages": ["Can it handle cyclic multi-agent loops?"]}, config=thread_config)
    print("Turn 2 State Messages (Retains Turn 1 history):")
    for m in res2["messages"]:
        print(f" - {m}")


if __name__ == "__main__":
    main()
