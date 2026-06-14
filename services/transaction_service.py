from decimal import Decimal

from db import queries


class TransactionService:
    def __init__(self, pool) -> None:
        self.pool = pool

    async def add(self, user_id: int, category_id: int, type_: str, amount: Decimal, note: str | None) -> None:
        async with self.pool.acquire() as conn:
            await queries.add_transaction(conn, user_id, category_id, type_, amount, note)

    async def stats(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await queries.month_stats(conn, user_id)

    async def history(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await queries.history(conn, user_id)

    async def monthly_compare(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await queries.monthly_compare(conn, user_id)
