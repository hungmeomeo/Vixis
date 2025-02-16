import streamlit as st
from streamlit_js_eval import streamlit_js_eval  # Handles cookies
from datetime import datetime
from models.Report import Report
from navbar import navbar
from interface import interface

# Define user credentials (replace with DB lookup for real apps)
CREDENTIALS = {
    "username": "1",
    "password": "1"
}

# Function to get user session from cookies
def get_user_session():
    return streamlit_js_eval(js_expressions="document.cookie", want_output=True)

# Function to set cookies using JavaScript
def set_cookie(key, value):
    streamlit_js_eval(js_expressions=f"document.cookie = '{key}={value}; path=/'")

# Function to clear cookies using JavaScript
def clear_cookies():
    streamlit_js_eval(js_expressions="""
        document.cookie.split(";").forEach(function(c) { 
            document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
        });
    """)

# Authentication function
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username", key="username_input")
    password = st.sidebar.text_input("Password", type="password", key="password_input")
    login_button = st.sidebar.button("Login", key="login_button")

    if login_button:
        if username == CREDENTIALS["username"] and password == CREDENTIALS["password"]:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            set_cookie("user_session", username)  # Store login in cookies
            st.sidebar.success(f"Logged in as {username}")
            st.rerun()  # ✅ FIXED: Refresh properly
        else:
            st.sidebar.error("Invalid credentials")

def main():
    st.set_page_config(page_title="Financial Report Generator", layout="wide")

    navbar()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Prompt")
        prompt1 = st.text_input("Companies & Indices", placeholder="NVIDIA, Apple Inc, Amazon, Microsoft, etc...", key="prompt1")
        st.subheader("Agent Webscraper")
        output1 = st.text_area("Output", "XXXX\nXXXX\nXXXXXX", key="output1")
        if st.button("Validate", key="validate1"):
            st.session_state["validate1"] = True
            st.success("Validated")
        st.button("Update prompt", key="update1")

    with col2:
        st.subheader("Prompt")
        prompt2 = st.text_area("Description of report", "", height=100, key="prompt2")
        st.subheader("Agent Stock Options")
        output2 = st.text_area("Output1", "XXXX\nXXXX\nXXXXXX", key="output2")
        if st.button("Validate", key="validate2"):
            st.session_state["validate2"] = True
            st.success("Validated")
        st.button("Update prompt", key="update2")

    with col3:
        st.subheader("PDF File Uploader")
        st.file_uploader("Upload PDF file", type=["pdf"], key="pdf_uploader")
        st.subheader("Agent Analysis Engine")
        output3 = st.text_area("Output2", "XXXX\nXXXX\nXXXXXX", key="output3")
        if st.button("Validate", key="validate3"):
            st.session_state["validate3"] = True
            st.success("Validated")
        st.button("Update prompt", key="update3")

    # Ensure session state is initialized
    for key in ["validate1", "validate2", "validate3"]:
        if key not in st.session_state:
            st.session_state[key] = False

    # Generate Report Button
    if st.button("Generate Report", key="generate_report"):
        if all([st.session_state["validate1"], st.session_state["validate2"], st.session_state["validate3"]]):
            st.success("Report generated!")
            st.text_area("Generated Report", "Report content goes here...", height=200, key="generated_report")
        else:
            st.error("Please validate all three agents before generating the report.")

if __name__ == "__main__":
    interface()
    # main()
