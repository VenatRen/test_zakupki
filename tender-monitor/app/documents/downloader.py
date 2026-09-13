import os
import hashlib
import httpx

from app.config import settings


async def download_document(url: str, tender_id: int, filename: str) -> str | None:

    if not settings.download_documents:
        return None

    doc_dir = settings.document_dir
    os.makedirs(doc_dir, exist_ok=True)

    local_path = os.path.join(doc_dir, f"{tender_id}_{filename}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            with open(local_path, "wb") as f:
                f.write(response.content)

            return local_path

    except Exception:
        return None
