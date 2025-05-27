from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_tasks_pdf(tasks: list) -> bytes:
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y, "Your Tasks")
    y -= 40

    p.setFont("Helvetica", 12)
    for task in tasks:
        p.drawString(40, y, f"• {task.title} | {task.description} | Due: {task.due_date or 'N/A'} | Status: {task.status}")
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 40

    p.save()
    buffer.seek(0)
    return buffer.read()
