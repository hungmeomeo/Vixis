import streamlit as st
from datetime import datetime
from models.Report import Report
    
def navbar():
    if 'reports' not in st.session_state:
        st.session_state.reports = []  # Store list of reports
    if 'current_report' not in st.session_state:
        st.session_state.current_report = None  # Currently selected report
    if 'report_contents' not in st.session_state:
        st.session_state.report_contents = {}  # Store report content dynamically
    if 'renaming_report' not in st.session_state:
        st.session_state.renaming_report = None  # Track rename mode

    # Create a new report
    def create_new_report():
        new_report_name = f"Report {len(st.session_state.reports) + 1}"
        timestamp = datetime.now().strftime("%Y-%m-%d")
        new_report = Report(new_report_name, timestamp)
        st.session_state.reports.append(new_report.name)
        st.session_state.report_contents[new_report.name] = ""  # Initialize report content
        st.session_state.current_report = new_report.name

    # Rename a report
    def rename_report(old_name, new_name):
        if new_name and new_name != old_name and new_name not in st.session_state.reports:
            st.session_state.reports[st.session_state.reports.index(old_name)] = new_name
            st.session_state.report_contents[new_name] = st.session_state.report_contents.pop(old_name)
            if st.session_state.current_report == old_name:
                st.session_state.current_report = new_name
            st.session_state.renaming_report = None  # Exit rename mode
            st.rerun()

    # Delete a report
    def delete_report(report_name):
        if report_name in st.session_state.reports:
            st.session_state.reports.remove(report_name)
            st.session_state.report_contents.pop(report_name, None)  # Remove content
            if st.session_state.current_report == report_name:
                st.session_state.current_report = None  # Reset selection
        st.rerun()

    # Sidebar for managing reports
    st.sidebar.title("📊 Vixis - Reports")
    st.sidebar.header("Manage Reports")

    if st.sidebar.button("New Report ➕"):
        
        create_new_report()

    # Display existing reports with rename & delete buttons
    for report in reversed(st.session_state.reports):
        col1, col2, col3 = st.sidebar.columns([10, 2, 2])  # Adjusted column widths

        with col1:
            if st.session_state.renaming_report == report:
                # Show text input for renaming
                new_name = st.text_input("", report, key=f"rename_input_{report}")
                if new_name and new_name != report:
                    rename_report(report, new_name)
            else:
                # Show button for selecting report
                if st.button(report, key=f"report_{report}"):
                    st.session_state.current_report = report

        with col2:
            if st.button("✏️", key=f"rename_{report}"):
                st.session_state.renaming_report = report  # Enter rename mode

        with col3:
            if st.button("🗑️", key=f"delete_{report}"):
                delete_report(report)

