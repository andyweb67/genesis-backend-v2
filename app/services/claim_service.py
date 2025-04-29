# app/services/claim_service.py
"""
GENESIS DNA INSTRUCTION

Purpose:
- Guide AI or manual extraction of structured claim data from uploaded demand packages.

Strategic Objective:
- Ensure full transparency of damages claimed.
- Capture medical specials, general damages, pain and suffering narratives, and supporting evidence.

Extraction Requirements:
- Claimant Name
- Date of Loss
- Liability Admission (if any)
- Medical Specials (Provider, Amount Billed, Amount Paid)
- Diagnosis Codes (if listed)
- Permanent Impairments (e.g., WPI ratings)
- Pain and Suffering Narratives
- Wage Loss (documentation of employment disruption)
- Collateral Source Issues (health insurance offsets)

Response Expectations:
- Populate Genesis claim object accurately.
- Flag missing fields for manual intervention if AI fails.

Future AI Enhancement Plan:
- Automate extraction via OCR and LLM parsing of demand packages.

Author: Andrew Weber
Date Created: 2025-04-28
"""

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
