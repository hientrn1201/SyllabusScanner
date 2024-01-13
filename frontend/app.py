import streamlit as st
from streamlit_ace import st_ace
import json
import requests
from helper.token_helper import num_tokens_from_string
from helper.pdf_scraper import scrape

st.title("Syllabus Extractor")

openai_api_key = st.text_input("OpenAI API Key", type="password")
notion_api_key = st.text_input("Notion API Key", type="password")
notion_database_id = st.text_input("Notion Database ID", type="password")
file = st.file_uploader("Upload Syllabus", type=["pdf"])

if file is not None:
    button = st.button("Extract", disabled=False)
    if button:
        if not openai_api_key:
            st.error("Please enter OpenAI API Key")
        else:
            text = scrape(file)
            if num_tokens_from_string(text, "cl100k_base") > 13000:
                st.error(
                    "Syllabus too long, please upload a syllabus with less than 13000 tokens")
            else:
                data = {"openai_api_key": openai_api_key, "text": text}
                response = requests.post(
                    f"{st.secrets['backend_url']}/extract", json=data)

                if response.status_code == 200:
                    st.session_state['data'] = response.json().get('data')
                else:
                    st.error(response.json().get('error'))

if st.session_state.get("data") is not None:
    st.subheader("Extracted Data (editable)")
    formatted = json.dumps(st.session_state['data'], indent=4)

    st.session_state['data'] = json.loads(st_ace(
        value=formatted,
        language="java",
        theme="solarized_dark",
        keybinding="vscode",
        min_lines=20,
        max_lines=50,
        font_size=14,
        tab_size=4,
        wrap=False,
        show_gutter=True,
        show_print_margin=False,
        annotations=None,
    ))

    if not notion_api_key or not notion_database_id:
        st.button("Save to Notion", disabled=True)
        st.error("Please enter Notion API Key and Database ID")
    else:
        button_export_notion = st.button("Export to Notion", disabled=False)
        if button_export_notion:
            if not notion_api_key or not notion_database_id:
                st.error("Please enter Notion API Key and Database ID")
            else:
                data = {"notion_api_key": notion_api_key,
                        "notion_database_id": notion_database_id, "data": st.session_state['data']}
                response = requests.post(
                    f"{st.secrets['backend_url']}/save_to_notion", json=data)

                if response.status_code == 200:
                    st.success("Successfully created Notion page")
                else:
                    st.error(
                        f"Error creating Notion page. {response.json().get('error')}")
