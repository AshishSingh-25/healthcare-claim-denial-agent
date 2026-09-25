# Claim Resolve deployment

The Streamlit app remains available with `python -m streamlit run app.py`.
The hosted version uses a React/Vite frontend and the same LangGraph workflow behind FastAPI.
Only synthetic sample claims are supported. No database or claim history is stored.

## Linux backend

- Directory: `/home/ubuntu/healthcare-claim-denial-agent`
- Service: `claim-resolve-api`
- Local listener: `127.0.0.1:8510`
- Health: `GET /api/health`
- Reference library: `GET /api/denial-codes`
- Assessment: `POST /api/assess`

Copy `agents`, `tools`, `data`, `backend`, and `deploy` to the deployment directory, then run
`sh deploy/install-backend.sh`. For updates, restart with
`sudo systemctl restart claim-resolve-api` after installing dependencies.
Status: `systemctl status claim-resolve-api`; logs: `journalctl -u claim-resolve-api`.
The service is enabled on boot and restarts after failures. Request access logging and
LangSmith tracing are disabled. No API keys are required for this reference workflow.

Publish the loopback listener through an HTTPS reverse proxy or a configured Cloudflare
Tunnel hostname. Do not change existing server routes when adding the app.

## Vercel frontend

Deploy from `frontend/`, which has its own package lock and Vercel config.
Set `CLAIM_API_ORIGIN` to the backend HTTPS origin (scheme and hostname, without an API path).
The frontend calls same-origin `/api/*` functions; the Vercel proxy forwards only the
three documented endpoints. This avoids cross-origin browser access and keeps backend
configuration on the server. No `VITE_` environment variables or client secrets are needed.

Run `npm ci` and `npm run build` from `frontend/`. The linked Vercel project uses
`frontend` as its Root Directory, so run `vercel --prod` from the repository root.
GitHub deployments also build the `frontend` directory.
A public backend origin must be available before publishing a functioning production UI.

## Local development and tests

Install `requirements-dev.txt` in the project virtual environment.
Run `python -m uvicorn backend.api:app --host 127.0.0.1 --port 8510`.
In `frontend/`, run `npm ci` then `npm run dev`. Vite proxies `/api` to the local backend.
Run `python -m unittest discover -s tests -v` from the repository root.

## Configured production addresses

- Vercel project: `claim-resolve` in `ashish-8880`.
- Frontend: https://claim-resolve-dun.vercel.app
- Backend: https://claims-api.droidrex.me (Cloudflare Tunnel to `http://127.0.0.1:8510`).
- Production Vercel environment: `CLAIM_API_ORIGIN=https://claims-api.droidrex.me`.

Production verified on 2026-09-25: health checks, all seven sample-code options,
and a CO-18 assessment succeed through the public Vercel API proxy.
Cloudflare Bot Fight Mode originally challenged Vercel requests; the domain owner
disabled that feature to allow the integration. Re-enabling it can block the API again.
The proxy logs backend status and Cloudflare ray ID on non-JSON responses, never claim contents.
