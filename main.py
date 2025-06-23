import streamlit as st

st.set_page_config(
    page_title="Sistema Especialista",
    page_icon=":robot:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("<h1>Guia de tipos de violencia</h1>", unsafe_allow_html=True)

user_input = st.text_input("Entrada: ")

# função de debug
if user_input:
    st.write(f"Você: {user_input}")