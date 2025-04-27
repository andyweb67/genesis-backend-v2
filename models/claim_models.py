# --- models/claim_models.py ---

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GDSItem(BaseModel):
    Category: str
    Amount: float

class ClaimUpload(BaseModel):
    claimant_name: str
    ocr_text: str
    gds: List[GDSItem]
    upload_timestamp: datetime

class AdjusterResponse(BaseModel):
    adjuster_name: str
    adjuster_email: Optional[str]
    liability_acknowledged: str
    ime_status: str
    claim_software: str
    medical_specials_total: str
    medical_specials_justification: Optional[str]
    pain_and_suffering: str
    refuses_ps_breakdown: str
    future_medicals: Optional[str]
    lost_wages: Optional[str]
    lost_wages_justification: Optional[str]
    mileage: Optional[str]
    mileage_justification: Optional[str]
    timestamp: datetime

class CallEscalationEntry(BaseModel):
    adjuster_name: str
    contact_date: str
    contact_time: str
    outcome: str
    follow_up: Optional[str]
    timestamp: datetime
