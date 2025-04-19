from data_loader import load_transactions
from charts import (
    payment_method_pie,
    top_products_bar,
    cashbox_sum_bar,
    sales_by_day_bar
)
from monthly_stats import show_monthly_statistics
from utils import plotly_chart_no_controls

import os
import sys
from pathlib import Path
import streamlit as st
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


st.set_page_config(
    page_title="Transaction Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"
)

# ──────────────────────────────────────────────────────
# 📎 Fonts and custom CSS
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

css_path = Path(__file__).resolve().parent / "styles" / "custom.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("⚠️ custom.css not found.")

# ──────────────────────────────────────────────────────
# 📌 Title
st.title("📈 Transaction Dashboard")

# ──────────────────────────────────────────────────────
# 🔑 Read query params
params = st.query_params
if "organization_id" in params:
    st.session_state.organization_id = params["organization_id"]
    st.session_state.page = params["page"]
    st.session_state.limit = params["limit"]


org_id = st.session_state.get("organization_id")
page = st.session_state.get("page")
limit = st.session_state.get("limit")

if not org_id:
    st.info("⏳ Waiting for organization ID...")
    st.stop()

# ──────────────────────────────────────────────────────
# 🔐 Load data
token = st.secrets.get("API_TOKEN")
df, error = load_transactions(org_id, page, limit, token)

if error:
    st.error(error)
    st.stop()

# ──────────────────────────────────────────────────────
# 📆 Date range filter
st.subheader("📅 Data for the selected period")
df["created_at"] = pd.to_datetime(df["created_at"]).dt.date

min_date = df["created_at"].min()
max_date = df["created_at"].max()
date_range = st.date_input("Select date range", (min_date, max_date))

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df["created_at"] >= start_date) & (df["created_at"] <= end_date)]
else:
    df = df[df["created_at"] == date_range]

if df.empty:
    st.warning("⚠️ No data available for the selected period.")
    st.stop()

# ──────────────────────────────────────────────────────
# 📊 Main charts
col1, col2 = st.columns(2)
with col1:
    plotly_chart_no_controls(payment_method_pie(df), use_container_width=True)
with col2:
    plotly_chart_no_controls(top_products_bar(df), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    plotly_chart_no_controls(cashbox_sum_bar(df), use_container_width=True)
with col4:
    plotly_chart_no_controls(sales_by_day_bar(df), use_container_width=True)

# ──────────────────────────────────────────────────────
# 📆 Monthly breakdown
show_monthly_statistics(df)
