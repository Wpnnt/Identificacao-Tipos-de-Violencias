import os
import streamlit as st # type: ignore
from engine.expert_system import ExpertSystem
from knowledge_base.violence_types import VIOLENCE_TYPES

# Inicializar o sistema especialista
@st.cache_resource
def get_expert_system():
    if 'expert_system' not in st.session_state:
        api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
        st.session_state.expert_system = ExpertSystem(api_key=api_key)
    return st.session_state.expert_system

st.set_page_config(
    page_title="Sistema Especialista",
    page_icon=":robot:",
    layout="centered",
    initial_sidebar_state="collapsed"
)
st.title("Sistema Especialista de Identificação de Violência")

# Inicializar variáveis de estado da sessão
if 'state' not in st.session_state:
    st.session_state.state = 'initial'  # initial, follow_up, result
if 'keywords' not in st.session_state:
    st.session_state.keywords = {}
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'missing_fields' not in st.session_state:
    st.session_state.missing_fields = []
if 'partial_facts' not in st.session_state:
    st.session_state.partial_facts = {}
if 'results' not in st.session_state:
    st.session_state.results = []

expert_system = get_expert_system()

# Interface do usuário baseada no estado atual
if st.session_state.state == 'initial':
    st.subheader("Relate a situação ocorrida")
    
    user_text = st.text_area(
        "Descreva em detalhes o que aconteceu:",
        height=200,
        placeholder="Conte com suas palavras o que aconteceu, incluindo detalhes sobre o comportamento, local, frequência e como isso te afetou..."
    )
    
    if st.button("Analisar"):
        if len(user_text) < 20:
            st.error("Por favor, forneça um relato mais detalhado para análise.")
        else:
            with st.spinner("Analisando seu relato..."):
                # Usar o sistema especialista em vez do processador diretamente
                result = expert_system.analyze_text(user_text)
                
                # Atualizar a interface com os resultados
                st.session_state.results = result["classifications"]
                st.session_state.state = 'result'
                st.rerun()

elif st.session_state.state == 'follow_up':
    st.subheader("Precisamos de mais algumas informações")
    
    # Mostrar as palavras-chave já identificadas
    if st.session_state.keywords:
        st.write("Com base no seu relato, identificamos:")
        for category, keywords in st.session_state.keywords.items():
            if keywords:
                category_name = category.replace("_", " ").capitalize()
                st.write(f"- **{category_name}**: {', '.join(keywords)}")
    
    # Mostrar as perguntas complementares
    st.write("Para uma análise mais precisa, por favor responda:")
    for question in st.session_state.questions:
        st.write(f"- {question}")
    
    follow_up_text = st.text_area(
        "Sua resposta:",
        height=150,
        placeholder="Responda as perguntas acima para continuar a análise..."
    )
    
    if st.button("Continuar análise"):
        if follow_up_text:
            with st.spinner("Processando suas respostas..."):
                # Processar a resposta complementar através do sistema especialista
                combined_text = follow_up_text  # Você pode combinar com o texto original se necessário
                
                # Usar o sistema especialista para analisar o texto complementar
                result = expert_system.analyze_text(combined_text)
                
                # Atualizar a interface com os resultados
                st.session_state.results = result["classifications"]
                st.session_state.state = 'result'
                st.rerun()
        else:
            st.error("Por favor, responda às perguntas para continuar.")

elif st.session_state.state == 'result':
    st.subheader("Resultados da Análise")
    
    if not st.session_state.results:
        st.info("Nenhum tipo de violência foi identificado com base nas informações fornecidas.")
    else:
        st.success("Identificamos possíveis tipos de violência:")
        
        for r in st.session_state.results:
            # Obter informações mais detalhadas do tipo/subtipo
            vtype = r["violence_type"]
            subtype = r.get("subtype")
            
            # Determinar o título a ser exibido
            if subtype:
                subtype_formatted = subtype.replace("_", " ").capitalize()
                title = f"{subtype_formatted} ({vtype.replace('_', ' ').title()})"
            else:
                title = VIOLENCE_TYPES[vtype]['nome'] if 'nome' in VIOLENCE_TYPES[vtype] else vtype.replace('_', ' ').title()
            
            # Exibir resultado (sem mostrar confiança)
            with st.expander(f"{title}"):
                # Exibir descrição
                if subtype and "subtipos" in VIOLENCE_TYPES[vtype] and subtype in VIOLENCE_TYPES[vtype]["subtipos"]:
                    st.write(VIOLENCE_TYPES[vtype]["subtipos"][subtype]["definicao"])
                else:
                    st.write(VIOLENCE_TYPES[vtype]["definicao"])
                
                # Exibir explicações se disponíveis
                if "explanation" in r and r["explanation"]:
                    st.subheader("Por que identificamos este tipo:")
                    for exp in r["explanation"]:
                        st.write(f"- {exp}")
                
                # Exibir recomendações se disponíveis
                if "recomendacoes" in VIOLENCE_TYPES[vtype]:
                    st.subheader("Recomendações:")
                    for rec in VIOLENCE_TYPES[vtype]["recomendacoes"]:
                        st.write(f"- {rec}")
    
    # Opção para reiniciar
    if st.button("Iniciar Nova Análise"):
        # Resetar todos os estados
        for key in ['state', 'keywords', 'questions', 'missing_fields', 'partial_facts', 'results', 'expert_system']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.state = 'initial'
        st.rerun()