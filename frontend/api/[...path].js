// Same-origin proxy: the browser never receives server configuration.
export default async function handler(req, res) {
  const path = new URL(req.url, 'http://localhost').pathname;
  const allowed = {'/api/health':'GET', '/api/denial-codes':'GET', '/api/assess':'POST'};
  res.setHeader('Cache-Control', 'no-store');
  if (!(path in allowed)) return res.status(404).json({detail:'Not found.'});
  if (req.method !== allowed[path]) {
    res.setHeader('Allow', allowed[path]);
    return res.status(405).json({detail:'Method not allowed.'});
  }
  const origin = process.env.CLAIM_API_ORIGIN;
  if (!origin) return res.status(503).json({detail:'The review service is not configured yet.'});
  const body = req.method === 'POST' ? JSON.stringify(req.body) : undefined;
  if (body && Buffer.byteLength(body) > 8192) return res.status(413).json({detail:'Claim data is too large.'});
  try {
    const upstream = await fetch(new URL(path, origin), {
      method:req.method, headers:{'Content-Type':'application/json'}, body,
      signal:AbortSignal.timeout(15000), redirect:'error',
    });
    const payload = await upstream.json();
    return res.status(upstream.status).json(payload);
  } catch {
    return res.status(503).json({detail:'The review service is temporarily unavailable. Please try again.'});
  }
}
