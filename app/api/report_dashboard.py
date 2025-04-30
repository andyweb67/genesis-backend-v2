# app/api/report_dashboard.py

from fastapi import APIRouter
from app.services.claim_service import claims_db
from app.services.file_naming_service import (
    get_casefile_folder,
    get_report_filename,
    get_final_demand_filename,
    get_prophet_summary_filename,
    get_full_path
)
import os

router = APIRouter()

@router.get("/report/summary")
def report_summary():
    summary = []

    for claim in claims_db:
        claim_id = claim.claim_id
        claim_number = claim.claim_number
        folder = get_casefile_folder(claim_id)

        entry = {
            "claim_id": claim_id,
            "claim_number": claim_number,
            "claimant_name": claim.claimant_name,
            "rrt_md": os.path.exists(get_full_path(claim_id, get_report_filename(claim_number, "md"))),
            "rrt_pdf": os.path.exists(get_full_path(claim_id, get_report_filename(claim_number, "pdf"))),
            "final_demand": os.path.exists(get_full_path(claim_id, get_final_demand_filename(claim_number))),
            "prophet_summary": os.path.exists(get_full_path(claim_id, get_prophet_summary_filename(claim_number))),
            "zip_ready": all([
                os.path.exists(get_full_path(claim_id, get_report_filename(claim_number, "md"))),
                os.path.exists(get_full_path(claim_id, get_report_filename(claim_number, "pdf"))),
                os.path.exists(get_full_path(claim_id, get_final_demand_filename(claim_number))),
                os.path.exists(get_full_path(claim_id, get_prophet_summary_filename(claim_number)))
            ])
        }
        summary.append(entry)

    return summary
