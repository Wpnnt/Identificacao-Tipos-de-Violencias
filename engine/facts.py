from experta import Fact, Field
from knowledge_base.violence_types import VIOLENCE_TYPES, SEVERITY_LEVEL, REPORT_CONTACT
import streamlit as st

"""Depois separar em um arquivo para cada classe"""

class ViolenceRelact(Fact):
    """
    Representa o relato que o usuário fez sobre a violência.
    Cada campo corresponde a uma informação coletada no formulário.
    """
    action_type = Field(str, mandatory=True)  # Tipo de comportamento/ação
    frequency = Field(str)  # Frequência da ocorrência
    context = Field(str)  # Contexto onde ocorreu
    target = Field(str)  # Característica(s) da vítima
    relationship = Field(str)  # Relação entre agressor e vítima
    impact = Field(str)  # Impacto na vítima

    # Metadados para pontuação e classificação
    weight = Field(int, default=0)  # Peso atribuído a este relato
    confidence = Field(float, default=0.0)  # Nível de confiança (0.0 a 1.0)

class ViolenceClassification(Fact):
    """
    Representa o resultado da classificação de uma violência.
    Será criado pelo motor de inferência ao identificar um tipo de violência.
    """
    violence_type = Field(str, mandatory=True)  # Tipo principal de violência
    subtype = Field(str, default=None)  # Subtipo (se aplicável)
    confidence_level = Field(float, default=0.0)  # Nível de confiança na classificação (0-1)
    score = Field(int, default=0)  # Pontuação acumulada
    explanation = Field(list, default=[])  # Lista de explicações sobre a classificação

class AnalysisResult(Fact):
    """
    Armazena o resultado final da análise com todos os tipos de violência 
    identificados e suas pontuações
    """
    classifications = Field(list, default=[])  # Lista de ViolenceClassifications
    primary_result = Field(str, default=None)  # Resultado principal (maior pontuação)
    multiple_types = Field(bool, default=False)  # Indica se foram encontrados múltiplos tipos
    ambiguity_level = Field(float, default=0.0)  # Nível de ambiguidade na classificação

def calculate_confidence(score, threshold, max_possible_score):
    """
    Calcula o nível de confiança de uma classificação baseado em um sistema de pontuação.
    
    Esta função implementa uma escala de confiança de 0% a 100% dividida em duas faixas:
    - 0% a 50%: Para pontuações abaixo do limiar mínimo
    - 50% a 100%: Para pontuações acima do limiar mínimo
    
    Parâmetros:
    -----------
    score : int
        Pontuação total acumulada pelo relato baseada no sistema de pesos.
        Exemplo: Comportamento (10 pontos) + Frequência (8 pontos) = 18 pontos
        
    threshold : int
        Limiar mínimo de pontos necessários para considerar que o tipo de violência
        foi identificado. Definido no sistema de pesos para cada tipo/subtipo.
        Exemplo: Microagressão-Interrupções = 15 pontos, Perseguição = 20 pontos
        
    max_possible_score : int
        Pontuação máxima teórica que o tipo de violência poderia atingir se todos
        os critérios fossem atendidos, incluindo fatores agravantes.
        Exemplo: Critérios obrigatórios + indicativos + complementares + agravantes
    
    Retorna:
    --------
    float
        Nível de confiança entre 0.0 e 1.0 (0% a 100%)
    
    Lógica de Cálculo:
    ------------------
    FAIXA 1 - Abaixo do Limiar (0% a 50%):
    Se a pontuação não atingiu o mínimo necessário, a confiança é proporcional
    ao progresso em direção ao limiar.
    Fórmula: (pontuação_atual / limiar_mínimo) × 0.5
    
    Exemplo: Limiar = 15, Pontuação = 10
    Confiança = (10/15) × 0.5 = 0.33 (33%)
    
    FAIXA 2 - Acima do Limiar (50% a 100%):
    A confiança base é 50% (por ter atingido o mínimo), mais uma confiança
    adicional proporcional ao quanto excede o limiar em relação ao máximo possível.
    
    Fórmula: 0.5 + ((pontos_excedentes / máximo_excedente_possível) × 0.5)
    
    Exemplo: Limiar = 15, Pontuação = 22, Máximo = 35
    - Pontos excedentes = 22 - 15 = 7
    - Máximo excedente = 35 - 15 = 20
    - Confiança adicional = (7/20) × 0.5 = 0.175
    - Confiança total = 0.5 + 0.175 = 0.675 (67.5%)
    
    Interpretação dos Resultados:
    -----------------------------
    0% - 25%:   Evidências muito fracas, classificação duvidosa
    25% - 50%:  Algumas evidências, mas insuficientes para confirmação
    50% - 60%:  Evidências mínimas suficientes, baixa confiança
    60% - 75%:  Evidências sólidas, confiança moderada
    75% - 90%:  Evidências fortes, alta confiança
    90% - 100%: Evidências muito fortes, quase todas as características presentes
    
    Esta abordagem permite:
    - Graduação suave ao invés de classificação binária (sim/não)
    - Transparência sobre a qualidade da identificação
    - Identificação de casos limítrofes que podem precisar análise adicional
    - Explicação clara de por que o sistema chegou a determinada conclusão
    """
    if score < threshold:
        # Abaixo do limiar, confiança proporcional ao progresso até o limiar
        return round((score / threshold) * 0.5, 2)
    else:
        # Acima do limiar, confiança entre 0.5 e 1.0 baseada no quanto excede o limiar
        base_confidence = 0.5
        remaining_confidence = 0.5  # 0.5 para atingir 1.0 total
        
        # Quanto acima do limiar está a pontuação?
        points_above_threshold = score - threshold
        max_points_above_threshold = max_possible_score - threshold
        
        # Calcular confiança adicional proporcional
        if max_points_above_threshold > 0:
            additional_confidence = (points_above_threshold / max_points_above_threshold) * remaining_confidence
            return round(base_confidence + additional_confidence, 2)
        return base_confidence

def print_information(violence_type, subtype=None, confidence=None):
    """
    Apresenta informações sobre um tipo de violência identificado.
    Versão aprimorada que suporta subtipos e mostra nível de confiança.
    """
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

    # Mostra título com indicador de confiança se disponível
    if confidence is not None:
        confidence_percent = int(confidence * 100)
        confidence_color = "green" if confidence_percent > 75 else "orange" if confidence_percent > 50 else "red"
        st.markdown(f"### ✅ {title} <span style='color:{confidence_color}'>[Confiança: {confidence_percent}%]</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"### ✅ {title}")
    
    st.markdown(f"**Definição:** {definition}")

    # Exibe gravidade
    severity = info.get('gravidade')
    if severity:
        st.markdown(f"**Gravidade:** {SEVERITY_LEVEL.get(severity, '')}")

    # Exibe canais de denúncia
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

    # Exibe recomendações
    recommendations = info.get("recomendacoes", [])
    if recommendations:
        st.markdown("**Recomendações:**")
        for r in recommendations:
            st.markdown(f"- {r}")










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