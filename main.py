from agents.workflow import claim_workflow


claim_state = {
    "claim_id": "CLM001",
    "patient_id": "P1001",
    "procedure_code": "99213",
    "diagnosis_code": "J06.9",
    "payer": "Example Health Insurance",
    "claim_amount": 250.00,
    "denial_code": "CO-16",
    "denial_info": None,
    "analysis": None,
    "recommendation": None
}


result = claim_workflow.invoke(claim_state)


print("\n========== DENIAL INFORMATION ==========")
print(result["denial_info"])


print("\n========== AI CLAIM ANALYSIS ==========")
print(result["analysis"])


print("\n========== RECOMMENDED ACTION ==========")
print(result["recommendation"])
