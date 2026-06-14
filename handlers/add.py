from decimal import Decimal, InvalidOperation

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from i18n import t
from keyboards.inline import cancel_keyboard, categories_keyboard, type_keyboard
from states import AddTransaction

router = Router()


async def user_lang(user_service, user_id: int) -> str:
    user = await user_service.get_user(user_id)
    return user["language"] if user else "uz"


@router.message(Command("add"))
async def add_start(message: Message, state: FSMContext, user_service) -> None:
    lang = await user_lang(user_service, message.from_user.id)
    await state.set_state(AddTransaction.amount)
    await message.answer(t(lang, "amount"), reply_markup=cancel_keyboard(lang))


@router.message(AddTransaction.amount)
async def add_amount(message: Message, state: FSMContext, user_service) -> None:
    lang = await user_lang(user_service, message.from_user.id)
    try:
        amount = Decimal(message.text.replace(" ", "").replace(",", "."))
        if amount <= 0:
            raise InvalidOperation
    except (InvalidOperation, AttributeError):
        await message.answer(t(lang, "bad_amount"), reply_markup=cancel_keyboard(lang))
        return

    await state.update_data(amount=str(amount))
    await state.set_state(AddTransaction.type)
    await message.answer(t(lang, "type"), reply_markup=type_keyboard(lang, "add_type"))


@router.callback_query(AddTransaction.type, F.data.startswith("add_type:"))
async def add_type(callback: CallbackQuery, state: FSMContext, user_service, category_service) -> None:
    lang = await user_lang(user_service, callback.from_user.id)
    type_ = callback.data.split(":", 1)[1]
    categories = await category_service.list(callback.from_user.id, type_)
    if not categories:
        await callback.message.edit_text(t(lang, "no_categories"))
        await state.clear()
        await callback.answer()
        return

    await state.update_data(type=type_)
    await state.set_state(AddTransaction.category)
    await callback.message.edit_text(
        t(lang, "category"),
        reply_markup=categories_keyboard(lang, categories, "add_category"),
    )
    await callback.answer()


@router.callback_query(AddTransaction.category, F.data.startswith("add_category:"))
async def add_category(callback: CallbackQuery, state: FSMContext, user_service) -> None:
    lang = await user_lang(user_service, callback.from_user.id)
    category_id = int(callback.data.split(":", 1)[1])
    await state.update_data(category_id=category_id)
    await state.set_state(AddTransaction.note)
    await callback.message.edit_text(t(lang, "note"), reply_markup=cancel_keyboard(lang))
    await callback.answer()


@router.message(AddTransaction.note)
async def add_note(
    message: Message,
    state: FSMContext,
    user_service,
    category_service,
    transaction_service,
    limit_service,
) -> None:
    lang = await user_lang(user_service, message.from_user.id)
    data = await state.get_data()
    note = None if message.text == "-" else message.text
    category = await category_service.get(message.from_user.id, int(data["category_id"]))

    await transaction_service.add(
        user_id=message.from_user.id,
        category_id=int(data["category_id"]),
        type_=data["type"],
        amount=Decimal(data["amount"]),
        note=note,
    )
    await state.clear()

    type_name = t(lang, data["type"])
    await message.answer(
        t(
            lang,
            "added",
            type_name=type_name,
            amount=data["amount"],
            category=category["name"] if category else "-",
        )
    )
    warning = await limit_service.warning(message.from_user.id)
    if warning:
        limit, expense = warning
        await message.answer(t(lang, "limit_warning", limit=limit, expense=expense))
