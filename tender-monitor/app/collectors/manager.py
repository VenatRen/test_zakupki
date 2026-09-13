import logging
from datetime import datetime, timezone

from app.db.models import CollectorRun
from app.db.repository import (
    save_raw,
    save_tender,
)
from app.parsers.common import fingerprint


logger = logging.getLogger(
    "collector.manager"
)


class CollectorManager:

    def __init__(self, session):

        self.session = session

    async def run(self, collector):

        started = datetime.now(
            timezone.utc
        )

        run = CollectorRun(
            source=collector.name,
            started_at=started,
            status="RUNNING",
        )

        self.session.add(run)

        await self.session.commit()

        try:

            items = await collector.collect()

            run.received_count = len(
                items
            )

            for item in items:

                payload = {
                    "notice_number":
                        item.notice_number,
                    "title":
                        item.title,
                    "okpd":
                        item.okpd_code,
                    "source":
                        item.source,
                }

                await save_raw(
                    self.session,
                    item.source,
                    item.external_id,
                    payload,
                )

                fp = fingerprint(item)

                tender, created = (
                    await save_tender(
                        self.session,
                        item,
                        fp,
                    )
                )

                if created:

                    run.new_count += 1

            run.status = "OK"

        except Exception as exc:

            logger.exception(
                "Collector failed: %s",
                collector.name,
            )

            run.status = "ERROR"
            run.error_count += 1
            run.error_message = str(
                exc
            )

        finally:

            run.finished_at = (
                datetime.now(
                    timezone.utc
                )
            )

            await self.session.commit()
