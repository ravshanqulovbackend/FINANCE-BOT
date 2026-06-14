from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from i18n import t

router = Router()


@router.message(Command("stats"))
async def stats(message: Message, user_service, transaction_service) -> None:
    user = await user_service.get_user(message.from_user.id)
    lang = user["language"] if user else "uz"
    row = await transaction_service.stats(message.from_user.id)
    income = row["income"]
    expense = row["expense"]
    if income == 0 and expense == 0:
        await message.answer(t(lang, "stats_empty"))
        return
    await message.answer(
        t(lang, "stats", income=income, expense=expense, balance=income - expense)
    )
