from experta import Fact, Field
from knowledge_base.violence_types import VIOLENCE_TYPES, SEVERITY_LEVEL, REPORT_CONTACT
import streamlit as st  # type: ignore

class TextRelato(Fact):
    text = Field(str, mandatory=True)
    processed = Field(bool, default=False)

class KeywordFact(Fact):
    category = Field(str, mandatory=True)
    keyword = Field(str, mandatory=True)

class ViolenceBehavior(Fact):
    behavior_type = Field(str, mandatory=True)

class ContextFact(Fact):
    location = Field(str, mandatory=True)

class FrequencyFact(Fact):
    value = Field(str, mandatory=True)

class TargetFact(Fact):
    characteristic = Field(str, mandatory=True)

class RelationshipFact(Fact):
    type = Field(str, mandatory=True)

class ImpactFact(Fact):
    type = Field(str, mandatory=True)

class ViolenceClassification(Fact):
    """
    Representa o resultado da classificação de um tipo de violência.
    """
    violence_type = Field(str, mandatory=True)  # Tipo principal de violência
    subtype = Field(str, default="")           # Subtipo (se aplicável)
    explanation = Field(list, default=[])      # Lista de explicações

class AnalysisResult(Fact):
    """
    Armazena o resultado final da análise
    """
    classifications = Field(list, default=[])   # Lista de classificações 
    primary_result = Field(dict, default=None)  # Resultado principal
    multiple_types = Field(bool, default=False) # Indica se foram encontrados múltiplos tipos\

def create_facts_from_groq_response(response):
    facts = []
    if "identified_keywords" in response and response["identified_keywords"]:
        keywords = response["identified_keywords"]
        for category, values in keywords.items():
            for keyword in values:
                facts.append(KeywordFact(category=category, keyword=keyword))
                if category == "action_type":
                    facts.append(ViolenceBehavior(behavior_type=keyword))
                elif category == "context":
                    facts.append(ContextFact(location=keyword))
                elif category == "frequency":
                    facts.append(FrequencyFact(value=keyword))
                elif category == "target":
                    facts.append(TargetFact(characteristic=keyword))
                elif category == "relationship":
                    facts.append(RelationshipFact(type=keyword))
                elif category == "impact":
                    facts.append(ImpactFact(type=keyword))
    return facts

def print_information(violence_type, subtype=None, confidence=None):
    info = VIOLENCE_TYPES.get(violence_type)
    if not info:
        st.warning("Informações adicionais não disponíveis.")
        return
    
    title = violence_type.replace('_', ' ').title()
    if subtype and subtype in info.get('subtipos', {}):
        subtype_info = info['subtipos'][subtype]
        title += f" - {subtype.replace('_', ' ').title()}"
        definition = subtype_info.get('definicao', info.get('definicao', ''))
    else:
        definition = info.get('definicao', '')
    
    st.markdown(f"### ✅ {title}")
    st.markdown(f"**Definição:** {definition}")
    
    severity = info.get('gravidade')
    if severity:
        st.markdown(f"**Gravidade:** {SEVERITY_LEVEL.get(severity, '')}")
        
    contacts = info.get("canais_denuncia", [])
    if contacts:
        st.markdown("**Canais de denúncia:**")
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