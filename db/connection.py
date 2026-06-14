from pathlib import Path

import asyncpg

from config import Config


class Database:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self.pool = await asyncpg.create_pool(
            host=self.config.db_host,
            port=self.config.db_port,
            database=self.config.db_name,
            user=self.config.db_user,
            password=self.config.db_pass,
        )
        await self.migrate()

    async def migrate(self) -> None:
        if self.pool is None:
            raise RuntimeError("Database pool ochilmagan")
        schema = Path("db/schema.sql").read_text(encoding="utf-8")
        async with self.pool.acquire() as conn:
            await conn.execute(schema)

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
