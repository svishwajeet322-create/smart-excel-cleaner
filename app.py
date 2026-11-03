
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Smart Excel Cleaner",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart Excel Data Cleaner")
st.write("Upload your Excel file and clean your data.")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:
        df = pd.read_excel(uploaded_file)

        st.success("Excel file uploaded successfully!")

        st.subheader("Original Data")
        st.dataframe(df)

        st.write("Total Rows:", len(df))
        st.write("Total Columns:", len(df.columns))

        st.subheader("Data Cleaning Options")

        remove_duplicates = st.checkbox(
            "Remove Duplicate Rows"
        )

        remove_empty = st.checkbox(
            "Remove Completely Empty Rows"
        )

        if remove_duplicates:
            df = df.drop_duplicates()

        if remove_empty:
            df = df.dropna(how="all")

        st.subheader("Sorting")

        column = st.selectbox(
            "Select Column",
            ["None"] + list(df.columns)
        )

        if column != "None":
            ascending = st.checkbox(
                "Ascending Order",
                value=True
            )

            df = df.sort_values(
                by=column,
                ascending=ascending
            )

        st.subheader("Cleaned Data")
        st.dataframe(df)

        output = BytesIO()

        df.to_excel(
            output,
            index=False,
            engine="openpyxl"
        )

        st.download_button(
            label="Download Clean Excel",
            data=output.getvalue(),
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success("Your cleaned Excel file is ready!")

    except Exception as e:
        st.error(f"Error: {e}")
