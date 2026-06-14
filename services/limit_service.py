from decimal import Decimal

from db import queries


class LimitService:
    def __init__(self, pool) -> None:
        self.pool = pool

    async def set_limit(self, user_id: int, amount: Decimal) -> None:
        async with self.pool.acquire() as conn:
            await queries.set_limit(conn, user_id, amount)

    async def warning(self, user_id: int) -> tuple[Decimal, Decimal] | None:
        async with self.pool.acquire() as conn:
            user = await queries.get_user(conn, user_id)
            stats = await queries.month_stats(conn, user_id)
        if not user or user["monthly_limit"] is None:
            return None
        expense = Decimal(stats["expense"])
        limit = Decimal(user["monthly_limit"])
        if expense > limit:
            return limit, expense
        return None
