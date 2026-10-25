"""
02_conditional_routing.py - Conditional Branching in AgentGraph
Demonstrates routing workflows based on state inspection (intent classification).
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


class RouterState(TypedDict):
    ticket_text: str
    category: str
    department_response: str


def classifier_node(state: RouterState) -> dict:
    """Classifies user intent based on ticket text."""
    text = state["ticket_text"].lower()
    if any(k in text for k in ["invoice", "refund", "card", "billing", "payment"]):
        category = "billing"
    elif any(k in text for k in ["api", "error", "bug", "stacktrace", "crash"]):
        category = "technical"
    else:
        category = "general"
    
    print(f"[Classifier] Ticket classified as: {category.upper()}")
    return {"category": category}


def billing_agent(state: RouterState) -> dict:
    return {"department_response": "Billing Agent: Reviewed transaction history; processed requested adjustment."}


def technical_agent(state: RouterState) -> dict:
    return {"department_response": "Technical Agent: Located stack trace; patch dispatched to staging server."}


def general_agent(state: RouterState) -> dict:
    return {"department_response": "Support Agent: Thank you for reaching out; documentation and guides provided."}


def route_decision(state: RouterState) -> Literal["billing_node", "technical_node", "general_node"]:
    """Conditional routing function."""
    cat = state["category"]
    if cat == "billing":
        return "billing_node"
    elif cat == "technical":
        return "technical_node"
    return "general_node"


def main():
    builder = StateGraph(RouterState)

    builder.add_node("classifier", classifier_node)
    builder.add_node("billing_node", billing_agent)
    builder.add_node("technical_node", technical_agent)
    builder.add_node("general_node", general_agent)

    builder.add_edge(START, "classifier")
    builder.add_conditional_edges(
        "classifier",
        route_decision,
        {
            "billing_node": "billing_node",
            "technical_node": "technical_node",
            "general_node": "general_node"
        }
    )
    builder.add_edge("billing_node", END)
    builder.add_edge("technical_node", END)
    builder.add_edge("general_node", END)

    app = builder.compile()

    test_tickets = [
        "Payment failed during checkout with card ending in 4022",
        "Encountered NullPointerException on API endpoint /v1/auth",
        "What are your business operating hours on weekends?"
    ]

    for ticket in test_tickets:
        print(f"\nIncoming Ticket: '{ticket}'")
        res = app.invoke({"ticket_text": ticket})
        print(f"Outcome: {res['department_response']}")


if __name__ == "__main__":
    main()
