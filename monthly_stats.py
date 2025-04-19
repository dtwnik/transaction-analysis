import datetime
import calendar
import pandas as pd
import plotly.express as px
import streamlit as st


def show_monthly_statistics(df):
    st.header("📅 Data for Selected Year and Month")

    options_y = df["created_at"].dt.year.sort_values().unique()
    options_m = list(range(1, 13))
    month_names = [calendar.month_name[m] for m in options_m]

    year = st.pills("Year", options_y, selection_mode="single")
    month_name = st.pills("Month", month_names, selection_mode="single")
    month = list(calendar.month_name).index(month_name) if month_name else None

    # placeholders: chart on top, table below
    chart_placeholder = st.empty()
    dataframe_placeholder = st.empty()

    columns_to_display = [
        "created_at",
        "entry_id",
        "product_name",
        "product_price",
        "paymentMethod",
        "cashboxId",
        "organizationId"
    ]

    column_renames = {
        "created_at": "Date",
        "entry_id": "Transaction ID",
        "product_name": "Product",
        "product_price": "Price Tng",
        "paymentMethod": "Payment Method",
        "cashboxId": "Cashbox ID",
        "organizationId": "Organization ID"
    }

    if year is not None and month is not None:
        filtered = df[
            (df["created_at"].dt.year == year) &
            (df["created_at"].dt.month == month)
        ]

        num_days = calendar.monthrange(year, month)[1]
        all_dates = pd.date_range(
            start=datetime.date(year, month, 1),
            end=datetime.date(year, month, num_days)
        )

        grouped = filtered["created_at"].value_counts().sort_index()
        daily_counts = pd.Series(0, index=pd.date_range(start=datetime.date(year, month, 1), periods=num_days))
        daily_counts.update(grouped)

        fig = px.line(
            x=daily_counts.index,
            y=daily_counts.values,
            labels={"x": "Date", "y": "Transactions"},
            title="📊 Daily Transaction Count"
        )

        if "date_only_str" in filtered.columns:
            filtered = filtered.drop(columns=["date_only_str"])

        chart_placeholder.plotly_chart(fig, use_container_width=True)

        dataframe_placeholder.dataframe(
            filtered[columns_to_display].rename(columns=column_renames)
        )

    else:
        today = datetime.date.today()
        dummy_days = pd.date_range(
            start=today.replace(day=1),
            periods=calendar.monthrange(today.year, today.month)[1]
        )
        dummy_data = pd.Series(0, index=dummy_days)

        empty_fig = px.line(
            x=dummy_data.index,
            y=dummy_data.values,
            labels={"x": "Date", "y": "Transactions"},
            title="📊 Daily Transaction Count"
        )

        empty_df = pd.DataFrame(columns=columns_to_display)
        empty_df = empty_df.rename(columns=column_renames)

        chart_placeholder.plotly_chart(empty_fig, use_container_width=True)
        dataframe_placeholder.dataframe(empty_df)
