# --- routers/claims.py ---

from fastapi import APIRouter
from models.claim_models import ClaimUpload, AdjusterResponse, CallEscalationEntry
from services import claim_service

router = APIRouter(
    prefix="/claims",
    tags=["Claims Management"]
)

@router.post("/upload_claim")
def upload_claim(data: ClaimUpload):
    filename = claim_service.save_claim_upload(data.dict())
    return {"message": f"Claim uploaded successfully.", "file": filename}

@router.post("/adjuster_response")
def upload_adjuster_response(data: AdjusterResponse):
    filename = claim_service.save_adjuster_response(data.dict())
    return {"message": f"Adjuster response saved successfully.", "file": filename}

@router.post("/call_escalation")
def upload_call_escalation(data: CallEscalationEntry):
    filename = claim_service.save_call_escalation(data.dict())
    return {"message": f"Call escalation saved successfully.", "file": filename}
