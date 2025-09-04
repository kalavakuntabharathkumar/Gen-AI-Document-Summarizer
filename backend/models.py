from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column
from sqlalchemy import create_engine, String, Text
from pydantic import BaseModel
import os, json

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lexi.db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    key: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[str] = mapped_column(String, nullable=False)

class Summary(Base):
    __tablename__ = "summaries"
    document_id: Mapped[str] = mapped_column(String, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    citations_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")

    @property
    def citations(self):
        try:
            return json.loads(self.citations_json)
        except Exception:
            return []

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    actor: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    entity: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)

    @staticmethod
    def log(db, actor: str, action: str, entity: str, entity_id: str):
        import uuid
        db.add(AuditLog(id=str(uuid.uuid4()), actor=actor, action=action, entity=entity, entity_id=entity_id))
        db.commit()

class UserOut(BaseModel):
    id: str
    email: str
    token: str
