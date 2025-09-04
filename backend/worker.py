from celery import Celery
from .models import SessionLocal, Document, Summary, AuditLog
from .storage import get_file
from .summarize import summarize_with_citations, extract_text
import os

celery_app = Celery(__name__, broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"))

@celery_app.task
def summarize_task(doc_id: str):
    db = SessionLocal()
    try:
        doc = db.get(Document, doc_id)
        raw = get_file(doc.key)
        text = extract_text(raw, filename=doc.filename)
        summary, cites = summarize_with_citations(text)
        db.merge(Summary(document_id=doc_id, text=summary, citations_json=json.dumps(cites)))
        AuditLog.log(db, actor="system", action="SUMMARIZE", entity="Document", entity_id=doc_id)
    finally:
        db.close()

def enqueue_summarize(doc_id: str):
    summarize_task.delay(doc_id)
