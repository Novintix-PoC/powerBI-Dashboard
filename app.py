import streamlit as st

# Set page config
st.set_page_config(layout="wide", page_title="Power BI Dashboard")

# Embed Power BI report using iframe
powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiMzVmNjQ4ZTItZmNkZC00NzRkLWI1OWQtYjllOGFhZDExYmQ5IiwidCI6IjBjY2Y1MDQxLWE0YjAtNDNiNy1iN2FhLTViMDhlZGEzYjJiMSIsImMiOjF9"  # Replace with your Power BI embed URL

st.markdown(
    f"""
    <style>
        .report-container {{
            position: absolute;
            top: 0;
            left: 0;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
    </style>
    <div class="report-container">
        <iframe src="{powerbi_url}" allowfullscreen="true"></iframe>
    </div>
    """,
    unsafe_allow_html=True
)
