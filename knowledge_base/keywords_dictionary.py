from knowledge_base.violence_types import VIOLENCE_TYPES
from knowledge_base.confidence_levels import FORM_OPTION_MAPPING
from typing import Dict, List

def expand_keywords_with_variations(keywords: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Expande o dicionário de palavras-chave incluindo variações comuns.
    """
    expanded = {category: list(words) for category, words in keywords.items()}
    
    # Dicionário de variações comuns por palavra-chave
    variations = {
        # Action type variations
        "Perseguição ou vigilância constante": ["perseguir", "seguir", "stalking", "monitoramento", "observação constante"],
        "Ameaças, constrangimentos ou humilhações": ["ameaçar", "constranger", "humilhar", "intimidar"],
        "Interrupções durante fala ou participação": ["interromper", "cortar a fala", "silenciar"],
        "Piadas ou comentários sobre estereótipos": ["piadas ofensivas", "estereótipos", "comentários preconceituosos"],
        
        # Frequency variations
        "Repetidamente": ["repetidas vezes", "várias vezes", "frequentemente", "constantemente"],
        
        # Context variations
        "Espaço público no campus": ["campus", "universidade", "faculdade", "área pública"],
        "Local de trabalho/estágio": ["trabalho", "empresa", "escritório", "estágio"],
        
        # Relationship variations
        "Desconhecido": ["estranho", "pessoa desconhecida", "não conheço"],
        "Superior hierárquico": ["chefe", "supervisor", "gerente", "diretor"],
        
        # Impact variations
        "Medo ou sentimento de insegurança": ["inseguro", "medo", "receio", "insegurança"],
        "Danos emocionais ou psicológicos": ["trauma", "estresse", "ansiedade", "depressão"]
    }
    
    # Aplicar as variações ao dicionário
    for category, words in expanded.items():
        new_words = []
        for word in words:
            if word in variations:
                new_words.extend(variations[word])
        expanded[category].extend(new_words)
        # Remover duplicatas e ordenar
        expanded[category] = sorted(list(set(expanded[category])))
    
    return expanded

def extract_keywords_from_violence_types():
    """
    Extrai palavras-chave do dicionário VIOLENCE_TYPES.
    """
    keywords = {
        "action_type": [],
        "behavior": []  # Para comportamentos específicos
    }
    
    # Extrair palavras-chave de cada tipo de violência
    for vtype, vdata in VIOLENCE_TYPES.items():
        # Extrair do tipo principal
        if "palavras_chave" in vdata:
            keywords["action_type"].extend(vdata["palavras_chave"])
        
        # Extrair dos subtipos
        if "subtipos" in vdata:
            for subtype, subdata in vdata["subtipos"].items():
                if "palavras_chave" in subdata:
                    keywords["action_type"].extend(subdata["palavras_chave"])
                if "comportamentos" in subdata:
                    keywords["behavior"].extend(subdata["comportamentos"])
    
    return keywords

def extract_keywords_from_form_options():
    """
    Extrai palavras-chave das opções do formulário em FORM_OPTION_MAPPING.
    """
    keywords = {
        "action_type": [],
        "frequency": [],
        "context": [],
        "target": [],
        "relationship": [],
        "impact": []
    }
    
    # Extrair todas as opções como palavras-chave
    for category, options in FORM_OPTION_MAPPING.items():
        if category in keywords:
            keywords[category].extend(options.keys())
    
    return keywords

def build_keywords_dictionary():
    """
    Constrói o dicionário completo de palavras-chave combinando todas as fontes.
    """
    # Palavras-chave das definições de tipos de violência
    vt_keywords = extract_keywords_from_violence_types()
    
    # Palavras-chave das opções do formulário
    form_keywords = extract_keywords_from_form_options()
    
    # Combinar todos os dicionários
    combined = {}
    for category in set(list(vt_keywords.keys()) + list(form_keywords.keys())):
        combined[category] = []
        if category in vt_keywords:
            combined[category].extend(vt_keywords[category])
        if category in form_keywords:
            combined[category].extend(form_keywords[category])
        
        # Remover duplicatas e ordenar
        combined[category] = sorted(list(set(combined[category])))
    
    # Ajustes finais:
    # 1. Unificar action_type e behavior em uma categoria
    if "behavior" in combined:
        combined["action_type"].extend(combined.pop("behavior"))
        combined["action_type"] = sorted(list(set(combined["action_type"])))
    
    # 2. Expandir com variações comuns
    combined = expand_keywords_with_variations(combined)
    
    return combined

# Dicionário de perguntas para obter informações faltantes
FIELDS_QUESTIONS = {
    "action_type": "Poderia descrever o comportamento ou ação específica que ocorreu?",
    "frequency": "Com que frequência isso aconteceu? Foi uma única vez, algumas vezes, repetidamente ou continuamente?",
    "context": "Em qual ambiente ou local isso aconteceu?",
    "target": "Você acredita que a ação foi direcionada a alguma característica específica sua?",
    "relationship": "Qual é a sua relação com a pessoa que cometeu essa ação?",
    "impact": "Como isso te afetou? Quais foram os impactos deste comportamento para você?"
}

# Construir e exportar o dicionário de palavras-chave
KEYWORDS_DICT = build_keywords_dictionary()