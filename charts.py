import pandas as pd
import plotly.express as px


def payment_method_pie(df: pd.DataFrame):
    payment_counts = df["paymentMethod"].value_counts().reset_index()
    payment_counts.columns = ["Payment Method", "Count"]

    fig = px.pie(
        payment_counts,
        values="Count",
        names="Payment Method",
        title="Payment Methods",
        color_discrete_sequence=["#2196F3", "#FFC107", "#4CAF50"]
    )
    return fig


def top_products_bar(df: pd.DataFrame):
    top = df.groupby("product_name")["product_price"].sum().nlargest(3).reset_index()
    top.columns = ["Product", "Total"]

    fig = px.bar(
        top,
        x="Product",
        y="Total",
        title="Top 3 Products",
        text_auto=True
    )
    return fig


def cashbox_sum_bar(df: pd.DataFrame):
    df["cashboxId"] = df["cashboxId"].astype(str)

    df_unique = df.drop_duplicates(subset="entry_id")
    by_cashbox = df_unique.groupby("cashboxId")["totalAmount"].sum().reset_index()
    by_cashbox.columns = ["Cashbox ID", "Total Amount"]

    fig = px.bar(
        by_cashbox,
        x="Cashbox ID",
        y="Total Amount",
        title="Sales by Cashbox",
        text_auto=True,
        color_discrete_sequence=["#3D8BFD"]
    )

    fig.update_layout(xaxis_type="category")
    return fig


def sales_by_day_bar(df: pd.DataFrame):
    df["created_at"] = pd.to_datetime(df["created_at"])

    sales_by_day = df.groupby(df["created_at"].dt.date.astype(str))["totalAmount"].sum().reset_index()
    sales_by_day.columns = ["Date", "Total Amount"]

    fig = px.bar(
        sales_by_day,
        x="Date",
        y="Total Amount",
        title="Sales by Day",
        color_discrete_sequence=["#FFC107"]
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales",
        xaxis_type="category"
    )
    return fig
