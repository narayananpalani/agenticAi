"""kinkyPipeline_v2.py — Shared ingestion helpers for kinkyShoeBros documents.

This module provides the core parsing, chunking, and baseline PII scrubbing
utilities used to process the kinkyShoeBros document suite. 

HOW TO RUN & TEST THIS SCRIPT ON MAC TERMINAL:
1. Open Terminal and navigate to the folder containing this script and `sample_docs/`.
2. Install dependencies by running this command: 
   pip3 install pymupdf beautifulsoup4 python-docx
3. Start the Python interactive shell by typing:
   python3
4. Copy the code block below EXACTLY as written (do not add any >>> symbols) 
   and paste it into the terminal, then press Return:

import kinkyPipeline_v2 as kp
kp.check_samples_exist()
text = kp.parse_pdf(kp.SAMPLE_PDF)
chunks = kp.chunk_recursive(text, max_size=400)
scrubbed_text, flags = kp.scrub_pii_regex(chunks[0])
print(f"Scrubbed: {scrubbed_text} | Flags: {flags}")

5. Note: If your terminal gets stuck on a `...` prompt after pasting, just 
   press Return one more time to execute the block.
6. To exit Python and return to your normal Mac terminal, press Ctrl + D.
"""
from __future__ import annotations

import re
from pathlib import Path

# ─── Sample document paths ────────────────────────────────────────────

SAMPLE_DOCS_DIR = Path(__file__).parent / "sample_docs"

# Updated for kinkyShoeBros generated files
SAMPLE_PDF  = SAMPLE_DOCS_DIR / "kinkyshoebros_policies.pdf"
SAMPLE_HTML = SAMPLE_DOCS_DIR / "kinkyshoebros_catalog.html"
SAMPLE_DOCX = SAMPLE_DOCS_DIR / "kinkyshoebros_preloved.docx"


def check_samples_exist() -> None:
    """Assert all 3 sample documents are present. Raise a clear error if not."""
    missing = [p.name for p in [SAMPLE_PDF, SAMPLE_HTML, SAMPLE_DOCX] if not p.exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing sample docs: {missing}. "
            f"Run your document generation script first to populate sample_docs/."
        )


# ─── Parsing ──────────────────────────────────────────────────────────

def parse_pdf(path: Path) -> str:
    """Extract text from a PDF using PyMuPDF. Returns concatenated text."""
    import pymupdf  # Updated from fitz to remove deprecation warning
    doc = pymupdf.open(str(path))
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n\n".join(pages)


def parse_html(path: Path) -> str:
    """Extract main-content text from HTML, stripping nav/footer/scripts."""
    from bs4 import BeautifulSoup
    html = path.read_text()
    soup = BeautifulSoup(html, "html.parser")
    # Strip nav, footer, script, style — keep only content
    for tag in soup(["nav", "footer", "script", "style"]):
        tag.decompose()
    # Get the <main> if present, else fall back to whole body
    main = soup.find("main") or soup.find("body") or soup
    return main.get_text(separator="\n", strip=True)


def parse_docx(path: Path) -> list[dict]:
    """Extract paragraphs from DOCX along with heading style.
    Returns list of {text, style} dicts."""
    from docx import Document
    doc = Document(str(path))
    return [
        {"text": p.text, "style": p.style.name}
        for p in doc.paragraphs
        if p.text.strip()
    ]


# ─── Chunking strategies ──────────────────────────────────────────────

def chunk_fixed(text: str, size: int = 400, overlap: int = 40) -> list[str]:
    """Sliding-window fixed-size chunker."""
    if len(text) <= size:
        return [text]
    chunks, i = [], 0
    while i < len(text):
        end = min(i + size, len(text))
        chunks.append(text[i:end])
        if end == len(text):
            break
        i = end - overlap
    return chunks


def chunk_recursive(text: str, max_size: int = 400) -> list[str]:
    """Split by paragraphs → sentences if still too long. Respects boundaries."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for para in paragraphs:
        if len(para) <= max_size:
            chunks.append(para)
        else:
            # Fall back to sentence split
            sentences = re.split(r'(?<=[.!?])\s+', para)
            current = ""
            for sent in sentences:
                if len(current) + len(sent) + 1 <= max_size:
                    current = (current + " " + sent).strip()
                else:
                    if current:
                        chunks.append(current)
                    current = sent
            if current:
                chunks.append(current)
    return chunks


# ─── PII scrubbing (regex baseline) ───────────────────────────────────

PII_PATTERNS = {
    "EMAIL":    re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'),
    "PHONE":    re.compile(r'\+?\d{0,2}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3,4}(?:[-.\s]?\d{4})?\b'),
    "EMP_ID":   re.compile(r'\bEMP-\d{4,6}\b'),
}


def scrub_pii_regex(text: str) -> tuple[str, list[str]]:
    """Regex-baseline PII scrubber. Returns (scrubbed_text, flags_found)."""
    flags = []
    scrubbed = text
    for label, pattern in PII_PATTERNS.items():
        matches = pattern.findall(scrubbed)
        for m in matches:
            flags.append(f"{label}: {m}")
            scrubbed = scrubbed.replace(m, f"[{label}]")
    return scrubbed, flags


# ─── The 9-field metadata schema ──────────────────────────────────────

METADATA_FIELDS = [
    "chunk_id",       # unique id, format: '{source_stem}#{idx}'
    "source",         # filename, e.g. 'kinkyshoebros_policies.pdf'
    "doc_type",       # 'pdf', 'html', 'docx'
    "section_path",   # e.g. 'Employee Handbook > Leave Policy'
    "page",           # int, PDF only; None otherwise
    "date",           # YYYY-MM-DD document date if known
    "language",       # ISO code, default 'en'
    "version",        # doc revision if tracked
    "ingested_at",    # UTC ISO timestamp of ingestion run
]