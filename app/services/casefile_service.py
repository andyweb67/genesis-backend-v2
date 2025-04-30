# app/services/casefile_service.py

import os
import zipfile
from datetime import datetime

CASEFILE_DIR = "casefiles"

def zip_casefile(claim_id: int) -> str:
    """
    Zips the full casefile folder for a given claim_id.
    Deletes any old ZIPs for that claim before creating new one.
    After zipping, deletes the temporary PDFs, leaving only the ZIP file.
    Returns the path to the new ZIP file.
    """
    # --- NEW: Ensure base casefiles/ directory exists
    if not os.path.exists(CASEFILE_DIR):
        os.makedirs(CASEFILE_DIR)

    claim_folder = os.path.join(CASEFILE_DIR, str(claim_id))
    
    today = datetime.now().strftime("%Y-%m-%d")
    zip_filename = f"casefile_{claim_id}_{today}.zip"
    zip_path = os.path.join(CASEFILE_DIR, zip_filename)

    if not os.path.exists(claim_folder):
        raise FileNotFoundError(f"No case file found for claim ID {claim_id}")

    # --- Delete any old ZIPs for this claim
    for file in os.listdir(CASEFILE_DIR):
        if file.startswith(f"casefile_{claim_id}_") and file.endswith(".zip"):
            os.remove(os.path.join(CASEFILE_DIR, file))

    # --- Create fresh ZIP
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(claim_folder):
            for file in files:
                if file.endswith(".zip"):
                    continue  # Don't zip existing zips
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, claim_folder)
                zipf.write(file_path, arcname=arcname)

    # --- Delete all PDFs inside the casefile folder
    for file in os.listdir(claim_folder):
        file_path = os.path.join(claim_folder, file)
        if file.endswith(".pdf"):
            os.remove(file_path)

    return zip_path

def package_casefile(claim_number: str, file_paths: list, output_dir: str = "casefiles") -> str:
    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, f"{claim_number}_casefile.zip")

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for path in file_paths:
            if os.path.exists(path):
                arcname = os.path.basename(path)
                zipf.write(path, arcname=arcname)

    return zip_path
