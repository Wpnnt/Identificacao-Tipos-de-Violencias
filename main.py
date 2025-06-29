import streamlit as st # type: ignore
from engine.expert_system import ExpertSystem
from engine.facts import *
from form import *
from engine.classifier import *


st.set_page_config(
    page_title="Sistema Especialista",
    page_icon=":robot:",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.title("Sistema Especialista de Identificação de Violência")

#====================formulario========================

user_type_action = ask_type_action()
user_context = ask_context()
user_target = ask_target()


#====================processamento========================

if st.button("Avaliar"):
    if not user_type_action or not user_context or not user_target:
        st.error("Por favor, preencha todas as informações.")
    else:
        engine = ExpertSystem()
        engine.reset()

        for action in user_type_action:
            for t in user_target:
                engine.declare(ViolenceRelact(
                    action_type=action,
                    context=user_context,
                    target=t
                ))

        engine.run()

        if engine.results:
            st.success("Resultados encontrados: ")
            for r in engine.results:
                subtype = r["subtype"].replace("_", " ").capitalize()
                confidence_pct = round(r["confidence"] * 100)
                st.markdown(f"- **{subtype}** (Confiança: **{confidence_pct}%**)")
        else:
            st.info("Nenhum tipo de violência identificado com base nas informações fornecidas.")


