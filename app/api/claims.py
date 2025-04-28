# app/api/claims.py

from fastapi import APIRouter
from app.models.claim_models import ClaimCreate
from app.services.claim_service import add_claim, list_claims  # <-- NEW

router = APIRouter(
    prefix="/claims",
    tags=["Claims"]
)

# GET /claims/
@router.get("/")
def get_claims():
    claims = list_claims()
    return {"claims": claims}

# POST /claims/
@router.post("/")
def create_claim(claim: ClaimCreate):
    add_claim(claim)
    return {
        "message": "Claim successfully submitted!",
        "claim_data": claim.dict()
    }
