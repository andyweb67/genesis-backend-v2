# app/services/pdf_service.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
from markdown import markdown
from weasyprint import HTML
from app.services.file_naming_service import get_casefile_folder, get_full_path, get_report_filename

def generate_action_report_pdf(report_data: dict, save_path: str = None) -> bytes:
    """
    Generates the Genesis Action Report PDF.
    Optionally saves it to disk if save_path is provided.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(30, height - 50, "Genesis Action Report")

    p.setFont("Helvetica", 10)
    y = height - 80

    def draw_line(text):
        nonlocal y
        if y < 50:
            p.showPage()
            y = height - 50
        p.drawString(30, y, text)
        y -= 15

    # Section 1: Claim Info
    draw_line("Claim Info:")
    for key, value in report_data.get("claim_info", {}).items():
        draw_line(f"- {key}: {value}")

    # Section 2: Audit Summary
    draw_line("\nAudit Summary:")
    for finding in report_data.get("audit_summary", {}).get("audit_findings", []):
        draw_line(f"- {finding}")

    # Section 3: ZAP Rebuttals
    draw_line("\nZAP Rebuttals:")
    for zap in report_data.get("zap_rebuttals", []):
        rebuttal = zap.get("zap_rebuttal", "N/A")
        draw_line(f"- {rebuttal}")

    # Section 4: Escalation Decision
    draw_line("\nEscalation Decision:")
    draw_line(f"- {report_data.get('escalation_decision', {}).get('recommendation', 'N/A')}")

    # Section 5: Prophet Simulation
    draw_line("\nProphet Simulation:")
    draw_line(f"- {report_data.get('prophet_simulation', {}).get('recommendation', 'N/A')}")

    # Suppression alerts (if any)
    alerts = report_data.get("prophet_simulation", {}).get("suppression_alerts", [])
    if alerts:
        draw_line("\n⚠️ Suppression Alerts Detected:")
        for alert in alerts:
            draw_line(f"- {alert}")

    p.showPage()
    p.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(pdf_data)

    return pdf_data

def generate_final_demand_pdf(final_demand_text: str, save_path: str) -> None:
    """
    Generates a PDF for the Final Demand Letter.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, height - 50, "Final Demand Letter")

    p.setFont("Helvetica", 10)
    y = height - 80

    for line in final_demand_text.splitlines():
        if y < 50:
            p.showPage()
            y = height - 50
        p.drawString(30, y, line.strip())
        y -= 15

    p.showPage()
    p.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    with open(save_path, "wb") as f:
        f.write(pdf_data)

def generate_prophet_summary_pdf(prophet_data: dict, save_path: str) -> None:
    """
    Generates a PDF summarizing Prophet Litigation Simulation.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, height - 50, "Prophet Litigation Simulation Summary")

    p.setFont("Helvetica", 10)
    y = height - 80

    def draw_line(text):
        nonlocal y
        if y < 50:
            p.showPage()
            y = height - 50
        p.drawString(30, y, text)
        y -= 15

    draw_line(f"Claim ID: {prophet_data.get('claim_id')}")
    draw_line(f"Audit Score: {prophet_data.get('audit_score')}")
    draw_line(f"Suppression Alert: {prophet_data.get('suppression_alert')}")
    draw_line(f"Adjuster Behavior: {prophet_data.get('adjuster_behavior')}")
    draw_line(f"Estimated Jury Risk Score: {prophet_data.get('estimated_jury_risk_score')}")
    draw_line(f"Recommendation: {prophet_data.get('recommendation')}")

    if prophet_data.get("suppression_alerts"):
        draw_line("\n⚠️ Suppression Alerts Detected:")
        for alert in prophet_data["suppression_alerts"]:
            draw_line(f"- {alert}")

    p.showPage()
    p.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    with open(save_path, "wb") as f:
        f.write(pdf_data)

def convert_markdown_to_pdf(markdown_path: str) -> str:
    """
    Converts a Markdown file to PDF using WeasyPrint and Markdown rendering.
    """
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    with open(markdown_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown(md_content, extensions=["tables", "fenced_code"])

    output_dir = os.path.dirname(markdown_path)
    os.makedirs(output_dir, exist_ok=True)

    pdf_path = markdown_path.replace(".md", ".pdf")
    HTML(string=html_content).write_pdf(pdf_path)

    return pdf_path
