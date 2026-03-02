from __future__ import annotations

from typing import Any

from app.database import get_connection
from app.models import get_table_definitions
from services.csv_schema_parser import table_slug

BASE_COLUMNS = [
    "subject_id",
    "group",
    "enrollment_date",
    "sample_collection_date",
    "gender",
    "created_at",
]


def _safe_order_by(column: str | None) -> str:
    allowed = set(BASE_COLUMNS)
    for _, params in get_table_definitions().items():
        for p in params:
            allowed.add(p["parameter"])
    if column in allowed:
        return column
    return "created_at"


def get_flat_records(q: str = "", order_by: str | None = None, direction: str = "desc") -> tuple[list[str], list[dict[str, Any]]]:
    table_defs = get_table_definitions()

    select_parts = [
        'p.subject_id AS subject_id',
        'p."group" AS "group"',
        'p.enrollment_date AS enrollment_date',
        'p.sample_collection_date AS sample_collection_date',
        'p.gender AS gender',
        'p.created_at AS created_at',
    ]

    join_parts = []
    columns = BASE_COLUMNS.copy()
    seen = set(columns)

    alias_idx = 0
    for table_name, params in table_defs.items():
        alias = f"t{alias_idx}"
        alias_idx += 1
        table_sql = f"{table_slug(table_name)}_data"
        join_parts.append(f"LEFT JOIN {table_sql} {alias} ON {alias}.subject_id = p.subject_id")
        for param in params:
            col = param["parameter"]
            if col in seen:
                continue
            seen.add(col)
            select_parts.append(f'{alias}."{col}" AS "{col}"')
            columns.append(col)

    sql = "SELECT " + ", ".join(select_parts) + " FROM patients p " + " ".join(join_parts)
    params: list[str] = []
    if q:
        sql += ' WHERE p.subject_id LIKE ? OR p."group" LIKE ? OR p.gender LIKE ?'
        needle = f"%{q}%"
        params = [needle, needle, needle]

    order_col = _safe_order_by(order_by)
    order_dir = "ASC" if direction.lower() == "asc" else "DESC"
    sql += f' ORDER BY "{order_col}" {order_dir}'

    with get_connection() as conn:
        rows = [dict(r) for r in conn.execute(sql, params).fetchall()]

    return columns, rows
