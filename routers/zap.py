# /routers/zap.py

from fastapi import APIRouter, Depends
from models.request_models import ZapRequest
from services.ai_handler import smart_ai_call
from services.zap_templates import get_zap_template
from dependencies.security import verify_api_key

router = APIRouter(
    prefix="/zap",
    tags=["ZAP"]
)

@router.post("/response", dependencies=[Depends(verify_api_key)])
def generate_zap_response(request: ZapRequest):
    """
    Generates a ZAP rebuttal based on the adjuster's response and jurisdiction.
    Uses a base ZAP instruction template + the specific adjuster's suppression text.
    """
    issue_type = "delayed_treatment"  # hardcoded for now; can be dynamic later

    zap_instruction = get_zap_template(issue_type, request.jurisdiction)

    prompt = (
        f"{zap_instruction}\n\n"
        f"Adjuster's response to rebut: '{request.adjuster_response}'.\n"
        f"Formulate a strategic plaintiff rebuttal emphasizing good faith standards."
    )

    ai_response = smart_ai_call(prompt, use_model="gpt")  # using GPT for now
    return {"zap_rebuttal": ai_response}
