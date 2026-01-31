import streamlit as st
import pandas as pd

st.set_page_config(page_title="Oil Maintenance Demo", layout="wide")

st.title("🛢️ Oil Maintenance & Spare Parts Decision Layer")

st.markdown(
    """
This is a *demo decision layer* showing how maintenance events,
asset health, and inventory can be connected — similar to a lightweight,
AI-ready alternative to SAP maintenance modules.
"""
)

# --- Load data (relative paths, Streamlit-safe) ---
assets = pd.read_csv("assets.csv")
events = pd.read_csv("events.csv")
inventory = pd.read_csv("inventory.csv")

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Assets")
    st.dataframe(assets, use_container_width=True)

with col2:
    st.subheader("🛠️ Maintenance Events")
    st.dataframe(events, use_container_width=True)

st.subheader("📦 Spare Parts Inventory")
st.dataframe(inventory, use_container_width=True)

# --- Simple insight example ---
st.subheader("⚠️ Simple Operational Insight")

low_stock = inventory[inventory["quantity"] < 5]

if not low_stock.empty:
    st.warning("Some spare parts are running low:")
    st.dataframe(low_stock)
else:
    st.success("All spare parts are sufficiently stocked.")
