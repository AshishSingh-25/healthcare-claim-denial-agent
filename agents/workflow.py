"""
agents/workflow.py

v1: Deterministic LangGraph workflow.

START -> lookup_denial -> analyze_claim -> generate_recommendation -> END

This is the stable, tested baseline. See agents/agent_workflow.py for
the v2 tool-calling agent upgrade.
"""

from langgraph.graph import StateGraph, START, END
from agents.state import ClaimState
from tools.policy_tool import lookup_denial_code


def _fallback_analysis(state: ClaimState, denial_info: dict) -> str:
    """Return a useful local result when the inference provider is unavailable."""
    causes = ", ".join(denial_info["possible_causes"])
    return (
        f"The denial is classified as {denial_info['category']}: "
        f"{denial_info['description']} Likely causes to review are {causes}. "
        f"Review the submitted procedure code ({state['procedure_code']}), diagnosis "
        f"code ({state['diagnosis_code']}), and the supporting claim information. "
        "The local reference data cannot determine which specific field caused this denial."
    )


def lookup_denial_node(state: ClaimState):
    """
    Retrieve information about the claim's denial code
    from the local knowledge base.
    """

    denial_code = state["denial_code"]

    denial_info = lookup_denial_code(denial_code)

    return {
        "denial_info": denial_info
    }


def analyze_claim_node(state: ClaimState):
    """
    Analyze the healthcare claim using the claim details
    and retrieved denial-code information.
    """

    denial_info = state["denial_info"]

    if not denial_info or not denial_info.get("found"):
        return {
            "analysis": (
                "The claim could not be analyzed because no reference "
                "information was found for the provided denial code."
            )
        }

    return {
        "analysis": _fallback_analysis(state, denial_info),
        "ai_error": None,
    }


def recommendation_node(state: ClaimState):
    """
    Generate a recommended next action based on the
    claim analysis and denial-code reference information.
    """

    denial_info = state["denial_info"]
    if not denial_info or not denial_info.get("found"):
        return {
            "recommendation": (
                "No recommendation can be generated because "
                "the denial code was not found in the reference knowledge base."
            )
        }

    return {
        "recommendation": denial_info["recommended_action"] or (
            "Review the claim and supporting documentation before resubmission."
        )
    }


# Create a LangGraph workflow using ClaimState
workflow = StateGraph(ClaimState)


# Register the nodes
workflow.add_node("lookup_denial", lookup_denial_node)
workflow.add_node("analyze_claim", analyze_claim_node)
workflow.add_node("generate_recommendation", recommendation_node)


# Define the workflow connections
workflow.add_edge(START, "lookup_denial")

workflow.add_edge(
    "lookup_denial",
    "analyze_claim"
)

workflow.add_edge(
    "analyze_claim",
    "generate_recommendation"
)

workflow.add_edge(
    "generate_recommendation",
    END
)


# Compile the graph into an executable workflow
claim_workflow = workflow.compile()
