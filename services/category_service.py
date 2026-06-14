from db import queries


class CategoryService:
    def __init__(self, pool) -> None:
        self.pool = pool

    async def list(self, user_id: int, type_: str | None = None):
        async with self.pool.acquire() as conn:
            return await queries.list_categories(conn, user_id, type_)

    async def add(self, user_id: int, name: str, type_: str) -> None:
        async with self.pool.acquire() as conn:
            await queries.add_category(conn, user_id, name.strip(), type_)

    async def delete(self, user_id: int, category_id: int) -> None:
        async with self.pool.acquire() as conn:
            await queries.delete_category(conn, user_id, category_id)

    async def get(self, user_id: int, category_id: int):
        async with self.pool.acquire() as conn:
            return await queries.get_category(conn, user_id, category_id)
