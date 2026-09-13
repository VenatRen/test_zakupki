import hashlib
import json
from datetime import datetime, timezone

from sqlalchemy import select

from app.collectors.base import TenderData
from app.filters.education import classify

from .models import (
    RawTender,
    Tender,
    TenderSource,
)


def utcnow():

    return datetime.now(timezone.utc)


def payload_hash(payload):

    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )

    return hashlib.sha256(
        raw.encode()
    ).hexdigest()


async def save_raw(
    session,
    source: str,
    external_id: str | None,
    payload: dict,
):

    item = RawTender(
        source=source,
        external_id=external_id,
        payload=payload,
        payload_hash=payload_hash(payload),
    )

    session.add(item)


async def find_by_notice(
    session,
    notice_number,
):

    if not notice_number:
        return None

    result = await session.execute(
        select(Tender)
        .where(
            Tender.notice_number
            == notice_number
        )
        .limit(1)
    )

    return result.scalar_one_or_none()


async def find_source(
    session,
    source,
    external_id,
):

    if not external_id:
        return None

    result = await session.execute(
        select(TenderSource)
        .where(
            TenderSource.source
            == source,
            TenderSource.external_id
            == external_id,
        )
        .limit(1)
    )

    return result.scalar_one_or_none()


async def save_tender(
    session,
    data: TenderData,
    fp: str,
):

    match_type = classify(data)

    if not match_type:
        return None, False

    tender = await find_by_notice(
        session,
        data.notice_number,
    )

    created = False

    if tender is None:

        tender = Tender(
            law=data.law,
            notice_number=data.notice_number,
            title=data.title,
            description=data.description,
            customer_name=data.customer_name,
            customer_inn=data.customer_inn,
            okpd_code=data.okpd_code,
            okpd_name=data.okpd_name,
            price=data.price,
            currency=data.currency,
            region=data.region,
            published_at=data.published_at,
            deadline=data.deadline,
            status=data.status,
            match_type=match_type,
            canonical_url=(
                data.eis_url
                or data.source_url
            ),
            fingerprint=fp,
        )

        session.add(tender)

        await session.flush()

        created = True

    else:

        changed = (
            tender.fingerprint != fp
        )

        tender.title = data.title
        tender.description = data.description
        tender.customer_name = data.customer_name
        tender.customer_inn = data.customer_inn
        tender.okpd_code = data.okpd_code
        tender.okpd_name = data.okpd_name
        tender.price = data.price
        tender.currency = data.currency
        tender.region = data.region
        tender.published_at = data.published_at
        tender.deadline = data.deadline
        tender.status = data.status
        tender.match_type = match_type
        tender.fingerprint = fp
        tender.updated_at = utcnow()

        created = changed

    source = await find_source(
        session,
        data.source,
        data.external_id
        or data.notice_number,
    )

    if source is None:

        source = TenderSource(
            tender_id=tender.id,
            source=data.source,
            external_id=(
                data.external_id
                or data.notice_number
            ),
            url=data.source_url,
        )

        session.add(source)

    else:

        source.last_seen = utcnow()
        source.url = data.source_url

    await session.commit()

    return tender, created
