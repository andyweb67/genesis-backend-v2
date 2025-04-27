# --- Section 4: Adjuster Response ---

import streamlit as st

def run():
    st.title("Section 4: Adjuster Response")
    st.markdown("---")

    if "adjuster_info" not in st.session_state:
        st.error("❌ No adjuster setup found. Please complete Section 3 first.")
        return

    adjuster_info = st.session_state["adjuster_info"]

    st.subheader(f"👤 Adjuster: {adjuster_info.get('adjuster_name', 'Unknown')}")

    adjuster_response = {}

    with st.form("adjuster_response_form"):
        st.markdown("### 🧾 Adjuster Response Form")

        # 1. Liability Confirmation
        adjuster_response["liability_acknowledged"] = st.radio(
            "Do you acknowledge liability as alleged?",
            ["Yes", "No"]
        )

        # 2. IME Ordered?
        adjuster_response["ime_status"] = st.selectbox(
            "Has an Independent Medical Exam (IME) been conducted?",
            ["No", "Yes", "Scheduled"]
        )

        # 3. Software Usage
        adjuster_response["claim_software"] = st.selectbox(
            "Which claims-handling software was used?",
            ["Claim IQ", "Colossus", "Manual", "Undisclosed"]
        )

        # 4. Medical Specials
        adjuster_response["medical_specials_total"] = st.text_input(
            "Accepted Medical Specials Total (USD)", placeholder="e.g., 14,500"
        )
        adjuster_response["medical_specials_justification"] = st.text_area(
            "Justification for any reduction in Medical Specials:"
        )

        # 5. Pain & Suffering
        adjuster_response["pain_and_suffering"] = st.text_input(
            "Allocated Pain & Suffering Amount (USD)", placeholder="e.g., 20,000"
        )
        adjuster_response["refuses_ps_breakdown"] = st.radio(
            "Do you refuse to disclose the basis for Pain & Suffering amount?",
            ["No", "Yes"]
        )

        # 6. Future Medicals (Optional)
        adjuster_response["future_medicals"] = st.text_input(
            "Accepted Future Medicals (USD)", placeholder="Optional"
        )

        # 7. Lost Wages (Optional)
        adjuster_response["lost_wages"] = st.text_input(
            "Accepted Lost Wages (USD)", placeholder="Optional"
        )
        adjuster_response["lost_wages_justification"] = st.text_area(
            "Justification for any reduction to Lost Wages:", placeholder="Optional"
        )

        # 8. Mileage (Optional)
        adjuster_response["mileage"] = st.text_input(
            "Accepted Transportation Mileage (USD)", placeholder="Optional"
        )
        adjuster_response["mileage_justification"] = st.text_area(
            "Justification for any reduction to Mileage:", placeholder="Optional"
        )

        submitted = st.form_submit_button("✅ Submit Adjuster Response")

    if submitted:
        st.session_state["adjuster_responses"] = adjuster_response
        st.success("✅ Adjuster responses saved successfully. Ready for RRT generation.")

