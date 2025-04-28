# app/services/claim_service.py

from typing import List
from app.models.claim_models import ClaimCreate

# Fake database (just a simple list for now)
claims_db: List[ClaimCreate] = []

# Function to add a claim
def add_claim(claim: ClaimCreate):
    claims_db.append(claim)

# Function to list all claims
def list_claims() -> List[ClaimCreate]:
    return claims_db
