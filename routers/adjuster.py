from fastapi import APIRouter, Depends
from models.request_models import AdjusterResponseRequest
from services.ai_handler import smart_ai_call
from dependencies.security import verify_api_key


router = APIRouter(
    prefix="/adjuster",
    tags=["Adjuster"]
)

@router.post("/response", dependencies=[Depends(verify_api_key)])
def generate_adjuster_response(request: AdjusterResponseRequest):
    ...
    prompt = f"Given this damages summary, generate a typical insurance adjuster response minimizing payout values: {request.damages_summary}"
    ai_response = smart_ai_call(prompt, use_model="gpt")  # Use GPT-4 for adjuster simulation
    return {"adjuster_response": ai_response}
