import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales & Revenue Dashboard", layout="wide")

st.title("📊 Sales & Revenue Analysis Dashboard")

# Upload Excel or CSV
uploaded_file = st.file_uploader("Upload Excel or CSV File", type=["csv", "xlsx"])

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset")
    st.dataframe(df)

    # Sidebar Filters
    st.sidebar.header("Filters")

    if "Category" in df.columns:
        category = st.sidebar.multiselect(
            "Category",
            df["Category"].unique(),
            default=df["Category"].unique()
        )
        df = df[df["Category"].isin(category)]

    # KPIs
    total_sales = df["Sales"].sum()
    total_revenue = df["Revenue"].sum()

    col1, col2 = st.columns(2)

    col1.metric("Total Sales", f"{total_sales:,.0f}")
    col2.metric("Total Revenue", f"₹{total_revenue:,.2f}")

    # Bar Chart
    if "Product" in df.columns:
        fig = px.bar(
            df,
            x="Product",
            y="Revenue",
            color="Product",
            title="Revenue by Product"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Line Chart
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        trend = df.groupby("Date")["Revenue"].sum().reset_index()

        fig2 = px.line(
            trend,
            x="Date",
            y="Revenue",
            title="Revenue Trend"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Pie Chart
    if "Category" in df.columns:
        fig3 = px.pie(
            df,
            names="Category",
            values="Revenue",
            title="Revenue by Category"
        )
        st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Upload a CSV or Excel file to view the dashboard.")