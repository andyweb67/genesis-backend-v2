# --- Section 1: Upload Demand Package & Generate Genesis Demand Summary (GDS) ---

import streamlit as st
import pandas as pd
import pytesseract
from pdf2image import convert_from_bytes
from io import BytesIO
from zipfile import ZipFile
from docx import Document
import requests
from datetime import datetime

# --- Helper Functions ---

def extract_text_from_pdf(file_bytes):
    images = convert_from_bytes(file_bytes)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def extract_text_from_docx(file_bytes):
    doc = Document(file_bytes)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_zip(file_bytes):
    text = ''
    with ZipFile(BytesIO(file_bytes)) as archive:
        for file_name in archive.namelist():
            if file_name.endswith('.pdf'):
                with archive.open(file_name) as pdf_file:
                    text += extract_text_from_pdf(pdf_file.read())
    return text

def parse_gds_from_text(extracted_text):
    # Placeholder parsing logic
    # TODO: Expand into full AI/NLP parsing later
    gds = {
        "Claimant Name": "Extracted Name Placeholder",
        "Damages": [
            {"Category": "Medical Specials", "Amount": 15000},
            {"Category": "Lost Wages", "Amount": 8000},
            {"Category": "Pain & Suffering", "Amount": 25000}
        ],
        "Total Demand": 48000
    }
    return gds

def send_to_backend(payload):
    try:
        response = requests.post("http://localhost:8000/upload_claim_data", json=payload)
        if response.status_code == 200:
            st.success("✅ Claim data successfully saved to backend!")
        else:
            st.error(f"⚠️ Backend save failed. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"🚨 Failed to connect to backend: {e}")

# --- Streamlit App ---

def run():
    st.title("Step 1–2: Upload & Genesis Demand Summary (GDS)")

    uploaded_file = st.file_uploader("📁 Upload a Demand Package (PDF, ZIP, DOCX)", type=["pdf", "zip", "docx"])

    if uploaded_file:
        file_type = uploaded_file.name.split('.')[-1].lower()

        with st.spinner('Extracting data from uploaded file...'):
            if file_type == 'pdf':
                extracted_text = extract_text_from_pdf(uploaded_file.read())
            elif file_type == 'docx':
                extracted_text = extract_text_from_docx(uploaded_file)
            elif file_type == 'zip':
                extracted_text = extract_text_from_zip(uploaded_file.read())
            else:
                st.error("Unsupported file type uploaded.")
                return

        gds = parse_gds_from_text(extracted_text)

        # Update session state
        st.session_state["gds"] = gds
        st.session_state["extracted_text"] = extracted_text
        st.session_state["gds_ready"] = True

        # Prepare payload for backend
        payload = {
            "claimant_name": gds.get("Claimant Name", "Unknown"),
            "ocr_text": extracted_text,
            "gds": gds,
            "upload_timestamp": datetime.utcnow().isoformat()
        }

        send_to_backend(payload)

        # --- Display Genesis Demand Summary (GDS) ---
        st.subheader("📋 Genesis Demand Summary (Preview)")
        st.json(gds)

    else:
        st.info("Please upload a demand package to begin.")

