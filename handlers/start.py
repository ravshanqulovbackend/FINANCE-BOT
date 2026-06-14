from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from i18n import t
from keyboards.inline import language_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(t("uz", "choose_language"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery, user_service) -> None:
    lang = callback.data.split(":", 1)[1]
    name = callback.from_user.full_name
    await user_service.save_user(callback.from_user.id, name, lang)
    await callback.message.edit_text(
        f"{t(lang, 'language_saved', name=name)}\n\n{t(lang, 'menu')}"
    )
    await callback.answer()
