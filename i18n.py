DEFAULT_LANG = "uz"
LANGS = {"uz", "ru"}

TEXTS = {
    "uz": {
        "choose_language": "Tilni tanlang:",
        "language_saved": "Til saqlandi. Xush kelibsiz, {name}!",
        "welcome_back": "Xush kelibsiz, {name}! Quyidagi komandalar orqali botdan foydalaning.",
        "menu": (
            "/add - tranzaksiya qo'shish\n"
            "/stats - oylik statistika\n"
            "/history - oxirgi 10 ta yozuv\n"
            "/categories - kategoriyalar\n"
            "/report - CSV hisobot\n"
            "/limit - oylik limit\n"
            "/monthly - oxirgi 3 oy taqqoslash"
        ),
        "cancel": "Bekor qilish",
        "cancelled": "Bekor qilindi.",
        "amount": "Summani kiriting:",
        "bad_amount": "Summa noto'g'ri. Masalan: 45000",
        "type": "Turini tanlang:",
        "income": "Daromad",
        "expense": "Xarajat",
        "category": "Kategoriyani tanlang:",
        "no_categories": "Bu tur uchun kategoriya yo'q. Avval /categories orqali qo'shing.",
        "note": "Izoh kiriting yoki '-' yuboring:",
        "added": "Saqlandi: {type_name} {amount} so'm, kategoriya: {category}",
        "stats_empty": "Bu oy uchun yozuvlar yo'q.",
        "stats": "Oy statistikasi:\nDaromad: {income} so'm\nXarajat: {expense} so'm\nQoldiq: {balance} so'm",
        "history_empty": "Hali tranzaksiyalar yo'q.",
        "history_title": "Oxirgi tranzaksiyalar:",
        "categories_title": "Kategoriyalar:",
        "category_menu": "Kategoriyalarni boshqarish:",
        "add_category_type": "Qaysi tur uchun kategoriya qo'shasiz?",
        "category_name": "Kategoriya nomini kiriting:",
        "category_added": "Kategoriya qo'shildi: {name}",
        "delete_category": "O'chiriladigan kategoriyani tanlang:",
        "category_deleted": "Kategoriya o'chirildi.",
        "add_category": "Qo'shish",
        "delete": "O'chirish",
        "back": "Orqaga",
        "report_empty": "Hisobot uchun ma'lumot topilmadi.",
        "report_ready": "CSV hisobot tayyor.",
        "limit_prompt": "Oylik xarajat limitini kiriting:",
        "limit_saved": "Limit saqlandi: {amount} so'm",
        "limit_warning": "Diqqat: bu oy xarajat limitingizdan oshdi. Limit: {limit} so'm, xarajat: {expense} so'm",
        "monthly_empty": "Oxirgi 3 oy uchun ma'lumot yetarli emas.",
        "monthly_title": "Oxirgi 3 oy taqqoslash:",
    },
    "ru": {
        "choose_language": "Выберите язык:",
        "language_saved": "Язык сохранен. Добро пожаловать, {name}!",
        "welcome_back": "Добро пожаловать, {name}! Используйте команды ниже.",
        "menu": (
            "/add - добавить транзакцию\n"
            "/stats - статистика за месяц\n"
            "/history - последние 10 записей\n"
            "/categories - категории\n"
            "/report - CSV отчет\n"
            "/limit - месячный лимит\n"
            "/monthly - сравнение за 3 месяца"
        ),
        "cancel": "Отмена",
        "cancelled": "Отменено.",
        "amount": "Введите сумму:",
        "bad_amount": "Неверная сумма. Например: 45000",
        "type": "Выберите тип:",
        "income": "Доход",
        "expense": "Расход",
        "category": "Выберите категорию:",
        "no_categories": "Для этого типа нет категорий. Добавьте через /categories.",
        "note": "Введите комментарий или отправьте '-':",
        "added": "Сохранено: {type_name} {amount} сум, категория: {category}",
        "stats_empty": "За этот месяц записей нет.",
        "stats": "Статистика месяца:\nДоход: {income} сум\nРасход: {expense} сум\nБаланс: {balance} сум",
        "history_empty": "Транзакций пока нет.",
        "history_title": "Последние транзакции:",
        "categories_title": "Категории:",
        "category_menu": "Управление категориями:",
        "add_category_type": "Для какого типа добавить категорию?",
        "category_name": "Введите название категории:",
        "category_added": "Категория добавлена: {name}",
        "delete_category": "Выберите категорию для удаления:",
        "category_deleted": "Категория удалена.",
        "add_category": "Добавить",
        "delete": "Удалить",
        "back": "Назад",
        "report_empty": "Нет данных для отчета.",
        "report_ready": "CSV отчет готов.",
        "limit_prompt": "Введите месячный лимит расходов:",
        "limit_saved": "Лимит сохранен: {amount} сум",
        "limit_warning": "Внимание: расходы за месяц превысили лимит. Лимит: {limit} сум, расход: {expense} сум",
        "monthly_empty": "Недостаточно данных за последние 3 месяца.",
        "monthly_title": "Сравнение за последние 3 месяца:",
    },
}


def t(lang: str | None, key: str, **kwargs) -> str:
    safe_lang = lang if lang in LANGS else DEFAULT_LANG
    return TEXTS[safe_lang][key].format(**kwargs)
