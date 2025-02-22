import streamlit as st
from navbar import navbar
from helpers.fetchApi import *
from helpers.generateDocx import *
from runAgent import *

import json
from io import BytesIO
from docx import Document

def interface():
    st.set_page_config(page_title="Financial Report Generator", layout="wide")
    navbar()

    # Initialize session state for outputs if not already set
    if "output1" not in st.session_state:
        st.session_state.output1 = ""
    if "output2" not in st.session_state:
        st.session_state.output2 = ""
    if "output3" not in st.session_state:
        st.session_state.output3 = ""

    prompt = st.text_area(
        "Market analysis for tech stocks",
        placeholder="Enter list of stocks (i.e, AI, Tech, etc.)",
        height=100,
        key="prompt2"
    )

    uploaded_files = st.file_uploader("PDF File Uploader", accept_multiple_files=True, type=["pdf"], key="pdf_uploader")

    files = [("files", (file.name, file, file.type)) for file in uploaded_files]
    API_URL = "https://mincaai-1.app.flowiseai.com/api/v1/attachments/7d7fcbbd-d20f-4f06-a2cc-daefb9accd8c/bd13aae3-c806-46e0-8095-d48c9ccfea08"
    fileContent = fetch_attachment_data(API_URL, files=files)
            

    prompt_lines = [p.strip() for p in prompt.split("\n") if p.strip()]

    col1, col2, col3 = st.columns([6,6,6])
    

    with col1:
        prompt = prompt_lines[0] if len(prompt_lines) > 0 else ""
        run_agent(
            agent_name="Agent Stock Options",
            prompt_lines=prompt,
            api_url="https://mincaai-1.app.flowiseai.com/api/v1/prediction/b40044b1-c01e-4dc3-a60e-b4bf6c00dc96",
            key_output="output1",
            key_button="update1"
        )
    
    with col2:
        prompt = prompt_lines[0] + '\n'+ prompt_lines[1] if len(prompt_lines) > 1 else ""
        run_agent(
            agent_name="Agent Stock Options",
            prompt_lines=prompt,
            api_url="https://mincaai-1.app.flowiseai.com/api/v1/prediction/5a92d92a-a6ea-4d88-bbe6-2c16f3d50e9f",
            key_output="output2",
            key_button="update2"
        )

    
    with col3:
        #if st.session_state.output1 and st.session_state.output2:
            if fileContent:
                fileContentStr = json.dumps(fileContent, indent=2)  
                prompt = "Stock Options: "+ {st.session_state.output1} + '\nWebScrapper Result: '+ {st.session_state.output2} + '\nFile Content: '+ fileContentStr 
                run_agent(
                    agent_name="Agent PDF Analysis",
                    prompt_lines=prompt,
                    api_url="https://mincaai-1.app.flowiseai.com/api/v1/prediction/7d7fcbbd-d20f-4f06-a2cc-daefb9accd8c",
                    key_output="output3",
                    key_button="update3"
                )

    st.subheader("📂 Agent Document Generator")
    download_btn_placeholder = st.empty()  
    genReport_placeholder = st.empty()
    outputFile_placeholder = st.empty()
    
    # Placeholder for download button

    fileContentStr = json.dumps(fileContent, indent=2)  
    prompt4 = "Stock Companies: "+ {prompt_lines[0]} + '\nFile Content: '+ fileContentStr 
    API_URL = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/df48fb74-0478-451e-8d62-49501ec20823"
    agent4Result = fetch_data(API_URL, {
        "question": prompt4
    })

    
    if any([st.session_state.output1, st.session_state.output2, st.session_state.output3]):
        with genReport_placeholder:
            with st.status("Agent is ready ...", expanded=True) as status:
                if st.button("🔄 Generate Report"):   

                    API_URL = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/131cac63-bc31-4ccb-9c9a-8304f78fe8ed"
                    reportContent = fetch_data(API_URL, {
                        "question": f"Stock prices options: {st.session_state.output1}\nTarget stock prices: {agent4Result}\nReport analysis: {st.session_state.output3}"
                    })

                    # Save report content in session state
                    st.session_state.generated_report = reportContent  

                    # Generate DOCX file
                    st.session_state.docx_file = generate_docx(reportContent)

                    status.update(label="✅ Report generated!", state="complete", expanded=False)

        # Ensure report and download button persist
        if "generated_report" in st.session_state and "docx_file" in st.session_state:
            with download_btn_placeholder:
                st.download_button(
                    label="📥 Download Report as DOCX",
                    data=st.session_state.docx_file,
                    file_name="report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            outputFile_placeholder.write(st.session_state.generated_report)

    else:
        st.error("Please validate at least one agent before generating the report.")

