import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Operations Decision Layer", layout="wide")

assets = pd.read_csv("assets.csv")
inventory = pd.read_csv("inventory.csv")
events = pd.read_csv("events.csv")

st.title("Operations Decision Layer — Maintenance & Spare Parts")
st.caption("Read-only decision + audit layer above ERP/CMMS (demo data)")

left, right = st.columns([1.1, 1])

with left:
    st.subheader("Assets at risk")
    st.dataframe(assets, use_container_width=True)

    st.subheader("Active events")
    st.dataframe(events.sort_values(by="timestamp", ascending=False), use_container_width=True)

with right:
    asset_id = st.selectbox("Select asset", assets["asset_id"])
    asset = assets[assets["asset_id"] == asset_id].iloc[0]

    st.metric("Downtime cost / day", f"${int(asset['downtime_cost_usd']):,}")

    st.subheader("System recommendation")
    st.success("Transfer VALVE-X9 from Site-C")

    st.write("*Why:*")
    st.write("- Prevents ~2.5 days of downtime")
    st.write("- Estimated net savings: *$610,000*")

    st.subheader("Decision log")
    if st.button("Approve decision"):
        st.write(f"Approved at {datetime.now().strftime('%H:%M:%S')}")
