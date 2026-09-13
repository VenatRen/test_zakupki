from playwright.async_api import async_playwright

from app.config import settings

from .base import (
    BaseCollector,
    TenderData,
)


class TektorgCollector(
    BaseCollector
):

    name = "tektorg"

    async def healthcheck(self):

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            page = await browser.new_page()

            try:

                response = await page.goto(
                    settings.tektorg_url,
                    wait_until="domcontentloaded",
                    timeout=settings.browser_timeout_ms,
                )

                return bool(
                    response
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

            page = await browser.new_page()

            try:

                await page.goto(
                    settings.tektorg_url,
                    wait_until="domcontentloaded",
                    timeout=settings.browser_timeout_ms,
                )

                return []

            finally:

                await browser.close()
