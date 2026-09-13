import asyncio

from celery import Celery

from app.config import settings
from app.db.session import SessionLocal
from app.collectors.manager import CollectorManager

from app.collectors.eis import EisCollector
from app.collectors.fabrikant import (
    FabrikantCollector,
)
from app.collectors.tektorg import (
    TektorgCollector,
)
from app.collectors.rts import (
    RtsCollector,
)


celery_app = Celery(
    "tender_monitor",
    broker=settings.redis_url,
    backend=settings.redis_url,
)


celery_app.conf.beat_schedule = {
    "collect-tenders": {
        "task":
            "app.workers.tasks.collect_all",
        "schedule":
            settings.collect_interval_minutes * 60,
    },
}


def get_collectors():

    result = []

    if settings.enable_eis:
        result.append(
            EisCollector()
        )

    if settings.enable_fabrikant:
        result.append(
            FabrikantCollector()
        )

    if settings.enable_tektorg:
        result.append(
            TektorgCollector()
        )

    if settings.enable_rts:
        result.append(
            RtsCollector()
        )

    return result


async def collect():

    async with SessionLocal() as session:

        manager = CollectorManager(
            session
        )

        for collector in get_collectors():

            await manager.run(
                collector
            )


@celery_app.task
def collect_all():

    asyncio.run(
        collect()
    )
