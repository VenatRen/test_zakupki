import re

from app.collectors.base import TenderData


KEYWORDS = (
    "образователь",
    "обучен",
    "повышен квалификац",
    "профессиональн переподготов",
    "дополнительн образован",
    "профессиональн обучен",
    "дпо",
    "семинар",
    "тренинг",
    "подготовк специалистов",
)


def okpd_match(code: str | None) -> bool:

    if not code:
        return False

    normalized = code.strip()

    return normalized == "85" or normalized.startswith("85.")


def keyword_match(tender: TenderData) -> bool:

    text = " ".join(
        filter(
            None,
            [
                tender.title,
                tender.description,
                tender.okpd_name,
            ],
        )
    ).lower()

    return any(
        keyword in text
        for keyword in KEYWORDS
    )


def classify(
    tender: TenderData,
) -> str | None:

    by_okpd = okpd_match(
        tender.okpd_code
    )

    by_text = keyword_match(
        tender
    )

    if by_okpd and by_text:
        return "OKPD+KEYWORD"

    if by_okpd:
        return "OKPD"

    if by_text:
        return "KEYWORD"

    return None


def is_candidate(
    tender: TenderData,
) -> bool:

    return classify(tender) is not None
