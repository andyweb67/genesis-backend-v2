from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/gds",
    tags=["Genesis Demand Summary"]
)

# Pydantic Models

class MedicalSpecial(BaseModel):
    provider: str
    amount_billed: float
    amount_paid: float = 0.0

class GenesisGDS(BaseModel):
    claimant_name: str
    date_of_loss: str
    liability_admission: str = None
    medical_specials: List[MedicalSpecial] = []
    diagnosis_codes: List[str] = []
    wpi_rating: str = None
    pain_and_suffering_narrative: str = None
    wage_loss: str = None
    future_medicals: str = None
    collateral_source_issues: str = None

@router.post("/build", response_model=GenesisGDS)
def build_gds(gds_input: GenesisGDS):
    """
    Receives extracted claim fields and returns a structured Genesis Demand Summary (GDS) object.
    """
    return gds_input
