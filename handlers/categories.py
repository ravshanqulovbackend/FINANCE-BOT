from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from i18n import t
from keyboards.inline import categories_keyboard, category_menu_keyboard, type_keyboard
from states import CategoryForm

router = Router()


async def lang_for(user_service, user_id: int) -> str:
    user = await user_service.get_user(user_id)
    return user["language"] if user else "uz"


@router.message(Command("categories"))
async def categories(message: Message, user_service, category_service) -> None:
    lang = await lang_for(user_service, message.from_user.id)
    rows = await category_service.list(message.from_user.id)
    lines = [t(lang, "categories_title")]
    for row in rows:
        lines.append(f"- {t(lang, row['type'])}: {row['name']}")
    await message.answer("\n".join(lines), reply_markup=category_menu_keyboard(lang))


@router.callback_query(F.data == "cat:add")
async def category_add_start(callback: CallbackQuery, state: FSMContext, user_service) -> None:
    lang = await lang_for(user_service, callback.from_user.id)
    await state.set_state(CategoryForm.type)
    await callback.message.edit_text(t(lang, "add_category_type"), reply_markup=type_keyboard(lang, "cat_type"))
    await callback.answer()


@router.callback_query(CategoryForm.type, F.data.startswith("cat_type:"))
async def category_type(callback: CallbackQuery, state: FSMContext, user_service) -> None:
    lang = await lang_for(user_service, callback.from_user.id)
    await state.update_data(type=callback.data.split(":", 1)[1])
    await state.set_state(CategoryForm.name)
    await callback.message.edit_text(t(lang, "category_name"))
    await callback.answer()


@router.message(CategoryForm.name)
async def category_name(message: Message, state: FSMContext, user_service, category_service) -> None:
    lang = await lang_for(user_service, message.from_user.id)
    data = await state.get_data()
    await category_service.add(message.from_user.id, message.text, data["type"])
    await state.clear()
    await message.answer(t(lang, "category_added", name=message.text))


@router.callback_query(F.data == "cat:delete")
async def category_delete_start(callback: CallbackQuery, user_service, category_service) -> None:
    lang = await lang_for(user_service, callback.from_user.id)
    rows = await category_service.list(callback.from_user.id)
    await callback.message.edit_text(
        t(lang, "delete_category"),
        reply_markup=categories_keyboard(lang, rows, "cat_delete"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cat_delete:"))
async def category_delete(callback: CallbackQuery, user_service, category_service) -> None:
    lang = await lang_for(user_service, callback.from_user.id)
    category_id = int(callback.data.split(":", 1)[1])
    await category_service.delete(callback.from_user.id, category_id)
    await callback.message.edit_text(t(lang, "category_deleted"))
    await callback.answer()
