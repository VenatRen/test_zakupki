import asyncio
import re
from decimal import Decimal

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.config import settings

from .base import (
    BaseCollector,
    TenderData,
)


class FabrikantCollector(
    BaseCollector
):

    name = "fabrikant"

    async def healthcheck(self):

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            page = await browser.new_page()

            try:

                response = await page.goto(
                    settings.fabrikant_url,
                    wait_until="domcontentloaded",
                    timeout=settings.browser_timeout_ms,
                )

                return (
                    response is not None
                    and response.status < 500
                )

            except Exception:

                return False

            finally:

                await browser.close()

    async def collect(self):

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=settings.headless
            )

            page = await browser.new_page(
                viewport={
                    "width": 1440,
                    "height": 1000,
                }
            )

            result = []

            try:

                await page.goto(
                    settings.fabrikant_url,
                    wait_until="domcontentloaded",
                    timeout=settings.browser_timeout_ms,
                )

                for _ in range(
                    settings.max_pages_per_source
                ):

                    html = await page.content()

                    items = self.parse(
                        html
                    )

                    result.extend(items)

                    next_link = await self.next_page(
                        page
                    )

                    if not next_link:
                        break

                    await page.goto(
                        next_link,
                        wait_until="domcontentloaded",
                        timeout=settings.browser_timeout_ms,
                    )

                    await asyncio.sleep(
                        settings.request_delay_seconds
                    )

            finally:

                await browser.close()

            return result

    async def next_page(self, page):

        links = await page.locator(
            "a"
        ).all()

        current = page.url

        for link in links:

            text = (
                await link.inner_text()
            ).strip().lower()

            href = await link.get_attribute(
                "href"
            )

            if (
                href
                and (
                    text == ">"
                    or "след" in text
                    or "next" in text
                )
            ):

                if href.startswith("/"):
                    return (
                        "https://soap2.fabrikant.ru"
                        + href
                    )

                return href

        match = re.search(
            r"page=(\d+)",
            current,
        )

        if match:

            page_no = int(
                match.group(1)
            )

            next_no = page_no + 1

        else:

            next_no = 2

        if "?" in current:

            return re.sub(
                r"page=\d+",
                f"page={next_no}",
                current,
            )

        return (
            current
            + f"?page={next_no}"
        )

    def parse(self, html):

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        result = []

        for row in soup.select(
            "tr"
        ):

            cells = [
                cell.get_text(
                    " ",
                    strip=True,
                )
                for cell in row.select(
                    "td"
                )
            ]

            if len(cells) < 5:
                continue

            text = " ".join(cells)

            match = re.search(
                r"\b(3\d{10,})\b",
                text,
            )

            if not match:
                continue

            notice = match.group(1)

            title = cells[1]

            price = self.parse_price(
                cells[2]
            )

            customer = (
                cells[4]
                if len(cells) > 4
                else None
            )

            published = (
                cells[5]
                if len(cells) > 5
                else None
            )

            deadline = (
                cells[6]
                if len(cells) > 6
                else None
            )

            status = (
                cells[9]
                if len(cells) > 9
                else None
            )

            result.append(
                TenderData(
                    law="223-ФЗ",
                    notice_number=notice,
                    title=title,
                    customer_name=customer,
                    price=price,
                    published_at=self.parse_date(
                        published
                    ),
                    deadline=self.parse_date(
                        deadline
                    ),
                    status=status,
                    source=self.name,
                    external_id=notice,
                )
            )

        return result

    @staticmethod
    def parse_price(value):

        if not value:
            return None

        match = re.search(
            r"([\d\s]+[.,]\d+)",
            value,
        )

        if not match:
            return None

        raw = (
            match.group(1)
            .replace(" ", "")
            .replace(",", ".")
        )

        try:
            return Decimal(raw)

        except Exception:
            return None

    @staticmethod
    def parse_date(value):

        if not value:
            return None

        from dateutil import parser

        try:
            return parser.parse(
                value,
                dayfirst=True,
            )

        except Exception:
            return None
