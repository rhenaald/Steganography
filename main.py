import streamlit as st

st.set_page_config(page_title="EchoHide", layout="wide", page_icon="🎧")

from ui import run_app

if __name__ == "__main__":
    run_app()
