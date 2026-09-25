"""
agents/state.py

Defines the shared state object (ClaimState) that flows through
the LangGraph workflow. Every node reads from and writes to this
state.
"""

from typing import TypedDict, Optional, List, Dict, Any


class ClaimState(TypedDict):
    # --- Input claim fields ---
    claim_id: str
    patient_id: str
    procedure_code: str
    diagnosis_code: str
    payer: str
    claim_amount: float
    denial_code: str

    # --- Fields populated by the workflow ---
    denial_info: Optional[Dict[str, Any]]
    analysis: Optional[str]
    recommendation: Optional[str]
    ai_error: Optional[str]

    # --- Optional fields used by the v2 tool-calling agent workflow ---
    # (safe to ignore for the v1 deterministic workflow; included so
    # both workflow versions can share the same state definition)
    messages: Optional[List[Dict[str, Any]]]
