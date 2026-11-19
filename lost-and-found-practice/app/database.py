import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "lost_and_found.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS found_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                found_location TEXT NOT NULL,
                found_date TEXT NOT NULL,
                description TEXT DEFAULT '',
                storage_location TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT '보관 중',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

