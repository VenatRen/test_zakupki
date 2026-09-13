import hashlib
import json
import re

from app.collectors.base import TenderData


def clean_text(value: str | None) -> str | None:

    if not value:
        return None

    return re.sub(
        r"\s+",
        " ",
        value,
    ).strip()


def fingerprint(
    tender: TenderData,
) -> str:

    identity = {

        "law": tender.law,

        "notice_number":
            clean_text(
                tender.notice_number
            ),

        "customer_inn":
            clean_text(
                tender.customer_inn
            ),

        "title":
            clean_text(
                tender.title
            ),

    }

    raw = json.dumps(
        identity,
        ensure_ascii=False,
        sort_keys=True,
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()
