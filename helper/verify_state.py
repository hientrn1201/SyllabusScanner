import streamlit as st


def verify_openai_api_key():
    if st.session_state.get("openai_api_key") == "":
        return False
    return True


def verify_notion_key():
    if st.session_state.get("notion_api_key") == "" or st.session_state.get("notion_database_id") == "":
        return False
    return True
