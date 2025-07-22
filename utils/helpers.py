import time
import streamlit as st

def parse_suggestions(suggestions):
    if isinstance(suggestions, str):
        return [s.strip("-• ").strip() for s in suggestions.strip().split("\n") if s.strip()]
    elif isinstance(suggestions, list):
        return [s.strip("-• ").strip() for s in suggestions if isinstance(s, str) and s.strip()]
    return []

def render_streamed_markdown(markdown_text, delay=0.02):
    container = st.empty()
    output = ""
    for char in markdown_text:
        output += char
        container.markdown(output)
        time.sleep(delay)