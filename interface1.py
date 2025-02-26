import streamlit as st
from navbar import navbar
from helpers.fetchApi import fetch_attachment_data, fetch_data
from helpers.generateDocx import generate_docx
from runAgent import run_agent
import json

# API URLs
API_ATTACHMENT = "https://mincaai-1.app.flowiseai.com/api/v1/attachments/fecc2cff-f971-401e-8eeb-de68484888d1/b49aa47d-d507-4b4c-a731-ebacbf08725e"
API_STOCK_ANALYSIS_1 = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/411b7434-e4c5-4976-9dd2-35d793b58947"
API_STOCK_ANALYSIS_2 = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/5a92d92a-a6ea-4d88-bbe6-2c16f3d50e9f"
API_PDF_ANALYSIS = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/fecc2cff-f971-401e-8eeb-de68484888d1"
API_REPORT_GENERATION = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/f80e1f89-b069-4139-b93b-19042ec800a2"

def interface1():
    """Streamlit interface for generating financial reports."""

    # navbar()

    # Initialize session state
    for key in ["output4", "output5", "output6"]:
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
            run_agent("Agent Données Financières", prompt_lines[0], API_STOCK_ANALYSIS_1, "output4", "update1")

    with col2:
        if len(prompt_lines) > 1:
            run_agent("Agent Actualité", "\n".join(prompt_lines[:2]), API_STOCK_ANALYSIS_2, "output5", "update2")

    with col3:
        if file_content:
            file_content_str = json.dumps(file_content, indent=2)
            combined_prompt = f"WebScrapper Result: {st.session_state.output5}\nMultiple files Content: {file_content_str}"
            run_agent("Agent Analyste", combined_prompt, API_PDF_ANALYSIS, "output6", "update3")

    
    # Ensure all outputs are available before generating the report
    if any([st.session_state.output4, st.session_state.output5, st.session_state.output6]):
    # if True:
        st.subheader("📂 Agent Note d’Analyse")

        # Placeholders
        download_btn_placeholder = st.empty()
        genReport_placeholder = st.empty()
        outputFile_placeholder = st.empty()

        with genReport_placeholder:
            with st.status("L’agent est prêt ...", expanded=True) as status:
                if st.button("🔄 Générez la note d’analyse"):
                    report_query = {
                        "question": f"Stock prices options: {st.session_state.output4}\n"
                                    f"Report analysis: {st.session_state.output6}"
                    }
                    # Fetch generated report
                    st.session_state.generated_report_2 = fetch_data(API_REPORT_GENERATION, report_query)

                    # Generate a DOCX file
                    st.session_state.docx_file_2 = generate_docx(st.session_state.generated_report_2)

                    # Update status
                    status.update(label="✅ Report generated!", state="complete", expanded=False)

        # Ensure report output and download button persist
        if "generated_report_2" in st.session_state and "docx_file_2" in st.session_state:
            with download_btn_placeholder:
                st.download_button(
                    "📥 Téléchargez la note d’analyse en DOCX",
                    data=st.session_state.docx_file_2,
                    file_name="report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            outputFile_placeholder.write(st.session_state.generated_report_2)  # Display generated report
