import streamlit as st
import requests
from navbar import navbar

# Function to fetch data from API
def fetch_data(api_url, payload):
    try:
        response = requests.post(api_url, json=payload)
        data = response.json().get('text', "No response received.")
        return data
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def interface():
    st.set_page_config(page_title="Financial Report Generator", layout="wide")
    navbar()
    

        # Layout: 3 Columns
    col1, col2, col3 = st.columns([6,6,6])

    ### Column 1: Web Scraper
    with col1:
        st.subheader("Prompt")
        prompt1 = st.text_area(
            "Companies & Indices",
            placeholder="NVIDIA, Apple Inc, Amazon, Microsoft, etc...",
            height=100,
            key="prompt1"
        )

        st.subheader("Agent Webscraper")
        output1_placeholder = st.empty()  # Placeholder for dynamic output

        with st.status("Agent is ready ...", expanded=True) as status:
            if st.button("Update prompt", key="update1"):
                if prompt1.strip():
                    output1 = fetch_data("https://mincaai.app.flowiseai.com/api/v1/prediction/645e41db-37ad-4466-b368-15d04a28b50a",
                                        {"question": prompt1})
                    st.write(output1)
                    status.update(label="Download complete!", state="complete", expanded=False)
                else:
                    st.warning("Please enter a valid company or index.")
                    status.update(label="Please enter a valid company or index.", state="error", expanded=False)

    ### Column 2: Stock Options
    with col2:
        st.subheader("Description of Report")
        prompt2 = st.text_area(
            "Enter details about the report",
            placeholder="E.g., Market analysis for tech stocks...",
            height=100,
            key="prompt2"
        )

        st.subheader("Agent Stock Options")
        output2_placeholder = st.empty()

        with st.status("Agent is ready ...", expanded=True) as status:
            if st.button("Update prompt", key="update2"):
                if prompt2.strip():
                    output2 = fetch_data("https://mincaai.app.flowiseai.com/api/v1/prediction/def0efd9-158a-46a3-b334-5e061d6dc535",
                                        {"question": prompt2})
                    st.write(output2)
                    status.update(label="Download complete!", state="complete", expanded=False)
                else:
                    st.warning("Please enter a report description.")
                    status.update(label="Please enter a report description.", state="error", expanded=False)

    ### Column 3: Analysis Engine
    with col3:
        st.subheader("PDF File Uploader")
        uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"], key="pdf_uploader")

        st.subheader("Agent Analysis Engine")
        output3_placeholder = st.empty()

        with st.status("Agent is ready ...", expanded=True) as status:
            if st.button("Analyze PDF", key="update3"):
                if uploaded_file:
                    output3 = fetch_data("https://mincaai.app.flowiseai.com/api/v1/prediction/your-agent-id-here",
                                        {"file_name": uploaded_file.name})
                    st.write(output3)
                    status.update(label="Analysis complete!", state="complete", expanded=False)
                else:
                    st.warning("Please upload a PDF file.")
                    status.update(label="Please upload a PDF file.", state="error", expanded=False)

    st.button("Generate Report", key="generate_report")


# if st.button("Update prompt", key="update1"):
#         if prompt1.strip():
#             output1 = fetch_data("https://mincaai.app.flowiseai.com/api/v1/prediction/645e41db-37ad-4466-b368-15d04a28b50a",{"question": prompt1})
#             print(prompt1, output1)
#             # output1_placeholder.text_area("Output", value=output1, height=150, disabled=True)
#             st.chat_message(output1)
#         else:
#             st.warning("Please enter a valid company or index.")

# Column 2: Stock Options

