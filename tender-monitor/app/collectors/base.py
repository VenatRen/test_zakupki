from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class TenderData:

    law: str = "223-ФЗ"

    notice_number: str | None = None

    title: str = ""

    description: str | None = None

    customer_name: str | None = None

    customer_inn: str | None = None

    okpd_code: str | None = None

    okpd_name: str | None = None

    price: Decimal | None = None

    currency: str | None = None

    region: str | None = None

    published_at: datetime | None = None

    deadline: datetime | None = None

    status: str | None = None

    source: str = ""

    external_id: str | None = None

    source_url: str | None = None

    eis_url: str | None = None

    documents: list[dict] | None = None


class BaseCollector:

    name = "base"

    async def collect(self) -> list[TenderData]:
        raise NotImplementedError

    async def healthcheck(self) -> bool:
        return True
