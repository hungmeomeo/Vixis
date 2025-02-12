import streamlit as st
from datetime import datetime
from models.Report import Report
from navbar import navbar
    

def content():
    st.set_page_config(page_title="Financial Report Generator", layout="wide")


    # Placeholder for navbar (assumed function)
    navbar()  

    # Layout: 3 Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Prompt")
        #prompt1 = st.text_area("Companies & Indices", "NVIDIA, Apple Inc, Amazon, Microsoft, etc...", height=100)
        prompt1 = st.text_input("Companies & Indices", placeholder="NVIDIA, Apple Inc, Amazon, Microsoft, etc..." )
        st.subheader("Agent Webscraper")
        output1 = st.text_area("Output", "XXXX\nXXXX\nXXXXXX")
        if st.button("Validate", key="validate1"):
            st.session_state["validate1"] = True
            st.success("Validated")
        st.button("Update prompt", key="update1")


    with col2:
        st.subheader("Prompt")
        prompt2 = st.text_area("Description of report", "" , height=100)
        print(prompt2)

        st.subheader("Agent Stock Options")
        output2 = st.text_area("Output1", "XXXX\nXXXX\nXXXXXX")
        if st.button("Validate", key="validate2"):
            st.session_state["validate2"] = True
            st.success("Validated")
        st.button("Update prompt", key="update2")

    with col3:
        st.subheader("PDF File Uploader")
        
        st.file_uploader("Upload PDF file", type=["pdf"])
        
        st.subheader("Agent Analysis Engine")
        output3 = st.text_area("Output2", "XXXX\nXXXX\nXXXXXX")
        if st.button("Validate", key="validate3"):
            st.session_state["validate3"] = True
            st.success("Validated")
        st.button("Update prompt", key="update3")

   

    # Ensure session state is initialized
    for key in ["validate1", "validate2", "validate3"]:
        if key not in st.session_state:
            st.session_state[key] = False

    # Generate Report Button
    if st.button("Generate Report"):
        if all([st.session_state["validate1"], st.session_state["validate2"], st.session_state["validate3"]]):
            st.success("Report generated!")
            st.text_area("Generated Report", "Report content goes here...", height=200)
        else:
            st.error("Please validate all three agents before generating the report.")