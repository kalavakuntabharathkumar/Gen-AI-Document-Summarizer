# ASSUMPTIONS
- Local demo defaults to SQLite if `DATABASE_URL` not provided; docker-compose uses Postgres.
- Summarization defaults to a heuristic (first key sentences) to remain offline; when `USE_OPENAI=true` or `USE_OLLAMA=true`, a provider layer would be used (stubbed).
- PII redaction is regex‑based pre‑indexing; can be extended.
- RBAC: demo with single user/token; multi‑tenant hooks sketched via `owner_id` fields.
- Audit trail stored in immutable append‑only table.
