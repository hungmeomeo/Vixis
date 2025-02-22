from helpers.fetchApi import *
import streamlit as st

def run_agent(agent_name,prompt_lines, api_url, key_output, key_button):
    """
    Function to run an agent in a specified Streamlit column.

    Parameters:
    - agent_name (str): The display name of the agent.
    - col (streamlit column): The Streamlit column where the agent will be displayed.
    - prompt_lines (list): List of user-inputted stock prompts.
    - api_url (str): The API endpoint to fetch data.
    - key_output (str): The session state key for storing output.
    - key_button (str): The unique key for the button to trigger the agent.
    """
    st.subheader(agent_name)
    agent_placeholder = st.empty()
    output_placeholder = st.empty()
    output_placeholder.write(st.session_state.get(key_output, ""))  # Persist output

    with agent_placeholder:
            with st.status("Agent is ready ...", expanded=True) as status:
                if st.button("Run prompt", key=key_button):
                    if prompt_lines:
                        st.session_state[key_output] = fetch_data(api_url, {"question": prompt_lines})
                        output_placeholder.write(st.session_state[key_output])
                        status.update(label="Download complete!", state="complete", expanded=False)
                