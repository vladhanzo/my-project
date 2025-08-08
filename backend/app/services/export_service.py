from fastapi import APIRouter, Body, Response
from openpyxl import Workbook
from io import BytesIO
from weasyprint import HTML

router = APIRouter()

def export_excel(data: list[list]):
    wb = Workbook()
    ws = wb.active
    for row in data:
        ws.append(row)
    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()

def export_pdf(html_content: str):
    return HTML(string=html_content).write_pdf()

@router.post("/export")
def export(
    format: str = Body(..., embed=True),
    data: list[list] | None = Body(None, embed=True),
    html: str | None = Body(None, embed=True)
):
    if format == "xlsx":
        content = export_excel(data)  # data required for Excel
        return Response(
            content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=export.xlsx"}
        )
    content = export_pdf(html)  # html required for PDF
    return Response(
        content,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=export.pdf"}
    )
