from decimal import Decimal, InvalidOperation

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from i18n import t
from keyboards.inline import cancel_keyboard
from states import LimitForm

router = Router()


async def lang_for(user_service, user_id: int) -> str:
    user = await user_service.get_user(user_id)
    return user["language"] if user else "uz"


@router.message(Command("report"))
async def report(message: Message, user_service, report_service) -> None:
    lang = await lang_for(user_service, message.from_user.id)
    path = await report_service.csv_report(message.from_user.id)
    if path is None:
        await message.answer(t(lang, "report_empty"))
        return
    await message.answer_document(FSInputFile(path), caption=t(lang, "report_ready"))


@router.message(Command("limit"))
async def limit_start(message: Message, state: FSMContext, user_service) -> None:
    lang = await lang_for(user_service, message.from_user.id)
    await state.set_state(LimitForm.amount)
    await message.answer(t(lang, "limit_prompt"), reply_markup=cancel_keyboard(lang))


@router.message(LimitForm.amount)
async def limit_save(message: Message, state: FSMContext, user_service, limit_service) -> None:
    lang = await lang_for(user_service, message.from_user.id)
    try:
        amount = Decimal(message.text.replace(" ", "").replace(",", "."))
        if amount <= 0:
            raise InvalidOperation
    except (InvalidOperation, AttributeError):
        await message.answer(t(lang, "bad_amount"), reply_markup=cancel_keyboard(lang))
        return

    await limit_service.set_limit(message.from_user.id, amount)
    await state.clear()
    await message.answer(t(lang, "limit_saved", amount=amount))


@router.message(Command("monthly"))
async def monthly(message: Message, user_service, transaction_service) -> None:
    lang = await lang_for(user_service, message.from_user.id)
    rows = await transaction_service.monthly_compare(message.from_user.id)
    if not rows:
        await message.answer(t(lang, "monthly_empty"))
        return
    lines = [t(lang, "monthly_title")]
    for row in rows:
        balance = row["income"] - row["expense"]
        lines.append(f"{row['month']}: +{row['income']} / -{row['expense']} / = {balance}")
    await message.answer("\n".join(lines))
