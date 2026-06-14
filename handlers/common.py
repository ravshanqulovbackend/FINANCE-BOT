from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from i18n import t

router = Router()


@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext, user_service) -> None:
    await state.clear()
    user = await user_service.get_user(callback.from_user.id)
    lang = user["language"] if user else "uz"
    await callback.message.edit_text(t(lang, "cancelled"))
    await callback.answer()
