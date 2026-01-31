import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Oil Maintenance Decision System",
    layout="wide"
)

st.title("🛢️ Oil Maintenance & Spare Parts Decision System")
st.caption("AI-style operational decision layer demo (SAP alternative)")

# -------------------------
# DEMO DATA (hardcoded)
# -------------------------

assets = pd.DataFrame([
    {"Asset ID": "PUMP-001", "Type": "Pump", "Location": "Field A", "Status": "Critical"},
    {"Asset ID": "VALVE-014", "Type": "Valve", "Location": "Refinery", "Status": "Warning"},
    {"Asset ID": "COMP-221", "Type": "Compressor", "Location": "Pipeline", "Status": "Healthy"},
])

inventory = pd.DataFrame([
    {"Part": "Pump Seal", "Stock": 2, "Min Required": 5, "Lead Time (days)": 14},
    {"Part": "Valve Spring", "Stock": 18, "Min Required": 10, "Lead Time (days)": 7},
    {"Part": "Compressor Filter", "Stock": 0, "Min Required": 3, "Lead Time (days)": 21},
])

events = pd.DataFrame([
    {"Asset ID": "PUMP-001", "Event": "Pressure spike", "Date": "2026-01-28"},
    {"Asset ID": "VALVE-014", "Event": "Leak detected", "Date": "2026-01-30"},
])

# -------------------------
# UI
# -------------------------

tab1, tab2, tab3 = st.tabs([
    "📊 Asset Health",
    "📦 Spare Parts Risk",
    "🤖 AI Recommendations"
])

with tab1:
    st.subheader("Asset Health Overview")
    st.dataframe(assets, use_container_width=True)

with tab2:
    st.subheader("Spare Parts Inventory Risk")

    def risk(row):
        if row["Stock"] == 0:
            return "🔴 Stockout"
        if row["Stock"] < row["Min Required"]:
            return "🟠 Low Stock"
        return "🟢 OK"

    inventory["Risk"] = inventory.apply(risk, axis=1)
    st.dataframe(inventory, use_container_width=True)

with tab3:
    st.subheader("AI-Style Operational Decisions")

    st.markdown("""
    *System Output:*
    - Immediate maintenance required for *PUMP-001*
    - Order *Pump Seals* immediately (14-day lead time)
    - Preventive action recommended for *VALVE-014*
    """)

    st.success("✔ This system replaces manual SAP workflows and planner dependency")

# -------------------------
# Footer
# -------------------------

st.markdown("---")
st.caption("Demo system — no real operational data")
