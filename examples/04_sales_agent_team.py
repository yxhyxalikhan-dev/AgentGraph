"""
04_sales_agent_team.py - Multi-Agent Sales Pipeline
Simulates a collaborative multi-agent architecture for automated lead enrichment, qualification,
scoring, and account executive routing.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


class LeadState(TypedDict):
    company_name: str
    employee_count: int
    annual_budget: float
    industry: str
    lead_score: int
    qualification_status: str
    recommended_action: str


def enrichment_agent(state: LeadState) -> dict:
    """Agent 1: Enriches prospect profile with company intelligence."""
    print(f"\n[Enrichment Agent] Scanning company intelligence for: {state['company_name']}")
    return {"industry": state.get("industry") or "Technology & AI"}


def qualification_agent(state: LeadState) -> dict:
    """Agent 2: Scores lead viability using BANT methodology."""
    score = 0
    if state["employee_count"] > 100:
        score += 35
    elif state["employee_count"] > 20:
        score += 20
    else:
        score += 10

    if state["annual_budget"] >= 50000:
        score += 45
    elif state["annual_budget"] >= 15000:
        score += 25
    else:
        score += 10

    if state["industry"] == "Technology & AI":
        score += 20

    status = "QUALIFIED" if score >= 60 else "NURTURE"
    print(f"[Qualification Agent] Lead Score: {score}/100 | Status: {status}")
    return {"lead_score": score, "qualification_status": status}


def routing_decision(state: LeadState) -> Literal["enterprise_ae_node", "automated_nurture_node"]:
    if state["qualification_status"] == "QUALIFIED":
        return "enterprise_ae_node"
    return "automated_nurture_node"


def enterprise_ae_agent(state: LeadState) -> dict:
    action = f"Book priority Executive Briefing with Senior AE for {state['company_name']} (Score: {state['lead_score']})."
    return {"recommended_action": action}


def automated_nurture_agent(state: LeadState) -> dict:
    action = f"Enroll {state['company_name']} into personalized 5-stage educational email sequence."
    return {"recommended_action": action}


def main():
    builder = StateGraph(LeadState)

    builder.add_node("enricher", enrichment_agent)
    builder.add_node("qualifier", qualification_agent)
    builder.add_node("enterprise_ae_node", enterprise_ae_agent)
    builder.add_node("automated_nurture_node", automated_nurture_agent)

    builder.add_edge(START, "enricher")
    builder.add_edge("enricher", "qualifier")
    builder.add_conditional_edges(
        "qualifier",
        routing_decision,
        {
            "enterprise_ae_node": "enterprise_ae_node",
            "automated_nurture_node": "automated_nurture_node"
        }
    )
    builder.add_edge("enterprise_ae_node", END)
    builder.add_edge("automated_nurture_node", END)

    pipeline = builder.compile()

    leads = [
        {"company_name": "Apex Cloud Systems", "employee_count": 250, "annual_budget": 85000.0, "industry": "Technology & AI"},
        {"company_name": "Corner Bakery Co.", "employee_count": 8, "annual_budget": 3000.0, "industry": "Food & Beverage"}
    ]

    print("=== Multi-Agent Sales Pipeline in AgentGraph ===")
    for lead in leads:
        result = pipeline.invoke(lead)
        print(f"-> Target: {result['company_name']}")
        print(f"-> Action: {result['recommended_action']}")


if __name__ == "__main__":
    main()
