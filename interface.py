import streamlit as st
from navbar import navbar
from helpers.fetchApi import fetch_attachment_data, fetch_data
from helpers.generateDocx import generate_docx
from runAgent import run_agent
import json

# API URLs
API_ATTACHMENT = "https://mincaai-1.app.flowiseai.com/api/v1/attachments/7d7fcbbd-d20f-4f06-a2cc-daefb9accd8c/2f2131c7-bd60-4102-9a1e-4ea9e5e2a9ef"
API_STOCK_ANALYSIS_1 = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/a3b63d2d-3f5f-4e40-97f7-e2d0f9f4c8e9"
API_STOCK_ANALYSIS_2 = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/5a92d92a-a6ea-4d88-bbe6-2c16f3d50e9f"
API_PDF_ANALYSIS = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/7d7fcbbd-d20f-4f06-a2cc-daefb9accd8c"
API_TARGET_STOCKS = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/df48fb74-0478-451e-8d62-49501ec20823"
API_REPORT_GENERATION = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/131cac63-bc31-4ccb-9c9a-8304f78fe8ed"

def interface():
    """Streamlit interface for generating financial reports."""

    # navbar()

    # Initialize session state
    for key in ["output1", "output2", "output3"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    # User input for market analysis
    st.subheader("Entrez votre prompt")
    prompt = st.text_area("Analyse sectorielle + Performance des entreprises", 
                          placeholder="Entrez la liste des entreprises\nEntrez le secteur des entreprises (à la ligne)", 
                          height=100, key="prompt2")
    prompt_lines = [p.strip() for p in prompt.split("\n") if p.strip()]

    # File uploader
    uploaded_files = st.file_uploader("Télécharger des fichiers PDF", accept_multiple_files=True, type=["pdf"], key="pdf_uploader")
    files = [("files", (file.name, file, file.type)) for file in uploaded_files]
    file_content = fetch_attachment_data(API_ATTACHMENT, files=files) if uploaded_files else None

    # Stock Analysis Agents
    col1, col2, col3 = st.columns([6, 6, 6])

    with col1:
        if prompt_lines:
            run_agent("Agent Performance des Actions", prompt_lines[0], API_STOCK_ANALYSIS_1, "output1", "update1")

    with col2:
        if len(prompt_lines) > 0:
            run_agent("Agent Actualité", "\n".join(prompt_lines[:2]), API_STOCK_ANALYSIS_2, "output2", "update2")

    with col3:
        if file_content:
            file_content_str = json.dumps(file_content, indent=2)
            combined_prompt = f"Stock Options: {st.session_state.output1}\nWebScrapper Result: {st.session_state.output2}\nMultiple files Content: {file_content_str}"
            run_agent("Agent Analyste", combined_prompt, API_PDF_ANALYSIS, "output3", "update3")

    
    # Ensure all outputs are available before generating the report
    if any([st.session_state.output1, st.session_state.output2, st.session_state.output3]):
    # if True:
        st.subheader("📂 Agent Note d’Analyse")

        # Placeholders
        download_btn_placeholder = st.empty()
        genReport_placeholder = st.empty()
        outputFile_placeholder = st.empty()

        with genReport_placeholder:
            with st.status("L’agent est prêt ...", expanded=True) as status:
                if st.button("🔄 Générez la note d’analyse"):
                    file_content_str = json.dumps(file_content, indent=2) if file_content else ""
                    stock_query = f"Stock Companies: {prompt_lines[0]}\nMultiple files Content: {file_content_str}" if prompt_lines else ""

                    agent4_result = fetch_data(API_TARGET_STOCKS, {"question": stock_query})
                    report_query = {
                        "question": f"Stock prices options: {st.session_state.output1}\n"
                                    f"Target stock prices: {agent4_result}\n"
                                    f"Report analysis: {st.session_state.output3}"
                    }

                    # Fetch generated report
                    st.session_state.generated_report = fetch_data(API_REPORT_GENERATION, report_query)

                    # Generate a DOCX file
                    st.session_state.docx_file = generate_docx(st.session_state.generated_report)

                    # Update status
                    status.update(label="✅ Report generated!", state="complete", expanded=False)

        # Ensure report output and download button persist
        if "generated_report" in st.session_state and "docx_file" in st.session_state:
            with download_btn_placeholder:
                st.download_button(
                    "📥 Téléchargez la note d’analyse en DOCX",
                    data=st.session_state.docx_file,
                    file_name="report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            outputFile_placeholder.write(st.session_state.generated_report)  # Display generated report
