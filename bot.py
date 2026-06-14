import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties

from config import load_config
from db.connection import Database
from handlers import routers
from services.category_service import CategoryService
from services.limit_service import LimitService
from services.report_service import ReportService
from services.transaction_service import TransactionService
from services.user_service import UserService


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    database = Database(config)
    await database.connect()
    if database.pool is None:
        raise RuntimeError("Database pool ochilmadi")

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    user_service = UserService(database.pool)
    category_service = CategoryService(database.pool)
    transaction_service = TransactionService(database.pool)
    report_service = ReportService(database.pool)
    limit_service = LimitService(database.pool)

    dp["user_service"] = user_service
    dp["category_service"] = category_service
    dp["transaction_service"] = transaction_service
    dp["report_service"] = report_service
    dp["limit_service"] = limit_service

    for router in routers:
        dp.include_router(router)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start / Til tanlash"),
            BotCommand(command="add", description="Tranzaksiya qo'shish"),
            BotCommand(command="stats", description="Oylik statistika"),
            BotCommand(command="history", description="Oxirgi 10 ta yozuv"),
            BotCommand(command="categories", description="Kategoriyalar"),
            BotCommand(command="report", description="CSV hisobot"),
            BotCommand(command="limit", description="Oylik limit"),
            BotCommand(command="monthly", description="3 oy taqqoslash"),
        ]
    )

    try:
        await dp.start_polling(bot)
    finally:
        await database.close()


if __name__ == "__main__":
    asyncio.run(main())
# source venv/bin/activate
# python3 bot.py


# deactivate
# rm -rf venv
# /opt/homebrew/bin/python3.12 -m venv venv
# source venv/bin/activate
# python --version
# python -m pip install --upgrade pip
# python -m pip install -r requirements.txt
# python bot.py

# python3 bot.py