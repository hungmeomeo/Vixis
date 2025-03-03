import streamlit as st
from datetime import datetime
from models.Report import Report
from streamlit_option_menu import option_menu

def navbar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Vixis - Note d’analyse",
            options=["Note d’analyse sectorielle", "Note d’analyse mono sous-jacent"],
            menu_icon="menu-up",
            default_index=["Note d’analyse sectorielle", "Note d’analyse mono sous-jacent"].index(st.session_state.selected_page),
            key="navigation",
            styles={
                "container": {"background-color": "transparent"},
                "icon": {"color": "white", "font-size": "20px"},  
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                    "color": "#808080",
                    "background-color": "transparent",
                },
                "nav-link-selected": {"background-color": "#666699", "color": "white"},
            }
        )
        st.session_state.selected_page = selected  # Store selection in session state
