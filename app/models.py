from __future__ import annotations

from services.csv_schema_parser import load_schema, grouped_schema
from app.config import SCHEMA_CSV


def get_table_definitions() -> dict[str, list[dict[str, str]]]:
    definitions = load_schema(SCHEMA_CSV)
    grouped = grouped_schema(definitions)
    result: dict[str, list[dict[str, str]]] = {}
    for table, params in grouped.items():
        if table == "All tables":
            continue
        result[table] = [
            {
                "parameter": p.parameter,
                "data_type": p.data_type,
                "lookup_category": p.lookup_category,
                "description": p.description,
            }
            for p in params
            if p.parameter != "subject_id"
        ]
    return result
