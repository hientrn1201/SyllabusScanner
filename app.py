import streamlit as st
from extraction.extraction import Extraction
from helper.token_helper import num_tokens_from_string
from helper.verify_state import verify_openai_api_key, verify_notion_key
from streamlit_ace import st_ace
import json

from notion.syllabus_notion import SyllabusNotion


def export_to_notion():
    notion_service = SyllabusNotion(
        st.session_state['notion_api_key'],
        st.session_state['notion_database_id'],
        st.session_state['data']
    )

    response = notion_service.create_syllabus_notion_page()
    st.session_state['response'] = response


st.title("Syllabus Extractor")

st.session_state['openai_api_key'] = st.text_input(
    "OpenAI API Key", type="password")
st.session_state['notion_api_key'] = st.text_input(
    "Notion API Key", type="password")
st.session_state['notion_database_id'] = st.text_input(
    "Notion Database ID", type="password")
file = st.file_uploader("Upload Syllabus", type=["pdf"])
if file is not None:
    button = st.button(
        "Extract", disabled=True if st.session_state.get("data") else False)
    if button:
        if verify_openai_api_key():
            # st.write(st.session_state['openai_api_key'])
            extraction_service = Extraction(
                openai_api_key=st.session_state['openai_api_key'])
            text = extraction_service.scrape(file)
            if num_tokens_from_string(text, "cl100k_base") > 13000:
                st.error(
                    "Syllabus too long, please upload a syllabus with less than 13000 tokens")
            else:
                st.session_state['data'] = extraction_service.extract(text)

            if st.session_state['data'] is None:
                st.error(
                    "Error extracting data, please check your OpenAI API Key and the length of the syllabus or try again later")

        else:
            st.error("Please enter OpenAI API Key")

if st.session_state.get("data") is not None:
    st.subheader("Extracted Data (editable)")
    formatted = json.dumps(
        st.session_state['data'],
        indent=4,
    )

    st.session_state['data'] = json.loads(st_ace(
        value=formatted,
        language="java",
        theme="solarized_dark",
        keybinding="vscode",
        min_lines=20,
        max_lines=None,
        font_size=14,
        tab_size=4,
        wrap=False,
        show_gutter=True,
        show_print_margin=False,
        annotations=None,
    ))

    if verify_notion_key():
        st.button("Save to Notion",
                  on_click=export_to_notion, disabled=True if st.session_state.get("response") else False)
    else:
        st.button("Save to Notion", disabled=True)
        st.error("Please enter Notion API Key and Database ID")

if st.session_state.get("response"):
    if st.session_state['response'].status_code == 200:
        st.success("Successfully created Notion page")
    else:
        st.error("Error creating Notion page")
        st.error(st.session_state['response'].text)
