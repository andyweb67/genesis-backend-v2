# app/models/claim_models.py

from pydantic import BaseModel
from typing import Optional

class ClaimCreate(BaseModel):
    claimant_name: str
    date_of_loss: str
    description: Optional[str] = None
    amount_claimed: float
    liability_percent: Optional[int] = 0  # New: defaults to 0% if not provided
    medical_proof_attached: Optional[bool] = False  # New: default False
    wage_proof_attached: Optional[bool] = False  # New: default False
