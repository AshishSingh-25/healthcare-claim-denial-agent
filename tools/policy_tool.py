"""
tools/policy_tool.py

Loads the local denial-code knowledge base and exposes a lookup
function. Also exposes a LangChain @tool-wrapped version for the
tool-calling agent workflow (v2).
"""

import json
import os

from langchain_core.tools import tool

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "denial_codes.json"
)

with open(_DATA_PATH, "r", encoding="utf-8") as f:
    _DENIAL_CODES = json.load(f)


def list_denial_codes() -> dict[str, str]:
    """Return available sample codes and labels from the reference library."""
    return {code: entry["category"] for code, entry in _DENIAL_CODES.items()}


def lookup_denial_code(denial_code: str) -> dict:
    """
    Look up a denial code in the local knowledge base.

    Returns a dict shaped either as:

        {
            "found": True,
            "denial_code": "...",
            "description": "...",
            "category": "...",
            "possible_causes": [...],
            "recommended_action": "..."
        }

    or, when the code is not in the knowledge base:

        {
            "found": False,
            "denial_code": "...",
            "message": "No information found for denial code ..."
        }
    """

    normalized_code = denial_code.strip().upper()

    entry = _DENIAL_CODES.get(normalized_code)

    if entry is None:
        return {
            "found": False,
            "denial_code": normalized_code,
            "message": f"No information found for denial code {normalized_code}."
        }

    return {
        "found": True,
        **entry,
        # Always supply the normalized lookup value, even if a legacy data
        # entry contains a malformed or missing denial_code field.
        "denial_code": normalized_code,
    }


@tool
def denial_lookup_tool(denial_code: str) -> str:
    """
    Look up the meaning, category, possible causes, and recommended
    action for a healthcare insurance claim denial code (e.g. 'CO-16').
    Returns a JSON string with the result. Use this tool whenever you
    need reference information about a specific denial code before
    analyzing a claim.
    """

    result = lookup_denial_code(denial_code)
    return json.dumps(result)
