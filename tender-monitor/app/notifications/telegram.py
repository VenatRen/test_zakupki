from aiogram import Bot
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.config import settings


async def send_tender(tender):

    if not settings.telegram_bot_token:
        return

    if not settings.telegram_chat_id:
        return

    bot = Bot(
        token=settings.telegram_bot_token
    )

    text = f"""
🆕 <b>Новая закупка</b>

<b>223-ФЗ</b>

<b>{tender.title}</b>

ОКПД2: {tender.okpd_code or "не указан"}

Заказчик:
{tender.customer_name or "—"}

НМЦ:
{tender.price or "не указана"}

Регион:
{tender.region or "—"}

Подача до:
{tender.deadline or "—"}

Источник:
{tender.sources[0].source if tender.sources else "—"}

№:
{tender.notice_number or "—"}
""".strip()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔗 Открыть",
                    url=tender.canonical_url
                    or "https://zakupki.gov.ru/",
                )
            ]
        ]
    )

    try:

        await bot.send_message(
            chat_id=settings.telegram_chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )

    finally:

        await bot.session.close()
