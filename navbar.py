import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
from models.Report import Report
from sharepoint import SharePointClient

def navbar():
    # Ensure session state has selected_page
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Note d’analyse sectorielle"

    with st.sidebar:
        selected = option_menu(
            menu_title="Vixis - Note d’analyse",
            options=["Note d’analyse sectorielle", "Note d’analyse mono sous-jacent"],
            menu_icon="menu-up",
            default_index=["Note d’analyse sectorielle", "Note d’analyse mono sous-jacent"].index(st.session_state.selected_page),
            key="navigation",
            styles={
                "container": {
                    "background-color": "#F8F9FA",
                    "padding": "10px",
                    "border-radius": "8px",
                },
                "icon": {"color": "#4B0082", "font-size": "22px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "5px",
                    "padding": "12px",
                    "color": "#333333",
                    "border-radius": "5px",
                    "transition": "0.3s ease-in-out",
                    "font-family": "Arial, sans-serif",
                },
                "nav-link-selected": {
                    "background-color": "#4B0082",
                    "color": "white",
                    "font-weight": "bold",
                    "font-family": "Arial, sans-serif",
                },
            }
        )

        # Update session state with selection
        st.session_state.selected_page = selected

        # Centered button with same style as navbar
        st.markdown(
            """
            <style>
                .update-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-top: 20px;
                }
                .update-button {
                    background-color: #4B0082;
                    color: white;
                    font-size: 21px;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                    padding: 12px 20px;
                    border-radius: 5px;
                    width: 100%;
                    text-align: center;
                    cursor: pointer;
                    transition: 0.3s ease-in-out;
                    border: none;
                }
                .update-button:hover {
                    background-color: #5A0099;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Centered button (real Streamlit button inside styled layout)

        if st.button("Update Data", key="update_data", help="Click to refresh data"):
                with st.spinner("Updating data... ⏳"):
                    sp = SharePointClient()
                    sp.load_data()
                    st.success("✅ Data updated successfully!")

