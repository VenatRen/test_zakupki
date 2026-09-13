import fitz
import docx

from app.config import settings


def extract_text_from_pdf(path: str) -> str | None:

    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception:
        return None


def extract_text_from_docx(path: str) -> str | None:

    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return None
