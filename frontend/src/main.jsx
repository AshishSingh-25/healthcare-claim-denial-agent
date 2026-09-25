import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const initial = {claim_id:'CLM001',patient_id:'P1001',payer:'Example Health Insurance',procedure_code:'99213',diagnosis_code:'J06.9',claim_amount:'250.00',denial_code:'CO-16'};
const fields = [['claim_id','Claim ID'],['patient_id','Patient ID'],['payer','Payer'],['procedure_code','Procedure code'],['diagnosis_code','Diagnosis code']];
async function request(path, options = {}) {
  const response = await fetch(`/api/${path}`, {...options, signal: AbortSignal.timeout(20000)});
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const detail = Array.isArray(body.detail) ? body.detail.map(e => `${e.loc.at(-1)}: ${e.msg}`).join(' ') : body.detail;
    throw new Error(detail || 'The service is unavailable. Please try again.');
  }
  return response.json();
}
function App() {
  const [claim, setClaim] = useState(initial);
  const [codes, setCodes] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  async function loadCodes() {
    setLoading(true); setError('');
    try { setCodes(await request('denial-codes')); }
    catch { setError('Could not load sample codes. Check your connection and retry.'); }
    finally { setLoading(false); }
  }
  useEffect(() => { loadCodes(); }, []);
  function update(e) { setClaim({...claim,[e.target.name]:e.target.value}); setResult(null); }
  async function submit(e) {
    e.preventDefault(); setBusy(true); setError(''); setResult(null);
    try { setResult(await request('assess',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...claim,claim_amount:Number(claim.claim_amount)})})); }
    catch(e) { setError(e.name === 'TimeoutError' ? 'The review took too long. Please try again.' : e.message); }
    finally { setBusy(false); }
  }
  return <main>
    <header><span className="brand-icon" aria-hidden="true">+</span><span className="brand-name">Claim Resolve</span><span className="demo">Demo workspace</span></header>
    <section className="intro"><h1>A clearer next step for every denial.</h1><p>Explore a sample claim, understand its denial reason, and review the recommended action.</p></section>
    <form onSubmit={submit} aria-busy={busy}>
      <div className="form-title"><h2>Claim details</h2><span>Pre-filled with sample data</span></div>
      <fieldset disabled={busy}><legend className="sr-only">Sample claim information</legend>
        <div className="fields">{fields.map(([name,label])=><label key={name}>{label}<input name={name} value={claim[name]} onChange={update} required maxLength={name.endsWith('_code')?20:120}/></label>)}
          <label>Claim amount ($)<input name="claim_amount" type="number" min="0" max="10000000" step="0.01" required value={claim.claim_amount} onChange={update}/></label>
        </div>
        <label className="denial-label">Sample denial reason<select name="denial_code" value={claim.denial_code} onChange={update} disabled={loading || !codes.length} aria-describedby="reason-help">{loading?<option>Loading sample codes...</option>:codes.map(c=><option key={c.denial_code} value={c.denial_code}>{c.denial_code} — {c.category}</option>)}</select></label>
        <p className="hint" id="reason-help">Choose the reason that you want to explore. Need help? Open the sample code guide below.</p>
        <button type="submit" disabled={loading || !codes.length}>{busy?'Reviewing claim...':'Review denial'}</button>
      </fieldset>
    </form>
    {error && <div className="error" role="alert">{error}{!codes.length&&<button className="retry" onClick={loadCodes} disabled={loading}>Retry connection</button>}</div>}
    <details><summary>Sample code guide — what does each reason mean?</summary>{codes.map(c=><div className="guide-row" key={c.denial_code}><strong>{c.denial_code} &middot; {c.category}</strong><p>{c.description}</p></div>)}</details>
    <div aria-live="polite">{result&&<section className="results"><div className="results-title"><h2>Denial assessment</h2><span className="match">Reference matched</span></div><div className="result-grid">
      <article><span className="code-badge">{result.denial_info.denial_code}</span><h3>{result.denial_info.category}</h3><p>{result.denial_info.description}</p><h4>Possible causes</h4><ul>{result.denial_info.possible_causes.map(c=><li key={c}>{c}</li>)}</ul></article>
      <article><h3>Assessment</h3><p>{result.analysis}</p><h4>Recommended next action</h4><div className="next-action">{result.recommendation}</div></article>
    </div></section>}</div>
    <footer>Synthetic data only &middot; Based on the local sample reference library</footer>
  </main>;
}
createRoot(document.getElementById('root')).render(<App/>);
