import streamlit as st
import pandas as pd

# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(page_title="Oil Maintenance Decision System", layout="wide")

st.title("🛢️ Oil Maintenance & Spare Parts Decision System")
st.caption("Decision-layer demo (lightweight SAP-style workflow, but simpler)")

st.markdown(
    """
This demo is *self-contained* (no CSV files, no database) so it runs reliably on Render.
It shows how maintenance + inventory can produce *actionable recommendations* instantly.
"""
)

# -------------------------
# DEMO DATA (NO FILES)
# -------------------------
assets = pd.DataFrame([
    {"asset_id": "PUMP-001", "type": "Pump", "site": "Field A", "health": "Critical", "downtime_risk": "High"},
    {"asset_id": "VALVE-014", "type": "Valve", "site": "Refinery", "health": "Warning", "downtime_risk": "Medium"},
    {"asset_id": "COMP-221", "type": "Compressor", "site": "Pipeline", "health": "Healthy", "downtime_risk": "Low"},
])

events = pd.DataFrame([
    {"event_id": "E-1001", "asset_id": "PUMP-001", "event": "Pressure spike", "date": "2026-01-28", "severity": "High"},
    {"event_id": "E-1002", "asset_id": "VALVE-014", "event": "Leak detected", "date": "2026-01-30", "severity": "Medium"},
    {"event_id": "E-1003", "asset_id": "PUMP-001", "event": "Vibration anomaly", "date": "2026-01-31", "severity": "High"},
])

inventory = pd.DataFrame([
    {"part": "Pump Seal", "stock": 2, "min_required": 5, "lead_time_days": 14, "unit_cost_usd": 180},
    {"part": "Valve Spring", "stock": 18, "min_required": 10, "lead_time_days": 7, "unit_cost_usd": 25},
    {"part": "Compressor Filter", "stock": 0, "min_required": 3, "lead_time_days": 21, "unit_cost_usd": 90},
])

# -------------------------
# SIMPLE DECISION LOGIC
# -------------------------
def stock_risk(row):
    if row["stock"] <= 0:
        return "🔴 Stockout"
    if row["stock"] < row["min_required"]:
        return "🟠 Low"
    return "🟢 OK"

inventory["risk"] = inventory.apply(stock_risk, axis=1)

# Example: connect PUMP-001 issues to Pump Seal requirement (demo mapping)
recommendations = []

# Maintenance recommendation
critical_assets = assets[assets["health"].isin(["Critical"])]
for _, a in critical_assets.iterrows():
    recommendations.append({
        "priority": "P1",
        "action": f"Schedule immediate maintenance for {a['asset_id']} ({a['type']})",
        "reason": f"Asset health = {a['health']}, downtime risk = {a['downtime_risk']}",
    })

# Inventory recommendation
low_parts = inventory[inventory["risk"].isin(["🔴 Stockout", "🟠 Low"])]
for _, p in low_parts.iterrows():
    recommendations.append({
        "priority": "P1" if p["risk"] == "🔴 Stockout" else "P2",
        "action": f"Reorder part: {p['part']} (target ≥ {p['min_required']})",
        "reason": f"Stock = {p['stock']}, lead time = {p['lead_time_days']} days",
    })

recs_df = pd.DataFrame(recommendations)

# -------------------------
# UI TABS
# -------------------------
tab1, tab2, tab3 = st.tabs(["📊 Assets", "🛠️ Events", "📦 Inventory & Risk"])

with tab1:
    st.subheader("Asset Health Overview")
    st.dataframe(assets, use_container_width=True)

with tab2:
    st.subheader("Recent Maintenance / Sensor Events")
    st.dataframe(events, use_container_width=True)

with tab3:
    st.subheader("Spare Parts Inventory")
    st.dataframe(inventory, use_container_width=True)

st.markdown("---")
st.subheader("🤖 Recommendations (Decision Layer Output)")

if recs_df.empty:
    st.success("No critical actions right now.")
else:
    st.dataframe(recs_df, use_container_width=True)
    st.info("This is the key pitch: the system outputs *actions*, not spreadsheets.")

st.caption("Demo only — no real operational data.")
