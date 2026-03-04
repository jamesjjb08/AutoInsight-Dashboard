import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auto Dashboard", layout="wide")

# Dashboard title input
dashboard_title = st.text_input("Enter Dashboard Title")

if dashboard_title:
    st.title(dashboard_title)

# Upload dataset
uploaded_file = st.file_uploader("Upload Dataset (CSV or Excel)", type=["csv","xlsx"])

if uploaded_file:

    # Read dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # Dashboard Metrics
    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # Detect column types
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    st.subheader("Interactive Dashboard")

    # Numeric charts
    for col in numeric_cols:
        fig = px.histogram(df, x=col, title=f"Distribution of {col}")
        st.plotly_chart(fig, use_container_width=True)

    # Categorical charts
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        fig = px.bar(
            x=value_counts.index,
            y=value_counts.values,
            labels={"x": col, "y": "Count"},
            title=f"{col} Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap
    if len(numeric_cols) > 1:
        st.subheader("Correlation Heatmap")
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload a dataset to generate the live dashboard.")
