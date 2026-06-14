from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from i18n import t

router = Router()


@router.message(Command("history"))
async def history(message: Message, user_service, transaction_service) -> None:
    user = await user_service.get_user(message.from_user.id)
    lang = user["language"] if user else "uz"
    rows = await transaction_service.history(message.from_user.id)
    if not rows:
        await message.answer(t(lang, "history_empty"))
        return

    lines = [t(lang, "history_title")]
    for row in rows:
        sign = "+" if row["type"] == "income" else "-"
        date = row["created_at"].strftime("%d.%m.%Y %H:%M")
        lines.append(f"{date} | {sign}{row['amount']} | {row['category_name'] or '-'} | {row['note'] or '-'}")
    await message.answer("\n".join(lines))
