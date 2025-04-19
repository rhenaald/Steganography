# main.py

import streamlit as st

# ⬇️ Harus di baris pertama, sebelum import lokal atau Streamlit lain dipanggil
st.set_page_config(page_title="EchoHide", layout="wide", page_icon="🎧")

from ui import run_app

if __name__ == "__main__":
    run_app()
