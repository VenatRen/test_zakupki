from .base import (
    BaseCollector,
    TenderData,
)


class EisCollector(
    BaseCollector
):

    name = "eis"

    async def healthcheck(self):

        return False

    async def collect(self):

        return []
