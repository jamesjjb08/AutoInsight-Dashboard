import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Ask dashboard title
dashboard_title = st.text_input("Enter Dashboard Title")

if dashboard_title:
    st.title(dashboard_title)

# Upload dataset
file = st.file_uploader("Upload Dataset", type=["csv","xlsx"])

if file is not None:

    # Load dataset
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # KPI Section
    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # Detect column types
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    datetime_cols = df.select_dtypes(include=['datetime64']).columns

    st.subheader("Automatic Data Analysis")

    # Numeric Columns
    if len(numeric_cols) > 0:

        st.markdown("### Numeric Data Charts")

        for col in numeric_cols:

            fig = px.histogram(df, x=col, title=f"Distribution of {col}")
            st.plotly_chart(fig, use_container_width=True)

    # Categorical Columns
    if len(categorical_cols) > 0:

        st.markdown("### Categorical Data Charts")

        for col in categorical_cols:

            value_counts = df[col].value_counts()

            fig = px.bar(value_counts,
                         x=value_counts.index,
                         y=value_counts.values,
                         title=f"Category Count: {col}")

            st.plotly_chart(fig, use_container_width=True)

    # Date Columns
    if len(datetime_cols) > 0:

        st.markdown("### Time Trend Charts")

        for date_col in datetime_cols:
            for num_col in numeric_cols:

                fig = px.line(df,
                              x=date_col,
                              y=num_col,
                              title=f"{num_col} over {date_col}")

                st.plotly_chart(fig, use_container_width=True)

    # Correlation Heatmap
    if len(numeric_cols) > 1:

        st.subheader("Correlation Analysis")

        corr = df[numeric_cols].corr()

        fig = px.imshow(corr,
                        text_auto=True,
                        title="Correlation Heatmap")

        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload a dataset to generate the dashboard")
