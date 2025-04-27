from fastapi import APIRouter, Depends
from models.request_models import ProphetTriggerRequest
from services.ai_handler import smart_ai_call
from services.prophet_templates import get_prophet_template
from dependencies.security import verify_api_key

router = APIRouter(
    prefix="/prophet",
    tags=["Prophet"]
)

@router.post("/response", dependencies=[Depends(verify_api_key)])
def generate_prophet_response(request: ProphetTriggerRequest):
    """
    Generates a litigation risk escalation notice based on adjuster's refusal behavior.
    """
    issue_type = "pns_withheld"  # hardcoded for now (later can be dynamic)

    prophet_instruction = get_prophet_template(issue_type, request.jurisdiction)

    prompt = (
        f"{prophet_instruction}\n\n"
        f"Adjuster's behavior: '{request.adjuster_behavior}'.\n"
        f"Draft a litigation risk escalation notice emphasizing jury hostility to suppression."
    )

    ai_response = smart_ai_call(prompt, use_model="gpt")
    
    return {"prophet_notice": ai_response}
