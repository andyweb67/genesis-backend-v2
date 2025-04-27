# /routers/admin.py

from fastapi import APIRouter, Depends
from dependencies.security import verify_api_key
from core.settings import genesis_settings  # ✅ Now imported properly

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/settings/get", dependencies=[Depends(verify_api_key)])
async def get_settings():
    """
    Retrieve the current Genesis system settings.
    """
    return genesis_settings

@router.post("/settings/update", dependencies=[Depends(verify_api_key)])
async def update_settings(model: str = None, temperature: float = None, default_jurisdiction: str = None):
    """
    Update Genesis system settings.
    Fields are optional — only provided values will be updated.
    """
    if model:
        genesis_settings["model"] = model
    if temperature:
        genesis_settings["temperature"] = temperature
    if default_jurisdiction:
        genesis_settings["default_jurisdiction"] = default_jurisdiction

    return {"message": "Genesis settings updated successfully.", "current_settings": genesis_settings}
