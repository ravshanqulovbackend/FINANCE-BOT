from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str


def load_config() -> Config:
    token = getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN .env faylda berilmagan")

    return Config(
        bot_token=token,
        db_host=getenv("DB_HOST", "localhost"),
        db_port=int(getenv("DB_PORT", "5432")),
        db_name=getenv("DB_NAME", "finance_bot"),
        db_user=getenv("DB_USER", "botuser"),
        db_pass=getenv("DB_PASS", ""),
    )
