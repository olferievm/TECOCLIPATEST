import csv
import io
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response

from services.records_service import get_flat_records

router = APIRouter(prefix="/export", tags=["export"])


def _assert_export_allowed(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if user["role"] not in {"admin", "registered_user"}:
        raise HTTPException(status_code=403, detail="Insufficient role")


@router.get("/csv")
def export_csv(request: Request, q: str = ""):
    _assert_export_allowed(request)
    headers, rows = get_flat_records(q=q)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    for row in rows:
        writer.writerow([row.get(h) for h in headers])

    filename = f"records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/xlsx")
def export_xlsx(request: Request, q: str = ""):
    _assert_export_allowed(request)
    headers, rows = get_flat_records(q=q)

    try:
        from openpyxl import Workbook
    except ImportError as exc:
        raise HTTPException(status_code=500, detail="openpyxl is required for XLSX export") from exc

    wb = Workbook()
    ws = wb.active
    ws.title = "records"
    ws.append(headers)
    for row in rows:
        ws.append([row.get(h) for h in headers])

    buffer = io.BytesIO()
    wb.save(buffer)
    filename = f"records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
