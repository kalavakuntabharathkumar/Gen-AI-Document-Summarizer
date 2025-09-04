# ARCHITECTURE

## Components
- **FastAPI** service exposes REST for auth, upload, and summary retrieval.
- **MinIO** stores raw files; Tika extracts text; we redact PII before processing.
- **Celery + Redis** handles async processing and status updates.
- **Postgres** stores metadata (documents), summaries, and audit logs.
- **React (Vite)** minimal UI for upload & polling.

## Provider Abstraction
`backend/summarize.py` encapsulates summarization. Local default is extractive/heuristic.
When keys/features are enabled, you can route to OpenAI/Ollama with the same interface.

## Security & Privacy
- JWT bearer for API, short‑lived demo token.
- PII redaction (emails/phones) before indexing.
- CORS restricted via config in production; HTTPS assumed behind gateway in cloud.
- Rate limiting can be added via proxy (e.g., API Gateway/Lambda or nginx + fail2ban).

## Deployment
- **Local**: Docker Compose (api, worker, redis, postgres, minio, web).
- **AWS**: Package FastAPI as Lambda via AWS SAM (template not included here for brevity).
