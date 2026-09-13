from app.collectors.base import TenderData
from app.filters.education import (
    classify,
    is_candidate,
)


def test_okpd_85():

    tender = TenderData(
        title="Любая услуга",
        okpd_code="85.42.19",
    )

    assert is_candidate(tender)
    assert classify(tender) == "OKPD"


def test_keyword():

    tender = TenderData(
        title="Проведение обучения работников",
        okpd_code="62.01",
    )

    assert is_candidate(tender)
    assert classify(tender) == "KEYWORD"


def test_both():

    tender = TenderData(
        title="Обучение работников",
        okpd_code="85.42.19",
    )

    assert classify(tender) == "OKPD+KEYWORD"
