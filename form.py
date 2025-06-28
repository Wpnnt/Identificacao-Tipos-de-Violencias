import streamlit as st

def ask_type_action():
    st.subheader("Tipo de ação observada")
    options = []

    if st.checkbox("Piadas ou comentários sobre estereótipos"):
        options.append("Piadas ou comentários sobre estereótipos")

    if st.checkbox("Perseguição ou vigilância constante"):
        options.append("Perseguição ou vigilância constante")

    if st.checkbox("Exclusão ou restrição de participação"):
        options.append("Exclusão ou restrição de participação")

    return options

def ask_context():
    st.subheader("Contexto da situação")
    return st.selectbox("Onde isso aconteceu?", [
        "", 
        "Espaço público no campus", 
        "Ambiente administrativo", 
        "Sala de aula"
    ])

def ask_target():
    st.subheader("Você acredita que foi alvo disso por:")
    options = []
    if st.checkbox("Gênero"):
        options.append("Gênero")
    if st.checkbox("Raça ou etnia"):
        options.append("Raça ou etnia")
    return options