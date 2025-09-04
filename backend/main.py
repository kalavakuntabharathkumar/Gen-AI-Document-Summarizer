from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .storage import store_file, ensure_bucket
from .security import get_current_user, create_demo_user, UserOut
from .models import Base, engine, SessionLocal, Document, Summary, AuditLog
from .worker import enqueue_summarize
from sqlalchemy.orm import Session
import uuid

app = FastAPI(title="LexiSumm API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
ensure_bucket()
create_demo_user()

class UploadResponse(BaseModel):
    document_id: str
    status: str

@app.post("/login", response_model=UserOut)
def login_demo():
    # Demo endpoint returns a short‑lived token for demo user
    return create_demo_user()

@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...), user=Depends(get_current_user)):
    content = await file.read()
    key = f"uploads/{uuid.uuid4()}-{file.filename}"
    store_file(key, content)
    db: Session = SessionLocal()
    try:
        doc = Document(id=str(uuid.uuid4()), key=key, filename=file.filename, owner_id=user.id)
        db.add(doc); db.commit()
        AuditLog.log(db, actor=user.email, action="UPLOAD", entity="Document", entity_id=doc.id)
        enqueue_summarize(doc.id)
        return UploadResponse(document_id=doc.id, status="QUEUED")
    finally:
        db.close()

class SummaryOut(BaseModel):
    document_id: str
    summary: str | None
    citations: list[str] | None
    status: str

@app.get("/summary/{doc_id}", response_model=SummaryOut)
def get_summary(doc_id: str, user=Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        summ = db.get(Summary, doc_id)
        doc = db.get(Document, doc_id)
        if not doc or doc.owner_id != user.id:
            raise HTTPException(status_code=404, detail="Not found")
        status = "PENDING" if summ is None else "READY"
        return SummaryOut(document_id=doc_id, summary=getattr(summ, "text", None),
                          citations=getattr(summ, "citations", None), status=status)
    finally:
        db.close()
