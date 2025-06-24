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

#ter que usar o spacy pra interpretar o texto do usuario e separar os dados coletados
#def spacy_interpreter(text):


#codigo recomendado pelo gepeto, precisa ser testado e traduzido para ingles
"""
import spacy
from engine.facts import RelatoDeViolencia

nlp = spacy.load("pt_core_news_sm")

def interpretar_com_spacy(texto):
    doc = nlp(texto.lower())
    
    # Define palavras-chave possíveis para cada campo
    acoes = ["piada", "comentário", "perseguir", "insulto", "ameaça"]
    contextos = ["trabalho", "escola", "ambiente público"]
    alvos = ["mulher", "minorias", "negro", "pessoa com deficiência", "lgbt"]

    campos = {"tipo_acao": None, "contexto": None, "alvo": None}

    for token in doc:
        if token.text in acoes:
            campos["tipo_acao"] = token.text
        elif token.text in contextos:
            campos["contexto"] = token.text
        elif token.text in alvos:
            campos["alvo"] = token.text

    if any(v is not None for v in campos.values()):
        return RelatoDeViolencia(**{k: v for k, v in campos.items() if v is not None})
    else:
        return None
"""