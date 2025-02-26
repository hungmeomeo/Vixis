import streamlit as st
from streamlit_js_eval import streamlit_js_eval  # Handles cookies
from datetime import datetime
from models.Report import Report
from navbar import navbar
from interface import interface
from interface1 import interface1


if __name__ == "__main__":
    st.set_page_config(page_title="Financial Report Generator", layout="wide")

    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Note d’analyse sectorielle"

    navbar()
    
    if st.session_state.selected_page == "Note d’analyse sectorielle":
        st.title("Note d’analyse sectorielle")
        interface()
    elif st.session_state.selected_page == "Note d’analyse mono sous-jacent":
        st.title("Note d’analyse mono sous-jacent")
        interface1()
    # main()
