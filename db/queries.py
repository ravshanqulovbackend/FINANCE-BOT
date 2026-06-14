from decimal import Decimal

import asyncpg


async def upsert_user(conn: asyncpg.Connection, user_id: int, name: str, language: str) -> None:
    await conn.execute(
        """
        INSERT INTO users (id, name, language)
        VALUES ($1, $2, $3)
        ON CONFLICT (id) DO UPDATE SET name = $2, language = $3
        """,
        user_id,
        name,
        language,
    )


async def get_user(conn: asyncpg.Connection, user_id: int) -> asyncpg.Record | None:
    return await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)


async def ensure_default_categories(conn: asyncpg.Connection, user_id: int) -> None:
    defaults = [
        ("Ish haqi", "income"),
        ("Stipendiya", "income"),
        ("Qo'shimcha daromad", "income"),
        ("Ovqat", "expense"),
        ("Transport", "expense"),
        ("Kommunal", "expense"),
        ("Internet", "expense"),
    ]
    await conn.executemany(
        """
        INSERT INTO categories (user_id, name, type)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id, name, type) DO NOTHING
        """,
        [(user_id, name, type_) for name, type_ in defaults],
    )


async def list_categories(conn: asyncpg.Connection, user_id: int, type_: str | None = None) -> list[asyncpg.Record]:
    if type_:
        return await conn.fetch(
            "SELECT * FROM categories WHERE user_id = $1 AND type = $2 ORDER BY name",
            user_id,
            type_,
        )
    return await conn.fetch(
        "SELECT * FROM categories WHERE user_id = $1 ORDER BY type, name",
        user_id,
    )


async def add_category(conn: asyncpg.Connection, user_id: int, name: str, type_: str) -> None:
    await conn.execute(
        """
        INSERT INTO categories (user_id, name, type)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id, name, type) DO NOTHING
        """,
        user_id,
        name,
        type_,
    )


async def delete_category(conn: asyncpg.Connection, user_id: int, category_id: int) -> None:
    await conn.execute(
        "DELETE FROM categories WHERE id = $1 AND user_id = $2",
        category_id,
        user_id,
    )


async def get_category(conn: asyncpg.Connection, user_id: int, category_id: int) -> asyncpg.Record | None:
    return await conn.fetchrow(
        "SELECT * FROM categories WHERE id = $1 AND user_id = $2",
        category_id,
        user_id,
    )


async def add_transaction(
    conn: asyncpg.Connection,
    user_id: int,
    category_id: int,
    type_: str,
    amount: Decimal,
    note: str | None,
) -> None:
    await conn.execute(
        """
        INSERT INTO transactions (user_id, category_id, type, amount, note)
        VALUES ($1, $2, $3, $4, $5)
        """,
        user_id,
        category_id,
        type_,
        amount,
        note,
    )


async def month_stats(conn: asyncpg.Connection, user_id: int) -> asyncpg.Record:
    return await conn.fetchrow(
        """
        SELECT
            COALESCE(SUM(amount) FILTER (WHERE type = 'income'), 0) AS income,
            COALESCE(SUM(amount) FILTER (WHERE type = 'expense'), 0) AS expense
        FROM transactions
        WHERE user_id = $1
          AND created_at >= date_trunc('month', NOW())
          AND created_at < date_trunc('month', NOW()) + interval '1 month'
        """,
        user_id,
    )


async def history(conn: asyncpg.Connection, user_id: int, limit: int = 10) -> list[asyncpg.Record]:
    return await conn.fetch(
        """
        SELECT t.*, c.name AS category_name
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.user_id = $1
        ORDER BY t.created_at DESC
        LIMIT $2
        """,
        user_id,
        limit,
    )


async def report_rows(conn: asyncpg.Connection, user_id: int) -> list[asyncpg.Record]:
    return await conn.fetch(
        """
        SELECT t.created_at, t.type, t.amount, COALESCE(c.name, '-') AS category_name, COALESCE(t.note, '') AS note
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.user_id = $1
        ORDER BY t.created_at DESC
        """,
        user_id,
    )


async def set_limit(conn: asyncpg.Connection, user_id: int, amount: Decimal) -> None:
    await conn.execute("UPDATE users SET monthly_limit = $2 WHERE id = $1", user_id, amount)


async def monthly_compare(conn: asyncpg.Connection, user_id: int) -> list[asyncpg.Record]:
    return await conn.fetch(
        """
        SELECT to_char(date_trunc('month', created_at), 'YYYY-MM') AS month,
               COALESCE(SUM(amount) FILTER (WHERE type = 'income'), 0) AS income,
               COALESCE(SUM(amount) FILTER (WHERE type = 'expense'), 0) AS expense
        FROM transactions
        WHERE user_id = $1
          AND created_at >= date_trunc('month', NOW()) - interval '2 month'
        GROUP BY date_trunc('month', created_at)
        ORDER BY month DESC
        """,
        user_id,
    )
