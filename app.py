import streamlit as st

from agents.workflow import claim_workflow


st.set_page_config(
    page_title="Claim Resolve | Denial Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
:root{--ink:#11263d;--muted:#64748b;--navy:#102a43;--blue:#1677ff;--aqua:#00a9a5;--line:#dbe5ef;--surface:#fff;--canvas:#f4f8fc}
.stApp{background:radial-gradient(circle at 92% 0%,#d9f5f1 0,transparent 26rem),radial-gradient(circle at 0% 10%,#e6f0ff 0,transparent 28rem),var(--canvas);color:var(--ink)}
#MainMenu,footer,header{visibility:hidden}.block-container{max-width:1220px;padding-top:2.4rem;padding-bottom:3rem}
.hero{background:linear-gradient(118deg,#0b2945 0%,#123c63 58%,#0f7175 100%);border-radius:24px;padding:2.1rem 2.3rem;color:#fff;box-shadow:0 18px 42px rgba(17,38,61,.2);margin-bottom:1.4rem;position:relative;overflow:hidden}
.hero:after{content:"";position:absolute;width:260px;height:260px;right:-85px;top:-130px;border:42px solid rgba(142,234,224,.16);border-radius:50%}.eyebrow{font-size:.72rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:#93e3dc}.hero h1{font-size:2.15rem;line-height:1.15;margin:.45rem 0 .55rem;letter-spacing:-.035em}.hero p{color:#d9e9f5;max-width:620px;margin:0;font-size:1rem}.trust-pill{display:inline-block;margin-top:1.2rem;padding:.36rem .7rem;border-radius:999px;background:rgba(255,255,255,.13);color:#d8fff9;font-size:.76rem;font-weight:600}
.section-label{font-size:.74rem;font-weight:750;color:var(--aqua);letter-spacing:.1em;text-transform:uppercase;margin-bottom:.2rem}.section-title{color:var(--ink);font-size:1.35rem;font-weight:720;letter-spacing:-.025em;margin:0 0 .2rem}.section-help{color:var(--muted);font-size:.9rem;margin-bottom:1.1rem}
div[data-testid="stForm"]{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:1.35rem 1.45rem .75rem;box-shadow:0 8px 25px rgba(28,57,85,.06)}div[data-testid="stTextInput"] label,div[data-testid="stNumberInput"] label{color:#496176;font-size:.79rem;font-weight:650}div[data-testid="stTextInput"] input,div[data-testid="stNumberInput"] input{border-radius:9px;border-color:#c9d8e6;background:#fbfdff}div[data-testid="stTextInput"] input:focus,div[data-testid="stNumberInput"] input:focus{border-color:var(--blue);box-shadow:0 0 0 2px rgba(22,119,255,.12)}div[data-testid="stFormSubmitButton"] button{border:0;border-radius:10px;background:linear-gradient(105deg,#087a84,#0b9e9c);color:#fff;font-weight:700;padding:.62rem 1.05rem;transition:transform .15s ease,box-shadow .15s ease}div[data-testid="stFormSubmitButton"] button:hover{transform:translateY(-1px);box-shadow:0 8px 18px rgba(0,139,139,.25)}
.result-shell{margin-top:1.7rem}.result-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:.9rem}.status-ok{color:#08756d;background:#d8f5ed;padding:.35rem .7rem;border-radius:999px;font-size:.75rem;font-weight:700}.info-card,.insight-card{background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:16px;padding:1.25rem 1.35rem;height:100%;box-sizing:border-box;box-shadow:0 7px 20px rgba(28,57,85,.045)}.info-card h3,.insight-card h3{margin:0 0 .85rem;font-size:1rem;color:var(--navy)}.code-badge{display:inline-block;color:#075c70;background:#e1f6f6;padding:.34rem .62rem;border-radius:7px;font-size:.85rem;font-weight:750;margin-bottom:.75rem}.detail-label{display:block;color:#718399;font-size:.68rem;letter-spacing:.08em;font-weight:750;text-transform:uppercase;margin:.75rem 0 .2rem}.detail-copy{color:#2d4358;font-size:.92rem;line-height:1.52}.cause{display:flex;gap:.55rem;align-items:flex-start;color:#395269;font-size:.88rem;line-height:1.35;margin:.58rem 0}.cause-dot{width:7px;height:7px;flex:0 0 7px;border-radius:50%;background:#1ab3ac;margin-top:.32rem}.answer{color:#30485e;line-height:1.65;font-size:.94rem;white-space:pre-wrap}.recommendation{border-left:4px solid #10a59e;background:#f1fbfa;border-radius:0 12px 12px 0;padding:1rem 1.05rem;color:#294c50;line-height:1.58}
@media(max-width:700px){.block-container{padding:1rem}.hero{padding:1.6rem;border-radius:18px}.hero h1{font-size:1.7rem}}
div[data-testid="stFormSubmitButton"]{margin-top:.7rem}div[data-testid="stFormSubmitButton"] button{width:100%;min-height:3.15rem;border:1px solid rgba(255,255,255,.22);border-radius:12px;background:linear-gradient(105deg,#075f6f 0%,#078f91 48%,#19afa2 100%);color:#fff;font-size:.96rem;font-weight:750;letter-spacing:.01em;padding:.72rem 1.3rem;box-shadow:0 8px 0 #064e5c,0 15px 28px rgba(4,105,112,.24);transition:transform .16s ease,box-shadow .16s ease,filter .16s ease}div[data-testid="stFormSubmitButton"] button:hover{transform:translateY(-2px);filter:brightness(1.06);box-shadow:0 10px 0 #064e5c,0 19px 32px rgba(4,105,112,.29)}div[data-testid="stFormSubmitButton"] button:active{transform:translateY(5px);box-shadow:0 3px 0 #064e5c,0 8px 16px rgba(4,105,112,.18)}div[data-testid="stFormSubmitButton"] button:focus:not(:active){box-shadow:0 8px 0 #064e5c,0 0 0 4px rgba(17,181,169,.22),0 15px 28px rgba(4,105,112,.24)}
div[data-testid="stTextInput"] div[data-baseweb="input"],div[data-testid="stNumberInput"] div[data-baseweb="input"]{background:rgba(248,252,255,.58);border:1px solid rgba(63,91,116,.46);border-radius:10px;box-shadow:inset 0 1px 0 rgba(255,255,255,.8),0 1px 2px rgba(18,45,70,.035);transition:border-color .16s ease,box-shadow .16s ease,background .16s ease}div[data-testid="stTextInput"] div[data-baseweb="input"] input,div[data-testid="stNumberInput"] div[data-baseweb="input"] input{background:transparent!important;border:0!important;box-shadow:none!important;color:#19334c}div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within{background:rgba(255,255,255,.78);border-color:#0b9e9c;box-shadow:0 0 0 3px rgba(11,158,156,.14),inset 0 1px 0 rgba(255,255,255,.9)}
div[data-testid="stTextInput"] label,div[data-testid="stNumberInput"] label{color:#334e68!important;opacity:1!important}div[data-testid="stTextInput"] div[data-baseweb="input"],div[data-testid="stNumberInput"] div[data-baseweb="input"]{border:1px solid #8ea5b8!important;outline:none;overflow:hidden}div[data-testid="stTextInput"] div[data-baseweb="input"] input,div[data-testid="stNumberInput"] div[data-baseweb="input"] input{color:#19334c!important;-webkit-text-fill-color:#19334c!important;caret-color:#087f82!important;opacity:1!important}div[data-testid="stTextInput"] div[data-baseweb="input"] input::placeholder,div[data-testid="stNumberInput"] div[data-baseweb="input"] input::placeholder{color:#718399!important;-webkit-text-fill-color:#718399!important;opacity:1!important}div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,div[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within{border-color:#078f91!important;box-shadow:0 0 0 3px rgba(7,143,145,.16),inset 0 1px 0 rgba(255,255,255,.95)!important}
div[data-testid="stTextInput"] input,div[data-testid="stNumberInput"] input,div[data-baseweb="input"] input{display:block!important;visibility:visible!important;color:#19334c!important;background:transparent!important;font-size:1rem!important;font-weight:500!important;line-height:1.4!important;opacity:1!important;-webkit-text-fill-color:#19334c!important;text-shadow:none!important}div[data-testid="stTextInput"] input::placeholder,div[data-testid="stNumberInput"] input::placeholder{color:#718399!important;opacity:1!important;-webkit-text-fill-color:#718399!important}
div[data-testid="stTextInput"] div[data-baseweb="input"],div[data-testid="stNumberInput"] div[data-baseweb="input"],div[data-baseweb="input"]>div{background-color:rgba(248,252,255,.94)!important;background-image:none!important}div[data-testid="stTextInput"] div[data-baseweb="input"] input,div[data-testid="stNumberInput"] div[data-baseweb="input"] input{background-color:transparent!important}
div[data-testid="stForm"]{background:rgba(255,255,255,.96)!important}div[data-testid="stTextInput"] input[type="text"],div[data-testid="stNumberInput"] input[type="number"],div[data-baseweb="input"] input{background:#f8fcff!important;background-color:#f8fcff!important;color:#19334c!important;-webkit-text-fill-color:#19334c!important;color-scheme:light!important}div[data-testid="stTextInput"] div[data-baseweb="input"],div[data-testid="stNumberInput"] div[data-baseweb="input"],div[data-baseweb="base-input"],div[data-baseweb="input"]{background:#f8fcff!important;background-color:#f8fcff!important;color-scheme:light!important}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<section class="hero"><div class="eyebrow">Claim operations workspace</div><h1>Make denial follow-up<br>clearer and faster.</h1><p>Review synthetic claim denials against a structured reference library and identify the next corrective step.</p><div class="trust-pill">● Reference-powered · Synthetic data only</div></section>
""", unsafe_allow_html=True)
st.markdown('<div class="section-label">New review</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Claim details</div>', unsafe_allow_html=True)
st.markdown('<div class="section-help">Enter the fields available on the denied claim. Denial codes are matched to the local reference library.</div>', unsafe_allow_html=True)

with st.form("claim_form"):
    claim_col, patient_col, payer_col = st.columns((1, 1, 1.35))
    with claim_col: claim_id = st.text_input("Claim ID", value="CLM001")
    with patient_col: patient_id = st.text_input("Patient ID", value="P1001")
    with payer_col: payer = st.text_input("Payer", value="Example Health Insurance")
    code_col, diagnosis_col, amount_col, denial_col = st.columns((1, 1, 1, 1))
    with code_col: procedure_code = st.text_input("Procedure code", value="99213")
    with diagnosis_col: diagnosis_code = st.text_input("Diagnosis code", value="J06.9")
    with amount_col: claim_amount = st.number_input("Claim amount ($)", min_value=0.0, value=250.0, step=10.0)
    with denial_col: denial_code = st.text_input("Denial code", value="CO-16")
    submitted = st.form_submit_button("Run denial assessment  →")

if submitted:
    claim_state = {"claim_id":claim_id,"patient_id":patient_id,"procedure_code":procedure_code,"diagnosis_code":diagnosis_code,"payer":payer,"claim_amount":claim_amount,"denial_code":denial_code,"denial_info":None,"analysis":None,"recommendation":None,"ai_error":None}
    with st.spinner("Reviewing denial reference data..."):
        result = claim_workflow.invoke(claim_state)
    denial_info = result["denial_info"]
    st.markdown('<div class="result-shell">', unsafe_allow_html=True)
    if denial_info["found"]:
        st.markdown("""<div class="result-header"><div><div class="section-label">Review result</div><div class="section-title">Denial assessment</div></div><div class="status-ok">REFERENCE MATCHED</div></div>""", unsafe_allow_html=True)
        detail_col, analysis_col = st.columns((1, 1.5), gap="large")
        with detail_col:
            causes = "".join(f'<div class="cause"><span class="cause-dot"></span><span>{cause}</span></div>' for cause in denial_info["possible_causes"])
            st.markdown(f"""<div class="info-card"><h3>Denial information</h3><div class="code-badge">{denial_info.get('denial_code', denial_code.strip().upper())}</div><span class="detail-label">Category</span><div class="detail-copy">{denial_info['category']}</div><span class="detail-label">Description</span><div class="detail-copy">{denial_info['description']}</div><span class="detail-label">Possible causes</span>{causes}</div>""", unsafe_allow_html=True)
        with analysis_col:
            st.markdown('<div class="insight-card"><h3>Assessment</h3>', unsafe_allow_html=True)
            st.markdown(f'<div class="answer">{result["analysis"]}</div>', unsafe_allow_html=True)
            st.markdown('<span class="detail-label">Recommended next action</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="recommendation">{result["recommendation"]}</div></div>', unsafe_allow_html=True)
    else:
        st.warning(denial_info["message"])
        st.info(result["analysis"])
    st.markdown("</div>", unsafe_allow_html=True)
