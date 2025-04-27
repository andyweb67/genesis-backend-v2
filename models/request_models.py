from pydantic import BaseModel

class AdjusterResponseRequest(BaseModel):
    claim_id: str
    damages_summary: str

class ZapRequest(BaseModel):
    adjuster_response: str
    jurisdiction: str

class ProphetTriggerRequest(BaseModel):
    adjuster_behavior: str
    jurisdiction: str
class SingleClaimAudit(BaseModel):
    claim_id: str
    damages_summary: str

class BatchAuditRequest(BaseModel):
    claims: list[SingleClaimAudit]

   
