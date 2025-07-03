from experta import Fact, Field  # ✅ CORREÇÃO PRINCIPAL: importar do experta diretamente
from knowledge_base.violence_types import VIOLENCE_TYPES, SEVERITY_LEVEL, REPORT_CONTACT
from knowledge_base.confidence_levels import *
import streamlit as st  # type: ignore

# Definição dos fatos usando Field para declarar os atributos
class TextRelato(Fact):
    text = Field(str, default=None)
    processed = Field(bool, default=False)

class KeywordFact(Fact):
    category = Field(str, default=None)
    keyword = Field(str, default=None)
    confidence = Field(float, default=1.0)

class ViolenceBehavior(Fact):
    behavior_type = Field(str, default=None)

class ContextFact(Fact):
    location = Field(str, default=None)

class FrequencyFact(Fact):
    value = Field(str, default=None)

class TargetFact(Fact):
    characteristic = Field(str, default=None)

class RelationshipFact(Fact):
    type = Field(str, default=None)

class ImpactFact(Fact):
    type = Field(str, default=None)

class ViolenceRelact(Fact):
    action_type = Field(str, default=None)
    frequency = Field(str, default=None)
    context = Field(str, default=None)
    target = Field(str, default=None)
    relationship = Field(str, default=None)
    impact = Field(str, default=None)
    weight = Field(int, default=0)
    confidence = Field(float, default=0.0)

class ViolenceClassification(Fact):
    violence_type = Field(str, default=None)
    subtype = Field(str, default=None)
    confidence_level = Field(float, default=0.0)
    score = Field(int, default=0)
    explanation = Field(list, default=[])

class AnalysisResult(Fact):
    classifications = Field(list, default=[])
    primary_result = Field(object, default=None)
    multiple_types = Field(bool, default=False)
    ambiguity_level = Field(float, default=0.0)


# Funções auxiliares (mantidas)
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

def calculate_confidence(score, threshold, max_possible_score):
    if score < threshold:
        return round((score / threshold) * 0.5, 2)
    else:
        base_confidence = 0.5
        remaining_confidence = 0.5
        points_above_threshold = score - threshold
        max_points_above_threshold = max_possible_score - threshold
        if max_points_above_threshold > 0:
            additional_confidence = (points_above_threshold / max_points_above_threshold) * remaining_confidence
            return round(base_confidence + additional_confidence, 2)
        return base_confidence

def get_threshold(violence_type, subtype=None):
    if subtype and violence_type in CLASSIFICATION_THRESHOLDS:
        subtipo_dict = CLASSIFICATION_THRESHOLDS.get(violence_type)
        if isinstance(subtipo_dict, dict):
            return subtipo_dict.get(subtype, 0)
    valor = CLASSIFICATION_THRESHOLDS.get(violence_type)
    return valor if isinstance(valor, int) else 0

def get_max_score(violence_type, subtype=None):
    if subtype and violence_type in MAX_POSSIBLE_SCORES:
        subtipo_dict = MAX_POSSIBLE_SCORES.get(violence_type)
        if isinstance(subtipo_dict, dict):
            return subtipo_dict.get(subtype, 0)
    valor = MAX_POSSIBLE_SCORES.get(violence_type)
    return valor if isinstance(valor, int) else 0

def should_report_multiple(classifications):
    if len(classifications) <= 1:
        return False, 0.0
    sorted_classifications = sorted(
        classifications, 
        key=lambda x: x.get('score', 0), 
        reverse=True
    )
    primary = sorted_classifications[0]
    secondary = sorted_classifications[1]
    primary_score = primary.get('score', 0)
    secondary_score = secondary.get('score', 0)
    if primary_score == 0:
        return False, 0.0
    ambiguity = secondary_score / primary_score if primary_score > 0 else 0
    should_report = ambiguity >= 0.8
    return should_report, ambiguity

def resolve_ambiguity(classifications):
    if not classifications:
        return None
    return sorted(
        classifications, 
        key=lambda x: (x.get('score', 0), x.get('confidence', 0)), 
        reverse=True
    )[0]

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
    if confidence is not None:
        confidence_percent = int(confidence * 100)
        confidence_color = "green" if confidence_percent > 75 else "orange" if confidence_percent > 50 else "red"
        st.markdown(f"### ✅ {title} <span style='color:{confidence_color}'>[Confiança: {confidence_percent}%]</span>", unsafe_allow_html=True)
    else:
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
