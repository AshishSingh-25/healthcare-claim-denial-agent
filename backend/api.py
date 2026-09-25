"""HTTP interface for the synthetic claim review workflow."""
from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from agents.workflow import claim_workflow
from tools.policy_tool import list_denial_codes, lookup_denial_code

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
Code = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=20)]


class ClaimRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    claim_id: Text
    patient_id: Text
    payer: Text
    procedure_code: Code
    diagnosis_code: Code
    claim_amount: float = Field(ge=0, le=10000000, allow_inf_nan=False)
    denial_code: Code

    @field_validator("denial_code")
    @classmethod
    def known_denial(cls, value):
        code = value.upper()
        if code not in list_denial_codes():
            raise ValueError("Choose a denial reason from the sample library.")
        return code


app = FastAPI(title="Claim Resolve API", version="1.0.0", docs_url=None, redoc_url=None)


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "synthetic-reference"}


@app.get("/api/denial-codes")
def denial_codes():
    return [lookup_denial_code(code) for code in list_denial_codes()]


@app.post("/api/assess")
def assess(claim: ClaimRequest):
    try:
        result = claim_workflow.invoke(claim.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=503, detail="The review could not be completed. Please try again.") from exc
    return {key: result[key] for key in ("denial_info", "analysis", "recommendation")}
