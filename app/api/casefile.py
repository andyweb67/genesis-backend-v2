# app/api/casefile.py

from fastapi import APIRouter
from app.services.action_report_service import generate_action_report
from app.services.pdf_service import (
    generate_action_report_pdf,
    generate_final_demand_pdf,
    generate_prophet_summary_pdf
)
from app.services.casefile_service import zip_casefile
from app.services.log_service import log_casefile_generation  # <-- added import
import os
from datetime import datetime

router = APIRouter(
    prefix="/casefile",
    tags=["Casefile"]
)

@router.post("/generate")
def generate_casefile(claim_id: int, jurisdiction: str = "Default State", adjuster_behavior: str = "neutral", force: bool = False):
    """
    Generates full Genesis case packet for a claim ID:
    - Action Report PDF
    - Final Demand Letter PDF
    - Prophet Simulation Summary PDF
    - Zipped casefile

    If today's casefile ZIP already exists, skips regeneration unless 'force=True' is set.
    Also logs every generation event.
    """

    today = datetime.now().strftime("%Y-%m-%d")
    zip_filename = f"casefile_{claim_id}_{today}.zip"
    zip_path = os.path.join("casefiles", zip_filename)

    if os.path.exists(zip_path) and not force:
        # Log even skipped generation
        log_casefile_generation(claim_id, jurisdiction, adjuster_behavior, forced=False)
        return {"message": f"Genesis Casefile for Claim ID {claim_id} already generated today."}

    # No valid ZIP found or forced refresh requested
    report = generate_action_report(claim_id, jurisdiction, adjuster_behavior)

    folder_path = f"casefiles/{claim_id}/"
    action_report_path = f"{folder_path}genesis_action_report.pdf"
    final_demand_path = f"{folder_path}final_demand_letter.pdf"
    prophet_summary_path = f"{folder_path}prophet_simulation_summary.pdf"

    # Generate and save PDFs
    generate_action_report_pdf(report, save_path=action_report_path)
    generate_final_demand_pdf(report.get("final_demand_letter", ""), save_path=final_demand_path)
    generate_prophet_summary_pdf(report.get("prophet_simulation", {}), save_path=prophet_summary_path)

    # Create ZIP
    zip_casefile(claim_id)

    # Log successful generation
    log_casefile_generation(claim_id, jurisdiction, adjuster_behavior, forced=force)

    return {"message": f"Genesis Casefile for Claim ID {claim_id} generated successfully."}
