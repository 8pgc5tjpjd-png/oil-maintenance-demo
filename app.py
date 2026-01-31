import os
from datetime import datetime

import pandas as pd
import streamlit as st

# --- Page setup ---
st.set_page_config(page_title="Operations Decision Layer", layout="wide")

# --- Robust paths (works on Render + locally) ---
BASE_DIR = os.path.dirname(os.path.abspath(_file_))

def load_csv(filename: str) -> pd.DataFrame:
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        st.error(f"Missing file: {filename}")
        st.write("Expected at:", path)
        st.stop()
    return pd.read_csv(path)

# --- Load data ---
assets = load_csv("assets.csv")
inventory = load_csv("inventory.csv")
events = load_csv("events.csv")

# --- UI ---
st.title("Operations Decision Layer — Maintenance & Spare Parts")
st.caption("Read-only decision + audit layer above ERP/CMMS (demo data)")

left, right = st.columns([1.1, 1])

with left:
    st.subheader("Assets at risk")
    st.dataframe(assets, use_container_width=True)

    st.subheader("Active events")
    if "timestamp" in events.columns:
        events_view = events.sort_values(by="timestamp", ascending=False)
    else:
        events_view = events
    st.dataframe(events_view, use_container_width=True)

with right:
    st.subheader("Decision panel")

    asset_id = st.selectbox("Select asset", assets["asset_id"].astype(str).tolist())
    asset = assets[assets["asset_id"].astype(str) == str(asset_id)].iloc[0]

    downtime = asset.get("downtime_cost_usd", 0)
    try:
        downtime_val = int(float(downtime)) if str(downtime) not in ["nan", "None", ""] else 0
    except Exception:
        downtime_val = 0

    st.metric("Downtime cost / day", f"${downtime_val:,}")

    st.subheader("System recommendation")
    st.success("Transfer VALVE-X9 from Site-C")

    st.write("*Why:*")
    st.write("- Stock on-site is 0; lead time from supplier is 6 days")
    st.write("- Site-C has 1 unit available with ~1 day transfer time")
    st.write("- Prevents ~2.5 days of downtime")
    st.write("- Estimated net savings: *$610,000*")

    st.subheader("Decision log")
    if st.button("Approve decision"):
        st.write(f"Approved at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.info("Next step (pilot): write this approval to a log table / ticket in CMMS.")
