# LexiSumm — Enterprise Document Summarizer (Privacy‑first)

FastAPI + React app to upload documents, extract content (Tika), redact PII, index chunks,
and generate concise summaries (≤150 words) with citations. Local‑first with MinIO, Postgres,
Redis+Celery; optional OpenAI/Ollama via feature flags.

## Quickstart (local, offline)
```bash
cp .env.example .env
docker compose up -d --build

# Dev without Docker
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload

# Run worker (separate shell)
celery -A backend.worker.celery_app worker --loglevel=INFO
```
Open UI: http://localhost:5173
API docs: http://localhost:8000/docs
# Gen-AI-Document-Summarizer
