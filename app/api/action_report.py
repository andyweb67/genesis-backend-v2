from fastapi.responses import StreamingResponse
from app.services.action_report_service import generate_action_report
from app.services.pdf_service import (
    generate_action_report_pdf,
    generate_final_demand_pdf,
    generate_prophet_summary_pdf
)
from app.services.casefile_service import zip_casefile  # <-- ADD THIS
import io

@router.post("/report/pdf")
def generate_action_report_pdf_route(claim_id: int, jurisdiction: str = "Default State", adjuster_behavior: str = "neutral"):
    # Generate full Genesis Action Report dictionary
    report = generate_action_report(claim_id, jurisdiction, adjuster_behavior)

    # Define file save paths
    folder_path = f"casefiles/{claim_id}/"
    action_report_path = f"{folder_path}genesis_action_report.pdf"
    final_demand_path = f"{folder_path}final_demand_letter.pdf"
    prophet_summary_path = f"{folder_path}prophet_simulation_summary.pdf"

    # Generate and save all three PDFs
    generate_action_report_pdf(report, save_path=action_report_path)
    generate_final_demand_pdf(report.get("final_demand_letter", ""), save_path=final_demand_path)
    generate_prophet_summary_pdf(report.get("prophet_simulation", {}), save_path=prophet_summary_path)

    # NEW: Automatically zip the casefile folder
    zip_casefile(claim_id)

    # Return the Genesis Action Report PDF for immediate download
    return StreamingResponse(open(action_report_path, "rb"), media_type="application/pdf",
                              headers={"Content-Disposition": f"attachment; filename=genesis_action_report_{claim_id}.pdf"})
