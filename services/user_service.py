from db import queries


class UserService:
    def __init__(self, pool) -> None:
        self.pool = pool

    async def save_user(self, user_id: int, name: str, language: str) -> None:
        async with self.pool.acquire() as conn:
            await queries.upsert_user(conn, user_id, name, language)
            await queries.ensure_default_categories(conn, user_id)

    async def get_user(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await queries.get_user(conn, user_id)
