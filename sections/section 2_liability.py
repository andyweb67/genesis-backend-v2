# --- Section 2: Liability Determination ---

import streamlit as st

def run():
    st.title("Section 2: Liability & Causation")
    st.markdown("---")

    if "extracted_text" not in st.session_state:
        st.error("❌ No extracted text found. Please complete the upload in Section 1.")
        return

    extracted_text = st.session_state["extracted_text"]

    # --- Generate basic draft from OCR Text ---
    def draft_liability_summary(text):
        lower_text = text.lower()
        if "rear-end" in lower_text:
            return "Liability is accepted against the defendant for causing a rear-end collision."
        elif "intersection" in lower_text:
            return "Liability determination involves right-of-way evaluation at intersection."
        elif "left turn" in lower_text:
            return "Potential liability on the turning party for improper left-hand turn."
        else:
            return "Liability determination requires further review of the provided facts."

    default_liability = draft_liability_summary(extracted_text)

    st.subheader("🧠 Auto-Generated Liability Summary (Editable)")
    liability_text = st.text_area(
        "Review and edit the liability determination below:",
        value=default_liability,
        height=250
    )

    if st.button("✅ Confirm Liability Summary"):
        st.session_state["liability_determination"] = liability_text
        st.success("Liability determination saved successfully.")

    st.markdown("---")

    # --- Optional: Future Expansion for Uploaded Police Report Images ---
    st.subheader("🚔 Optional Police Report Upload")
    police_report = st.file_uploader("Upload Police Report Image (Optional)", type=["png", "jpg", "jpeg"])

    if police_report:
        st.image(police_report, caption="Uploaded Police Report Snapshot", width=500)
