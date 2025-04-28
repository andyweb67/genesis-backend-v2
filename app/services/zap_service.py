# app/services/zap_service.py

from app.services.zap_templates import get_zap_template

# Mapping audit findings to issue types
def map_finding_to_issue(finding: str) -> str:
    if "delayed treatment" in finding.lower():
        return "delayed_treatment"
    elif "collateral source" in finding.lower():
        return "collateral_source"
    elif "comparative negligence" in finding.lower():
        return "comparative_negligence"
    elif "failure to mitigate" in finding.lower():
        return "failure_to_mitigate"
    else:
        return "general"

def generate_full_zap_response(audit_findings: list, jurisdiction: str) -> list:
    zap_responses = []

    for finding in audit_findings:
        issue_type = map_finding_to_issue(finding)
        zap_text = get_zap_template(issue_type, jurisdiction)
        zap_responses.append({
            "finding": finding,
            "zap_rebuttal": zap_text
        })

    return zap_responses
