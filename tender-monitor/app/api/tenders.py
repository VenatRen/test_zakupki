from fastapi import APIRouter
from sqlalchemy import select

from app.db.models import Tender
from app.db.session import SessionLocal

router = APIRouter()


@router.get("/api/tenders")
async def get_tenders(
    limit: int = 100,
):

    async with SessionLocal() as session:

        result = await session.execute(
            select(Tender)
            .order_by(
                Tender.created_at.desc()
            )
            .limit(
                min(limit, 500)
            )
        )

        tenders = result.scalars().all()

        return [
            {
                "id": t.id,
                "notice":
                    t.notice_number,
                "title":
                    t.title,
                "customer":
                    t.customer_name,
                "okpd":
                    t.okpd_code,
                "price":
                    str(t.price)
                    if t.price is not None
                    else None,
                "region":
                    t.region,
                "deadline":
                    t.deadline,
                "status":
                    t.status,
                "source":
                    t.canonical_url,
            }
            for t in tenders
        ]
