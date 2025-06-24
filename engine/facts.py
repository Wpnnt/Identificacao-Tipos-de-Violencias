from experta import Fact
from knowledge_base.violence_types import VIOLENCE_TYPES, SEVERITY_LEVEL, REPORT_CONTACT
import streamlit as st

class ViolenceRelact(Fact):
    
    #representa o relato que o usuario fez sobre a violencia
    
    pass

def print_information(violence_type):
    info = VIOLENCE_TYPES.get(violence_type)
    if not info:
        st.warning("Informações adicionais não disponíveis.")
        return

    st.markdown(f"### ✅ {violence_type.replace('_', ' ').title()}")
    st.markdown(f"**Definição:** {info.get('definicao')}")

    severity = info.get('gravidade')
    if severity:
        st.markdown(f"**Gravidade:** {SEVERITY_LEVEL.get(severity, '')}")

    contacts = info.get("canais_denuncia", [])
    for contact in contacts:
        contact_info = REPORT_CONTACT.get(contact)
        if contact_info:
            st.markdown(f"- **{contact}**: {contact_info.get('descricao')}")
            if "contato" in contact_info:
                st.markdown(f"  📧 Contato: `{contact_info['contato']}`")
            st.markdown(f"  📌 Procedimento: {contact_info.get('procedimento')}")

    recommendations = info.get("recomendacoes", [])
    if recommendations:
        st.markdown("**Recomendações:**")
        for r in recommendations:
            st.markdown(f"- {r}")