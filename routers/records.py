from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.records_service import get_flat_records

router = APIRouter(tags=["records"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def dashboard(request: Request, q: str = "", sort: str = "created_at", direction: str = "desc"):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    columns, rows = get_flat_records(q=q, order_by=sort, direction=direction)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "rows": rows, "columns": columns, "q": q, "user": user, "sort": sort, "direction": direction},
    )
