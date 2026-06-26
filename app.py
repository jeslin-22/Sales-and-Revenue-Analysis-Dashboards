import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)


st.title(" Sales & Revenue Analysis Dashboard")


df = pd.read_csv("sales_data.csv")


df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)


filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df.shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹{total_sales:,}")
col2.metric("Total Profit", f"₹{total_profit:,}")
col3.metric("Total Orders", total_orders)

st.markdown("---")


st.subheader("Revenue Trend")

sales_trend = filtered_df.groupby("Date")["Sales"].sum().reset_index()

fig1 = px.line(
    sales_trend,
    x="Date",
    y="Sales",
    markers=True,
    title="Sales Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader(" Top Performing Products")

top_products = (
    filtered_df.groupby("Product")["Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Sales", ascending=False)
)

fig2 = px.bar(
    top_products,
    x="Product",
    y="Sales",
    color="Product",
    title="Top Products by Sales"
)

st.plotly_chart(fig2, use_container_width=True)


st.subheader(" Category-wise Sales")

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig3 = px.pie(
    category_sales,
    names="Category",
    values="Sales",
    title="Sales Distribution by Category"
)

st.plotly_chart(fig3, use_container_width=True)


st.subheader("Sales Data")

st.dataframe(filtered_df)