from fastapi import APIRouter, HTTPException
from app.schemas.adjuster import AdjusterUploadModel
from app.services.mock_adjuster_responses import get_mock_adjuster_response
from app.services.audit_table import build_genesis_audit_table
from app.services.zap_rebuttals import build_zap_rebuttals
from app.services.ps_comparison import build_ps_comparison  # ✅ NEW
from app.services.report_writer import generate_rrt_markdown_report

import json
import os

router = APIRouter(prefix="/adjuster", tags=["Adjuster"])

MOCK_MODE = True

@router.post("/upload-response", summary="Upload Adjuster's Response or Inject Mock")
async def upload_adjuster_response(payload: AdjusterUploadModel):
    try:
        # ✅ 1. Get adjuster input (mock or real)
        if MOCK_MODE:
            adjuster_data = get_mock_adjuster_response(payload.claim_number)
        else:
            adjuster_data = payload.dict()

        # ✅ 2. Load matching Genesis Demand Summary
        gds_path = f"casefiles/{payload.claim_number}_gds.json"
        if not os.path.exists(gds_path):
            raise HTTPException(status_code=404, detail="Genesis Demand Summary (GDS) not found for this claim.")
        with open(gds_path, "r") as f:
            gds_data = json.load(f)

        # ✅ 3. Build Genesis components
        audit_table = build_genesis_audit_table(gds_data, adjuster_data)
        zap_rebuttals = build_zap_rebuttals(adjuster_data)
        ps_comparison = build_ps_comparison(gds_data, adjuster_data)  # ✅ NEW
        generate_rrt_markdown_report(payload.claim_number, zap_rebuttals, audit_table, ps_comparison)

        # ✅ 4. Return all together
        return {
            "status": "success",
            "adjuster_response": adjuster_data,
            "zap_rebuttals": zap_rebuttals,
            "audit_table": audit_table,
            "ps_comparison": ps_comparison  # ✅ NEW
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
