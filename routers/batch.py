# /routers/batch.py

from fastapi import APIRouter, Depends, Response
from models.request_models import BatchAuditRequest
from services.ai_handler import smart_ai_call
from services.pdf_generator import generate_audit_pdf
from dependencies.security import verify_api_key
import asyncio

router = APIRouter(
    prefix="/batch",
    tags=["Batch"]
)

async def audit_single_claim_with_status(claim):
    """
    Helper function to audit a single claim asynchronously with status tracking.
    """
    claim_status = {
        "claim_id": claim.claim_id,
        "status": "Processing",
        "audit_result": None
    }
    
    prompt = (
        f"Audit the following claim:\n\n"
        f"Claim ID: {claim.claim_id}\n"
        f"Damages Summary: {claim.damages_summary}\n\n"
        f"Identify potential undervaluation or suppression issues, using Genesis standards."
    )
    
    result = smart_ai_call(prompt, use_model="gpt", temperature=0.2)
    
    claim_status["audit_result"] = result
    claim_status["status"] = "Completed"
    
    return claim_status

@router.post("/audit", dependencies=[Depends(verify_api_key)])
async def batch_audit(request: BatchAuditRequest):
    """
    Processes multiple claim audits in parallel with real-time status tracking.
    """
    tasks = [asyncio.to_thread(audit_single_claim_with_status, claim) for claim in request.claims]
    audit_statuses = await asyncio.gather(*tasks)
    
    return {"batch_audit_status": audit_statuses}

@router.post("/download_audit_report", dependencies=[Depends(verify_api_key)])
async def download_audit_report(claim_id: str, damages_summary: str, audit_result: str):
    """
    Generate and download a PDF audit report for a single claim.
    """
    pdf_bytes = generate_audit_pdf(claim_id, damages_summary, audit_result)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={claim_id}_audit_report.pdf"
    })
