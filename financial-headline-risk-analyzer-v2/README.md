# Financial Headline Risk Analyzer — Version 2

This is a production-style starter that uses a real Python NLP backend and a Next.js frontend.

## Structure

- `web/` — Next.js frontend for Vercel
- `api/` — FastAPI backend for Vercel Python runtime
- `api/model/` — trained sklearn artifacts and labels

## Deploy on Vercel

Vercel's Python runtime supports ASGI/WSGI apps, and the docs say that to deploy a Python API alongside a frontend such as a Next.js app within the same project, you should use **Services**. That means you should create **two Vercel services** from this repo: one for `web/` and one for `api/`. See the official docs for Python runtime and Next.js deployment.

### 1) Frontend service
- Root directory: `web`
- Framework preset: Next.js
- Environment variable:
  - `NEXT_PUBLIC_API_BASE_URL=https://<your-api-service>.vercel.app`

### 2) API service
- Root directory: `api`
- Framework preset: Other / Python auto-detected
- Python app entrypoint: `app.py` with top-level `app = FastAPI()`

## Local development

### API
```bash
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Web
```bash
cd web
npm install
npm run dev
```

Then open `http://localhost:3000`.

## Notes
- The backend loads pre-trained sklearn artifacts on startup for fast inference.
- The frontend calls `POST /analyze`.
- You can retrain artifacts by running `python train_artifacts.py` inside `api/`.
