# services/zap_templates.py

def get_zap_template(issue_type: str, jurisdiction: str) -> str:
    """
    Returns a base ZAP rebuttal instruction based on issue type and jurisdiction.
    """
    templates = {
        "delayed_treatment": (
            "In {jurisdiction}, delayed treatment does not negate causation when reasonable explanations exist. "
            "Emphasize case law where treatment delays are justified by work, family obligations, or delayed onset of symptoms. "
            "Highlight insurer's duty to consider all reasonable explanations before denying or downgrading damages."
        ),
        "collateral_source": (
            "In {jurisdiction}, the collateral source rule prohibits insurers from reducing damages based on payments "
            "from third-party sources like health insurance. Rebut any attempt to offset damages based on outside payments, "
            "and cite applicable state law where appropriate."
        ),
        "comparative_negligence": (
            "Challenge the application of comparative negligence unless clearly supported by evidence. "
            "In {jurisdiction}, the burden is on the insurer to prove comparative negligence by a preponderance of evidence."
        ),
        "failure_to_mitigate": (
            "If alleging failure to mitigate, remind the insurer that {jurisdiction} requires clear evidence of unreasonable conduct "
            "causing additional damages. Lack of immediate treatment alone does not constitute failure to mitigate."
        )
    }
    
    template = templates.get(issue_type)
    if template:
        return template.format(jurisdiction=jurisdiction)
    else:
        return (
            f"In {jurisdiction}, general bad faith principles require insurers to fully and fairly evaluate claims. "
            "Challenge any vague or unsupported reductions in valuation."
        )
