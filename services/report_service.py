import csv
from pathlib import Path

from db import queries


class ReportService:
    def __init__(self, pool) -> None:
        self.pool = pool

    async def csv_report(self, user_id: int) -> Path | None:
        async with self.pool.acquire() as conn:
            rows = await queries.report_rows(conn, user_id)
        if not rows:
            return None

        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        path = reports_dir / f"report_{user_id}.csv"
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "type", "amount", "category", "note"])
            for row in rows:
                writer.writerow([row["created_at"], row["type"], row["amount"], row["category_name"], row["note"]])
        return path
