from html import escape
from pathlib import Path

import streamlit as st

from agents.workflow import claim_workflow
from tools.policy_tool import list_denial_codes, lookup_denial_code


st.set_page_config(page_title="Claim Resolve | Denial review", page_icon="+", layout="wide")
st.html(Path(__file__).with_name("styles.css"))
st.html('<div class="brand"><span class="brand-icon" aria-hidden="true">+</span>'
        '<span class="brand-name">Claim Resolve</span><span class="brand-note">Demo workspace</span></div>'
        '<div class="intro"><h1>A clearer next step for every denial.</h1>'
        '<p>Explore a sample claim, understand its denial reason, and review the recommended action.</p></div>')

denial_options = list_denial_codes()
with st.form("claim_form"):
    st.html('<div class="form-heading"><h2>Claim details</h2><span>Pre-filled with sample data</span></div>')
    claim_col, patient_col, payer_col = st.columns((1, 1, 1.35))
    with claim_col:
        claim_id = st.text_input("Claim ID", value="CLM001")
    with patient_col:
        patient_id = st.text_input("Patient ID", value="P1001")
    with payer_col:
        payer = st.text_input("Payer", value="Example Health Insurance")
    code_col, diagnosis_col, amount_col = st.columns(3)
    with code_col:
        procedure_code = st.text_input("Procedure code", value="99213")
    with diagnosis_col:
        diagnosis_code = st.text_input("Diagnosis code", value="J06.9")
    with amount_col:
        claim_amount = st.number_input("Claim amount ($)", min_value=0.0, value=250.0, step=10.0)
    denial_code = st.selectbox(
        "Sample denial reason", options=list(denial_options),
        format_func=lambda code: f"{code} \u2014 {denial_options[code]}",
        help="Search by code or reason. These seven options are sample reference data.",
    )
    st.caption("Choose the reason that you want to explore. Need help? Open the sample code guide below.")
    submitted = st.form_submit_button("Review denial", type="primary", use_container_width=True)

with st.expander("Sample code guide - what does each reason mean?"):
    rows = []
    for code, category in denial_options.items():
        description = lookup_denial_code(code)["description"]
        rows.append(f'<div class="guide-row"><strong>{escape(code)} &middot; {escape(category)}</strong>'
                    f'<p>{escape(description)}</p></div>')
    st.html("".join(rows))

if submitted:
    claim_state = {
        "claim_id": claim_id, "patient_id": patient_id, "procedure_code": procedure_code,
        "diagnosis_code": diagnosis_code, "payer": payer, "claim_amount": claim_amount,
        "denial_code": denial_code, "denial_info": None, "analysis": None,
        "recommendation": None, "ai_error": None,
    }
    with st.spinner("Reviewing the sample claim..."):
        result = claim_workflow.invoke(claim_state)
    denial_info = result["denial_info"]
    if denial_info["found"]:
        causes = "".join(f"<li>{escape(str(cause))}</li>" for cause in denial_info["possible_causes"])
        # Use the HTML renderer, not Markdown; escape every dynamic value.
        st.html(
            '<div class="results-heading"><h2>Denial assessment</h2><span class="match">Reference matched</span></div>'
            '<div class="result-grid"><section class="result-card"><span class="code-badge">'
            f'{escape(denial_info["denial_code"])}</span><h3>{escape(denial_info["category"])}</h3>'
            f'<p>{escape(denial_info["description"])}</p><span class="result-label">Possible causes</span><ul>{causes}</ul></section>'
            '<section class="result-card"><h3>Assessment</h3>'
            f'<p>{escape(str(result["analysis"]))}</p><span class="result-label">Recommended next action</span>'
            f'<div class="next-action"><p>{escape(str(result["recommendation"]))}</p></div></section></div>'
        )
    else:
        st.warning(denial_info["message"])
        st.info(result["analysis"])

st.html('<div class="footer-note">Synthetic data only &middot; Based on the local sample reference library</div>')
