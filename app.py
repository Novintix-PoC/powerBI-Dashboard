import streamlit as st
import requests
from msal import ConfidentialClientApplication

st.set_page_config(page_title="Executive Dashboard", layout="wide")

# --- Azure AD Auth Setup ---
def initialize_app():
    client_id = st.secrets["CLIENT_ID"]
    tenant_id = st.secrets["TENANT_ID"]
    client_secret = st.secrets["CLIENT_SECRET"]
    authority_url = f"https://login.microsoftonline.com/{tenant_id}"
    return ConfidentialClientApplication(
        client_id,
        authority=authority_url,
        client_credential=client_secret
    )

def acquire_access_token(app, code, scopes, redirect_uri):
    return app.acquire_token_by_authorization_code(code, scopes=scopes, redirect_uri=redirect_uri)

def fetch_user_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
    return response.json()

def authentication_process(app):
    scopes = ["User.Read"]
    redirect_uri = st.secrets["REDIRECT_URI"]
    query_params = st.query_params

    if "code" in query_params and "auth_code_handled" not in st.session_state:
        st.session_state["auth_code_handled"] = True
        token_result = acquire_access_token(app, query_params["code"], scopes, redirect_uri)
        if "access_token" in token_result:
            st.session_state["authenticated"] = True
            st.session_state["access_token"] = token_result["access_token"]
            st.session_state["user_data"] = fetch_user_data(token_result["access_token"])
            st.rerun()
        else:
            st.error("Authentication failed. Please try again.")
            st.stop()

    if "authenticated" not in st.session_state:
        auth_url = app.get_authorization_request_url(scopes, redirect_uri=redirect_uri)
        st.markdown(f"## Microsoft Login Required  \n[Click here to sign in]({auth_url})")
        st.stop()

# --- Dashboard Rendering ---
def dashboard_ui(powerbi_url):
    st.markdown(
        f"""
        <style>
            .report-container {{
                position: absolute;
                top: 20px;
                height: calc(100vh - 60px);
                width: 100%;
                margin: 0;
                padding: 0;
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
# --- Top Navigation Buttons ---
def btn_navigation():
    st.title("Executive Dashboards")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Delivery Dashboard",use_container_width=True,key="delivery_button"):
            st.session_state["active_dashboard"] = "Delivery"
    with col2:
        if st.button("Sales Dashboard", use_container_width=True):
            st.session_state["active_dashboard"] = "Sales"
    with col3:
        if st.button("Recruitment Dashboard", use_container_width=True):
            st.session_state["active_dashboard"] = "Recruitment"

# --- Main App ---
def main():
    app = initialize_app()
    authentication_process(app)

    if st.session_state.get("authenticated"):
        btn_navigation()

        selected = st.session_state.get("active_dashboard", "Delivery")

        if selected == "Delivery":
            dashboard_ui(st.secrets["DELIVERY_DASHBOARD_POWERBI_URL"])
        elif selected == "Sales":
            dashboard_ui(st.secrets["SALES_DASHBOARD_POWERBI_URL"])
        elif selected == "Recruitment":
            dashboard_ui(st.secrets["RECRUITMENT_DASHBOARD_POWERBI_URL"])

main()
