# /services/prophet_templates.py

def get_prophet_template(issue_type: str, jurisdiction: str) -> str:
    """
    Returns a base Prophet escalation instruction based on issue type and jurisdiction.
    """
    templates = {
        "pns_withheld": (
            "In {jurisdiction}, an insurer's refusal to disclose valuation reasoning for Pain and Suffering "
            "may constitute internal suppression and a breach of good faith duties under common and statutory law. "
            "Highlight the need for discovery into internal valuation software (e.g., Claim IQ, Colossus) and note "
            "jury sympathy trends against concealment tactics."
        ),
        "collateral_source_violation": (
            "If an adjuster applies unauthorized collateral source reductions, in {jurisdiction}, this violates the "
            "collateral source rule and constitutes potential bad faith exposure. Stress discovery rights and punitive damage exposure."
        )
    }

    template = templates.get(issue_type)
    if template:
        return template.format(jurisdiction=jurisdiction)
    else:
        return (
            f"In {jurisdiction}, internal suppression of claim valuations without clear justification constitutes potential bad faith. "
            "Request internal documentation and note jury hostility to concealment patterns."
        )
