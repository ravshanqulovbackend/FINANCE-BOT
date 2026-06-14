from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from i18n import t


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="O'zbekcha", callback_data="lang:uz"),
                InlineKeyboardButton(text="Русский", callback_data="lang:ru"),
            ]
        ]
    )


def cancel_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t(lang, "cancel"), callback_data="cancel")]]
    )


def type_keyboard(lang: str, prefix: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "income"), callback_data=f"{prefix}:income"),
                InlineKeyboardButton(text=t(lang, "expense"), callback_data=f"{prefix}:expense"),
            ],
            [InlineKeyboardButton(text=t(lang, "cancel"), callback_data="cancel")],
        ]
    )


def categories_keyboard(lang: str, categories, prefix: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=row["name"], callback_data=f"{prefix}:{row['id']}")]
        for row in categories
    ]
    rows.append([InlineKeyboardButton(text=t(lang, "cancel"), callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def category_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "add_category"), callback_data="cat:add"),
                InlineKeyboardButton(text=t(lang, "delete"), callback_data="cat:delete"),
            ]
        ]
    )
