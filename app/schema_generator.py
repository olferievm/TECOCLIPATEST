from __future__ import annotations

from services.csv_schema_parser import grouped_schema, load_lookup_values, load_schema, table_slug
from app.config import LOOKUP_CSV, SCHEMA_CSV, DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USERNAME
from app.database import get_connection
from app.security import hash_password

TYPE_MAP = {
    "date": "TEXT",
    "categorical": "TEXT",
    "text": "TEXT",
    "integer": "INTEGER",
    "numeric": "REAL",
    "primary_key": "TEXT",
}


def initialize_database() -> None:
    definitions = load_schema(SCHEMA_CSV)
    lookups = load_lookup_values(LOOKUP_CSV)
    grouped = grouped_schema(definitions)

    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'registered_user', 'viewer')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS patients (
                subject_id TEXT PRIMARY KEY,
                "group" TEXT,
                enrollment_date TEXT,
                sample_collection_date TEXT,
                gender TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS lookup_values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                value TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                UNIQUE(category, value)
            )
            """
        )

        for table_name, params in grouped.items():
            if table_name == "All tables":
                continue
            slug = f"{table_slug(table_name)}_data"
            columns_sql = []
            for p in params:
                if p.parameter == "subject_id":
                    continue
                sql_type = TYPE_MAP.get(p.data_type, "TEXT")
                columns_sql.append(f'"{p.parameter}" {sql_type}')
            dynamic_cols = ",\n".join(columns_sql)
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {slug} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_id TEXT NOT NULL,
                    {dynamic_cols},
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(subject_id) REFERENCES patients(subject_id) ON DELETE CASCADE
                )
                """
            )

        for category, values in lookups.items():
            for value in values:
                conn.execute(
                    "INSERT OR IGNORE INTO lookup_values (category, value, is_active) VALUES (?, ?, 1)",
                    (category, value),
                )

        existing = conn.execute("SELECT id FROM users WHERE username = ?", (DEFAULT_ADMIN_USERNAME,)).fetchone()
        if not existing:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')",
                (DEFAULT_ADMIN_USERNAME, hash_password(DEFAULT_ADMIN_PASSWORD)),
            )
