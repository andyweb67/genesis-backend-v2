# --- services/claim_service.py ---

import os
import json
from datetime import datetime

# Define a base directory for saving files
SAVE_DIR = "saved_claims"

# Ensure the folder exists
os.makedirs(SAVE_DIR, exist_ok=True)

def save_claim_upload(data: dict):
    claimant_name = data.get("claimant_name", "unknown").replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{claimant_name}_claim_{timestamp}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return filename

def save_adjuster_response(data: dict):
    adjuster_name = data.get("adjuster_name", "unknown").replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{adjuster_name}_adjuster_response_{timestamp}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return filename

def save_call_escalation(data: dict):
    adjuster_name = data.get("adjuster_name", "unknown").replace(" ", "_")
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{adjuster_name}_call_escalation_{timestamp}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return filename
