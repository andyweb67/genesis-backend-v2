# report_dashboard_ui.py (Streamlit)

import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Genesis Casefile Dashboard", layout="wide")
st.title("📁 Genesis Report Dashboard")

st.markdown("---")

response = requests.get(f"{API_URL}/report/summary")

if response.status_code != 200:
    st.error("Failed to load summary data.")
else:
    data = response.json()

    for entry in data:
        col1, col2, col3, col4, col5, col6 = st.columns([1.5, 1.5, 1, 1, 1, 2])

        with col1:
            st.markdown(f"**Claimant:** {entry['claimant_name']}")
            st.markdown(f"Claim #: `{entry['claim_number']}`")

        with col2:
            st.markdown(f"📄 RRT.md: {'✅' if entry['rrt_md'] else '❌'}")
            st.markdown(f"📄 RRT.pdf: {'✅' if entry['rrt_pdf'] else '❌'}")

        with col3:
            st.markdown(f"✉️ Final Demand: {'✅' if entry['final_demand'] else '❌'}")

        with col4:
            st.markdown(f"🧠 Prophet: {'✅' if entry['prophet_summary'] else '❌'}")

        with col5:
            st.markdown(f"📦 ZIP Ready: {'✅' if entry['zip_ready'] else '❌'}")

        with col6:
            if entry['zip_ready']:
                st.download_button(
                    label="⬇️ Download ZIP",
                    data=requests.get(f"{API_URL}/report/zip/{entry['claim_id']}").content,
                    file_name=f"casefile_{entry['claim_number']}.zip",
                    mime="application/zip"
                )
            else:
                if st.button(f"🔄 Regenerate Reports", key=f"regen_{entry['claim_id']}"):
                    regen = requests.get(f"{API_URL}/report/zip/{entry['claim_id']}")
                    if regen.status_code == 200:
                        st.success(f"Files regenerated for claim {entry['claim_number']}")
                    else:
                        st.error(f"Failed to regenerate files for claim {entry['claim_number']}")

        st.markdown("---")
