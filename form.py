import streamlit as st

def ask_type_action():
    st.subheader("Tipo de ação observada")
    options = []

    if st.checkbox("Alguém fez uma piada com você?"):
        options.append("piada")
    if st.checkbox("Alguém fez um comentário ofensivo ou esteoripado sobre você?"):
        options.append("comentario")
    if st.checkbox("Voce se sentiu vigiado(a), perseguido(a) ou intimidado(a)?"):
        options.append("perseguir")
    return options

def ask_context():
    st.subheader("Contexto da situação")
    return st.selectbox("Onde isso aconteceu?", ["", "trabalho", "escola", "ambiente publico", "casa", "outro"])

def ask_target():
    st.subheader("Você acredita que foi alvo disso por: ")
    target = []

    if st.checkbox("Ser mulher?"):
        target.append("genero")
    if st.checkbox("Pertencer ao grupo LGBTQIA+?"):
        target.append("genero")
    if st.checkbox("Ter uma cor de pele diferente do agressor?"):
        target.append("minoria")
    if st.checkbox("Ser uma pessoa com algum tipo de deficiência?"):
        target.append("minoria")
    return target

    #versão mais especifica, é melhor seguir com ela no futuro:
    """
    #aqui talvez seja interessante adicionar/mudar alguma coisa
    if st.checkbox("Ser mulher?"):
        target.append("genero")
    if st.checkbox("Pertencer ao grupo LGBTQIA+?"):
        target.append("genero")
    if st.checkbox("Ter uma cor de pele diferente do agressor?"):
        target.append("raça")
    if st.checkbox("Ser uma pessoa com algum tipo de deficiência?"):
        target.append("deficiencia")
    return target
    """
