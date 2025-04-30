from pydantic import BaseModel
from typing import Optional, List

class ProviderRow(BaseModel):
    name: str
    adjuster: str

class AdjusterTable(BaseModel):
    medical_specials_total: str
    providers: List[ProviderRow]
    pain_and_suffering: str
    future_medicals: str
    lost_wages: str
    mileage: str
    subtotal: str
    deductions: str
    total: str

class AdjusterUploadModel(BaseModel):
    adjuster_name: Optional[str] = None
    adjuster_email: Optional[str] = None
    claim_number: str  # ✅ Required to trigger mock profile
    fiduciary_ack: Optional[str] = None
    liability_acknowledged: Optional[str] = None
    ime_status: Optional[str] = None
    claim_software: Optional[str] = None
    medical_specials_justification: Optional[str] = None
    refuses_ps_breakdown: Optional[str] = None
    no_ime_acknowledgment: Optional[str] = None
    med_basis_if_adjusted: Optional[str] = None
    mileage_justification: Optional[str] = None
    lost_wages_justification: Optional[str] = None
    profile_name: Optional[str] = None
    adjuster_table: Optional[AdjusterTable] = None  # ✅ Allow missing table in mock mode
