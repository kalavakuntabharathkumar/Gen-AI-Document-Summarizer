from typing import Tuple, List
import re
from tika import parser

def redact_pii(text: str) -> str:
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[EMAIL]", text)
    text = re.sub(r"\+?\d[\d\s-]{7,}\d", "[PHONE]", text)
    return text

def extract_text(content: bytes, filename: str) -> str:
    parsed = parser.from_buffer(content, headers={'Content-Type':'application/octet-stream'})
    text = parsed.get("content") or ""
    return redact_pii(text.strip())

def chunk(text: str, size: int = 1200, overlap: int = 150):
    i = 0
    n = len(text)
    while i < n:
        yield text[i:i+size]
        i += size - overlap

def summarize_chunk(txt: str) -> str:
    # Lightweight heuristic summarizer: pick key sentences (stand‑in for local LLM)
    sentences = re.split(r'(?<=[.!?])\s+', txt.strip())
    return " ".join(sentences[:3])[:300]

def summarize_with_citations(text: str) -> Tuple[str, List[str]]:
    chs = list(chunk(text))
    parts = [summarize_chunk(c) for c in chs[:5]]  # cap for perf
    citations = [f"chunk:{i}" for i in range(len(parts))]
    summary = " ".join(parts)
    # Cap length ~150 words
    words = summary.split()
    if len(words) > 150:
        summary = " ".join(words[:150]) + "…"
    return summary, citations
