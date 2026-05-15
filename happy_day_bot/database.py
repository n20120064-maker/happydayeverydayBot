import aiosqlite
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


class Database:
    def __init__(self, path: str) -> None:
        self.path = path

    async def init(self) -> None:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.path) as db:
            await db.execute("PRAGMA foreign_keys = ON")
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL UNIQUE,
                    name TEXT,
                    communication_style TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS diary_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    mood TEXT NOT NULL,
                    wins TEXT NOT NULL,
                    gratitude TEXT NOT NULL,
                    difficulties TEXT NOT NULL,
                    support_type TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """
            )
            await db.commit()

    async def upsert_user(self, telegram_id: int, name: str | None = None, communication_style: str | None = None) -> int:
        now = datetime.utcnow().isoformat()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute(
                """
                INSERT INTO users (telegram_id, name, communication_style, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(telegram_id) DO UPDATE SET
                    name = COALESCE(excluded.name, users.name),
                    communication_style = COALESCE(excluded.communication_style, users.communication_style)
                """,
                (telegram_id, name, communication_style, now),
            )
            await db.commit()
            cursor = await db.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
            row = await cursor.fetchone()
            return int(row["id"])

    async def get_user_by_telegram_id(self, telegram_id: int) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def list_users(self) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            rows = await db.execute_fetchall("SELECT * FROM users")
            return [dict(row) for row in rows]

    async def add_diary_entry(
        self,
        user_id: int,
        mood: str,
        wins: str,
        gratitude: str,
        difficulties: str,
        support_type: str,
        ai_response: str,
    ) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                """
                INSERT INTO diary_entries
                    (user_id, date, mood, wins, gratitude, difficulties, support_type, ai_response, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    date.today().isoformat(),
                    mood,
                    wins,
                    gratitude,
                    difficulties,
                    support_type,
                    ai_response,
                    datetime.utcnow().isoformat(),
                ),
            )
            await db.commit()

    async def get_recent_entries(self, telegram_id: int, limit: int = 5) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            rows = await db.execute_fetchall(
                """
                SELECT diary_entries.*
                FROM diary_entries
                JOIN users ON users.id = diary_entries.user_id
                WHERE users.telegram_id = ?
                ORDER BY diary_entries.created_at DESC
                LIMIT ?
                """,
                (telegram_id, limit),
            )
            return [dict(row) for row in rows]

    async def get_week_entries(self, telegram_id: int) -> list[dict[str, Any]]:
        week_ago = (date.today() - timedelta(days=6)).isoformat()
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            rows = await db.execute_fetchall(
                """
                SELECT diary_entries.*
                FROM diary_entries
                JOIN users ON users.id = diary_entries.user_id
                WHERE users.telegram_id = ? AND diary_entries.date >= ?
                ORDER BY diary_entries.date ASC, diary_entries.created_at ASC
                """,
                (telegram_id, week_ago),
            )
            return [dict(row) for row in rows]
