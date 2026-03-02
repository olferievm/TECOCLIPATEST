from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

import sqlite3

from app.database import get_connection
from app.models import get_table_definitions
from services.csv_schema_parser import table_slug
from services.lookup_manager import get_active_lookup_map

router = APIRouter(prefix="/patients", tags=["patients"])
templates = Jinja2Templates(directory="templates")


def require_user(request: Request):
    if "user" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
    return None


@router.get("/new")
def new_patient(request: Request):
    redirect = require_user(request)
    if redirect:
        return redirect
    tables = get_table_definitions()
    lookups = get_active_lookup_map()
    return templates.TemplateResponse(
        "wizard.html",
        {"request": request, "tables": tables, "lookups": lookups, "error": None},
    )


@router.post("/new")
async def create_patient(request: Request):
    redirect = require_user(request)
    if redirect:
        return redirect

    form = await request.form()
    subject_id = str(form.get("subject_id", "")).strip()
    if not subject_id:
        tables = get_table_definitions()
        lookups = get_active_lookup_map()
        return templates.TemplateResponse(
            "wizard.html",
            {"request": request, "tables": tables, "lookups": lookups, "error": "Subject ID is required."},
            status_code=400,
        )

    table_defs = get_table_definitions()
    try:
        with get_connection() as conn:
            conn.execute(
            'INSERT INTO patients (subject_id, "group", enrollment_date, sample_collection_date, gender) VALUES (?, ?, ?, ?, ?)',
            (
                subject_id,
                form.get("group", None),
                form.get("enrollment_date", None),
                form.get("sample_collection_date", None),
                form.get("gender", None),
            ),
        )

            for table, params in table_defs.items():
                slug = f"{table_slug(table)}_data"
                columns = ["subject_id"]
                values = [subject_id]
                for param in params:
                    columns.append(param["parameter"])
                    values.append(form.get(param["parameter"], None))
                placeholders = ", ".join(["?"] * len(columns))
                quoted_cols = ", ".join([f'"{c}"' for c in columns])
                conn.execute(f"INSERT INTO {slug} ({quoted_cols}) VALUES ({placeholders})", values)
    except sqlite3.IntegrityError:
        tables = get_table_definitions()
        lookups = get_active_lookup_map()
        return templates.TemplateResponse(
            "wizard.html",
            {"request": request, "tables": tables, "lookups": lookups, "error": f"Subject ID {subject_id} already exists."},
            status_code=400,
        )

    return RedirectResponse(url="/", status_code=303)
