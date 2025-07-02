from experta.fact import Fact, Field

from knowledge_base.violence_types import VIOLENCE_TYPES, SEVERITY_LEVEL, REPORT_CONTACT
from knowledge_base.confidence_levels import *
import streamlit as st # type: ignore

class Field:
    """Classe Field compatível com Experta."""
    def __init__(self, type_=None, mandatory=False, default=None):
        self.type = type_
        self.mandatory = mandatory
        self.default = default

class Fact:
    """Classe Fact compatível com Experta."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def __contains__(self, key):
        return hasattr(self, key)
    
    def get(self, key, default=None):
        return getattr(self, key, default)

# Importações necessárias
from knowledge_base.violence_types import VIOLENCE_TYPES, SEVERITY_LEVEL, REPORT_CONTACT
from knowledge_base.confidence_levels import *
import streamlit as st # type: ignore

"""Depois separar em um arquivo para cada classe"""

class TextRelato(Fact):
    """Representa o texto do relato original."""
    def __init__(self, text=None, processed=False, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.processed = processed

class KeywordFact(Fact):
    """Representa uma palavra-chave extraída do texto."""
    def __init__(self, category=None, keyword=None, confidence=1.0, **kwargs):
        super().__init__(**kwargs)
        self.category = category
        self.keyword = keyword
        self.confidence = confidence

class ViolenceBehavior(Fact):
    """Representa um comportamento violento identificado."""
    def __init__(self, behavior_type=None, **kwargs):
        super().__init__(**kwargs)
        self.behavior_type = behavior_type

class ContextFact(Fact):
    """Representa o contexto onde ocorreu a violência."""
    def __init__(self, location=None, **kwargs):
        super().__init__(**kwargs)
        self.location = location

class FrequencyFact(Fact):
    """Representa a frequência da violência."""
    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value

class TargetFact(Fact):
    """Representa características da vítima."""
    def __init__(self, characteristic=None, **kwargs):
        super().__init__(**kwargs)
        self.characteristic = characteristic

class RelationshipFact(Fact):
    """Representa o relacionamento entre agressor e vítima."""
    def __init__(self, type=None, **kwargs):
        super().__init__(**kwargs)
        self.type = type

class ImpactFact(Fact):
    """Representa o impacto na vítima."""
    def __init__(self, type=None, **kwargs):
        super().__init__(**kwargs)
        self.type = type

class ViolenceRelact(Fact):
    """Representa o relato que o usuário fez sobre a violência."""
    def __init__(self, action_type=None, frequency=None, context=None, 
                 target=None, relationship=None, impact=None, 
                 weight=0, confidence=0.0, **kwargs):
        super().__init__(**kwargs)
        self.action_type = action_type
        self.frequency = frequency
        self.context = context
        self.target = target
        self.relationship = relationship
        self.impact = impact
        self.weight = weight
        self.confidence = confidence

class ViolenceClassification(Fact):
    """Representa o resultado da classificação de uma violência."""
    def __init__(self, violence_type=None, subtype=None, confidence_level=0.0, 
                 score=0, explanation=None, **kwargs):
        super().__init__(**kwargs)
        self.violence_type = violence_type
        self.subtype = subtype
        self.confidence_level = confidence_level
        self.score = score
        self.explanation = explanation or []

class AnalysisResult(Fact):
    """Armazena o resultado final da análise com todos os tipos de violência identificados."""
    def __init__(self, classifications=None, primary_result=None, 
                 multiple_types=False, ambiguity_level=0.0, **kwargs):
        super().__init__(**kwargs)
        self.classifications = classifications or []
        self.primary_result = primary_result
        self.multiple_types = multiple_types
        self.ambiguity_level = ambiguity_level

def create_facts_from_groq_response(response):
    """
    Cria fatos estruturados a partir da resposta da API Groq.
    
    Args:
        response: Resposta da API com palavras-chave identificadas
        
    Returns:
        List: Lista de fatos para o motor de regras
    """
    facts = []
    
    if "identified_keywords" in response and response["identified_keywords"]:
        keywords = response["identified_keywords"]
        
        for category, values in keywords.items():
            for keyword in values:
                facts.append(KeywordFact(category=category, keyword=keyword))
                
                # Criar fatos específicos conforme a categoria
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
    """
    Calcula o nível de confiança de uma classificação baseado em um sistema de pontuação.
    """
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
    """Retorna o limiar mínimo de pontos para considerar a classificação válida."""
    if subtype and violence_type in CLASSIFICATION_THRESHOLDS:
        subtipo_dict = CLASSIFICATION_THRESHOLDS.get(violence_type)
        if isinstance(subtipo_dict, dict):
            return subtipo_dict.get(subtype, 0)
    
    valor = CLASSIFICATION_THRESHOLDS.get(violence_type)
    return valor if isinstance(valor, int) else 0

def get_max_score(violence_type, subtype=None):
    """Retorna a pontuação máxima teórica possível para um tipo de violência."""
    if subtype and violence_type in MAX_POSSIBLE_SCORES:
        subtipo_dict = MAX_POSSIBLE_SCORES.get(violence_type)
        if isinstance(subtipo_dict, dict):
            return subtipo_dict.get(subtype, 0)

    valor = MAX_POSSIBLE_SCORES.get(violence_type)
    return valor if isinstance(valor, int) else 0

def should_report_multiple(classifications):
    """Determina se múltiplos tipos devem ser reportados."""
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
    """Resolve ambiguidades e retorna o resultado principal."""
    if not classifications:
        return None
        
    return sorted(
        classifications, 
        key=lambda x: (x.get('score', 0), x.get('confidence', 0)), 
        reverse=True
    )[0]

def print_information(violence_type, subtype=None, confidence=None):
    """Exibe informações sobre um tipo de violência identificado."""
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