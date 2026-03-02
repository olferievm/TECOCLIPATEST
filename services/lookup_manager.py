from __future__ import annotations

from app.database import get_connection


def get_active_lookup_map() -> dict[str, list[str]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT category, value FROM lookup_values WHERE is_active = 1 ORDER BY category, value"
        ).fetchall()
    lookup: dict[str, list[str]] = {}
    for row in rows:
        lookup.setdefault(row["category"], []).append(row["value"])
    return lookup


def update_lookup_value(category: str, value: str, is_active: bool) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO lookup_values(category, value, is_active) VALUES (?, ?, ?) "
            "ON CONFLICT(category, value) DO UPDATE SET is_active=excluded.is_active",
            (category, value, 1 if is_active else 0),
        )
