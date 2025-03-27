import streamlit as st
from firebase_auth import is_email_allowed
import json

if not st.experimental_user.is_logged_in:
    if st.button("Log in with SharePoint"):
        st.login()
    st.stop()

user_email = st.experimental_user.preferred_username
print(user_email)



# Logout button
if st.button("Log out"):
    st.logout()
