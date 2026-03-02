from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class ParameterDefinition:
    parameter: str
    table: str
    data_type: str
    lookup_category: str
    description: str


def load_schema(csv_path: Path) -> list[ParameterDefinition]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [
        ParameterDefinition(
            parameter=r["parameter"].strip(),
            table=r["table"].strip(),
            data_type=r["data_type"].strip().lower(),
            lookup_category=r.get("lookup_category", "").strip(),
            description=r.get("description", "").strip(),
        )
        for r in rows
    ]


def load_lookup_values(csv_path: Path) -> dict[str, list[str]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    values: dict[str, list[str]] = {}
    for row in rows:
        category = row["category"].strip()
        value = row["value"].strip()
        values.setdefault(category, [])
        if value not in values[category]:
            values[category].append(value)
    return values


def table_slug(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def grouped_schema(definitions: Iterable[ParameterDefinition]) -> dict[str, list[ParameterDefinition]]:
    grouped: dict[str, list[ParameterDefinition]] = {}
    for d in definitions:
        grouped.setdefault(d.table, []).append(d)
    return grouped
