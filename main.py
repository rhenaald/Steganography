# main.py
import streamlit as st
from ui import run_app

if __name__ == "__main__":
    st.set_page_config(page_title="EchoHide", page_icon="🎧")
    run_app()
