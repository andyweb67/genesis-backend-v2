# app/services/log_service.py

import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "casefile_generation.log")

def log_casefile_generation(claim_id: int, jurisdiction: str, adjuster_behavior: str, forced: bool):
    """
    Logs every casefile generation request.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    forced_text = "FORCED" if forced else "NORMAL"

    log_entry = (
        f"[{timestamp}] Casefile generated for Claim ID {claim_id} | "
        f"Jurisdiction: {jurisdiction} | Adjuster Behavior: {adjuster_behavior} | Mode: {forced_text}\n"
    )

    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)
