from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import json
import os

# ✅ Import Genesis Validation Engine
from app.services.gds_validation import build_gds_validation_table

router = APIRouter()

# Supporting Models
class Provider(BaseModel):
    name: str = Field(..., description="Provider's name")
    attorney: str = Field(..., description="Amount demanded by attorney")
    genesis: str = Field(..., description="Genesis audit recalculation")
    validation: Optional[str] = None
    page: Optional[str] = None

class GdsTable(BaseModel):
    medical_specials_total: Dict[str, Any]
    providers: List[Provider]
    pain_and_suffering: Dict[str, Any]
    future_medicals: Dict[str, Any]
    lost_wages: Dict[str, Any]
    mileage: Dict[str, Any]
    subtotal: Dict[str, Any]
    deductions: Dict[str, Any]
    total: Dict[str, Any]

class SupportingDocument(BaseModel):
    provider: str
    specialist: Optional[str]
    treatment_or_code: Optional[str]
    page: Optional[str]
    npi: Optional[str]
    board_certification: Optional[str]
    treatment_type: Optional[str]
    impairment_assessment: Optional[str]
    peer_reviewed_support: Optional[str]

class GenesisDemandUpload(BaseModel):
    claimant_name: str
    claim_number: str
    date_of_loss: str
    claim_type: str
    state: str
    pip_status: Optional[str] = "N/A"
    adjuster_name: str
    adjuster_email: str
    initial_offer: str
    attorney_name: str
    law_firm: str
    gds_table: GdsTable
    supporting_documents: Optional[List[SupportingDocument]] = []
    liability_determination: Optional[str] = None

@router.post("/upload-demand", summary="Upload Genesis Demand Summary JSON")
async def upload_genesis_demand(payload: GenesisDemandUpload):
    try:
        # Parse clean response
        parsed_response = {
            "Claim Details": {
                "Claimant Name": payload.claimant_name,
                "Claim Number": payload.claim_number,
                "Date of Loss": payload.date_of_loss,
                "Claim Type": payload.claim_type,
                "State": payload.state,
                "PIP Status": payload.pip_status,
                "Adjuster Name": payload.adjuster_name,
                "Adjuster Email": payload.adjuster_email,
                "Initial Offer": payload.initial_offer,
                "Attorney Name": payload.attorney_name,
                "Law Firm": payload.law_firm
            },
            "Genesis Demand Summary Table": payload.gds_table.dict(),
            "Supporting Documents": [doc.dict() for doc in payload.supporting_documents] if payload.supporting_documents else [],
            "Liability Determination Summary": payload.liability_determination
        }

        # ✅ Validate GDS Logic
        gds_validated_table = build_gds_validation_table(payload)

        # ✅ Save Parsed Genesis Demand + Audit Table
        os.makedirs("casefiles", exist_ok=True)
        safe_claim_number = payload.claim_number.replace(" ", "_").replace("/", "_")
        
        # (1) Save the full parsed Genesis Demand Summary
        with open(f"casefiles/{safe_claim_number}_gds.json", "w", encoding="utf-8") as f:
            json.dump(parsed_response, f, indent=4)

        # (2) Save the raw uploaded payload if needed (optional backup)
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        backup_filename = f"casefiles/{safe_claim_number}_{timestamp}.json"
        with open(backup_filename, "w", encoding="utf-8") as f:
            json.dump(payload.dict(), f, indent=4)

        # ✅ Return Both Parsed GDS + Validation Table
        return {
            "status": "success",
            "saved_as": f"{safe_claim_number}_gds.json",
            "parsed_genesis_demand": parsed_response,
            "gds_validated_table": gds_validated_table
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
