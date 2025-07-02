from knowledge_base.violence_types import VIOLENCE_TYPES
from knowledge_base.confidence_levels import CONCEPT_MAPPING
from typing import Dict, List

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

def extract_keywords_from_concept_mapping():
    """
    Extrai palavras-chave do CONCEPT_MAPPING.
    """
    keywords = {
        "action_type": [],
        "frequency": [],
        "context": [],
        "target": [],
        "relationship": [],
        "impact": []
    }
    
    # Mapeamento entre categorias de conceito e campos de formulário
    concept_to_field = {
        "comportamentos": "action_type",
        "frequencia": "frequency",
        "contexto": "context",
        "caracteristicas_alvo": "target",
        "relacionamento": "relationship",
        "impacto": "impact"
    }
    
    # Extrair chaves como palavras-chave
    for concept, mappings in CONCEPT_MAPPING.items():
        field = concept_to_field.get(concept)
        if field and field in keywords:
            keywords[field].extend(mappings.keys())
    
    return keywords

def build_keywords_dictionary():
    """
    Constrói o dicionário completo de palavras-chave combinando todas as fontes.
    """
    # Palavras-chave das definições de tipos de violência
    vt_keywords = extract_keywords_from_violence_types()
    
    # Palavras-chave do mapeamento de conceitos
    concept_keywords = extract_keywords_from_concept_mapping()
    
    # Combinar todos os dicionários
    combined = {}
    for category in set(list(vt_keywords.keys()) + list(concept_keywords.keys())):
        combined[category] = []
        if category in vt_keywords:
            combined[category].extend(vt_keywords[category])
        if category in concept_keywords:
            combined[category].extend(concept_keywords[category])
        
        # Remover duplicatas e ordenar
        combined[category] = sorted(list(set(combined[category])))
    
    # Ajustes finais
    if "behavior" in combined:
        combined["action_type"].extend(combined.pop("behavior"))
        combined["action_type"] = sorted(list(set(combined["action_type"])))
    
    # Expandir com variações comuns
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

def expand_keywords_with_variations(keywords: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Expande o dicionário de palavras-chave incluindo variações comuns.
    """
    expanded = {category: list(words) for category, words in keywords.items()}
    
    # Dicionário de variações comuns por palavra-chave
    variations = {
        # Action type variations
        "interrupcao": ["interromper", "cortar a fala", "silenciar", "não deixar falar"],
        "questionamento_capacidade": ["duvidar", "contestar", "questionar capacidade", "desmerecer opinião"],
        "perseguicao": ["perseguir", "seguir", "stalking", "monitoramento", "observação constante", "vigiar"],
        "vigilancia": ["vigiar", "monitorar", "observar constantemente"],
        "ameaca": ["ameaçar", "intimidar", "coagir"],
        "constrangimento": ["constranger", "causar vergonha", "embaraçar"],
        "humilhacao": ["humilhar", "ridicularizar", "rebaixar", "insultar"],
        "comentarios_saude_mental": ["histérico", "emocional", "sensível", "exagerado", "louco", "desequilibrado"],
        "piadas_estereotipos": ["piadas ofensivas", "estereótipos", "comentários preconceituosos", "zoação"],
        "coercao_sexual": ["estupro", "abuso", "forçar", "contra vontade", "sexualmente"],

        # NOVAS CATEGORIAS - Adicionadas
        # Gordofobia
        "comentarios_sobre_peso": ["gordofobia", "gordo", "gorda", "peso", "corpo grande", "comentário sobre peso"],
        "piadas_sobre_peso": ["piada sobre gordo", "zoar peso", "gordura", "obeso"],
        "exclusao_por_peso": ["exclusão por aparência", "discriminação por peso", "tamanho corporal"],
        
        # Capacitismo
        "negacao_acessibilidade": ["rampa", "elevador", "sinalização", "acessibilidade", "barreira física"],
        "infantilizacao": ["tratar como criança", "incapaz", "superproteção", "infantilizar"],
        
        # Violência Digital
        "cyberbullying": ["assédio online", "perseguição virtual", "intimidação online"],
        "mensagens_ofensivas": ["insultos online", "ameaças digitais", "ofensas virtuais"],
        "exposicao_conteudo": ["vazamento", "nudes", "fotos íntimas", "exposição online", "compartilhar sem permissão"],
        
        # Discriminação Religiosa
        "zombaria_religiao": ["preconceito religioso", "fé", "crença", "zombar de religião"],
        "impedimento_pratica_religiosa": ["proibir prática", "impedir ritual", "negar vestimenta religiosa"],
        
        # Xenofobia
        "discriminacao_origem": ["xenofobia", "estrangeiro", "imigrante", "nacionalidade"],
        "piada_sotaque": ["sotaque", "jeito de falar", "nordestino", "nortista", "caipira", "sotaque regional"],

        # Frequency variations
        "unica_vez": ["uma única vez", "uma vez só", "caso isolado"],
        "algumas_vezes": ["poucas vezes", "algumas ocasiões", "eventualmente"],
        "repetidamente": ["repetidas vezes", "várias vezes", "frequentemente"],
        "continuamente": ["sempre", "todo dia", "constantemente", "sem parar"],
        
        # Context variations
        "sala_aula": ["sala de aula", "durante aula", "na aula", "em classe"],
        "ambiente_administrativo": ["administração", "secretaria", "departamento"],
        "local_trabalho": ["trabalho", "empresa", "escritório", "estágio"],
        "espaco_publico_campus": ["campus", "universidade", "faculdade", "área pública"],
        "ambiente_online": ["online", "internet", "rede social", "plataforma digital"],
        "redes_sociais": ["facebook", "instagram", "twitter", "whatsapp", "grupo online"],
        "evento_academico": ["palestra", "congresso", "simpósio", "seminário"],
        "ambiente_social": ["festa", "confraternização", "evento social"],
        "local_culto_religioso": ["igreja", "templo", "centro religioso", "culto"],
        
        # Relationship variations
        "superior_hierarquico": ["chefe", "professor", "supervisor", "gerente", "diretor"],
        "colega": ["colega de classe", "colega de trabalho", "par"],
        "subordinado": ["funcionário", "supervisionado", "orientando"],
        "desconhecido": ["estranho", "pessoa desconhecida", "não conheço", "nunca vi"],
        "ex_relacionamento": ["ex-parceiro", "ex-namorado", "ex-cônjuge"],
        
        # Target variations
        "genero": ["mulher", "homem", "feminino", "masculino", "identidade de gênero"],
        "orientacao_sexual": ["gay", "lésbica", "bissexual", "homossexual", "orientação sexual"],
        "raca_etnia": ["negro", "preto", "branco", "indígena", "asiático", "raça", "cor da pele"],
        "deficiencia": ["deficiente", "cadeirante", "cego", "surdo", "neurodivergente"],
        "aparencia_fisica": ["bonito", "feio", "alto", "baixo", "aparência"],
        
        # Impact variations
        "constrangimento": ["vergonha", "desconforto", "embaraço", "constrangido"],
        "impacto_participacao": ["deixar de participar", "reduzir participação", "evitar interação"],
        "danos_emocionais": ["trauma", "estresse", "ansiedade", "depressão", "sofrimento psíquico"],
        "limitacao_liberdade": ["restringir movimentos", "impedir locomoção", "monitorar passos"],
        "prejuizo_desempenho": ["notas baixas", "avaliação negativa", "prejuízo acadêmico"],
        "medo_inseguranca": ["inseguro", "medo", "receio", "insegurança", "apreensão"],
        "violacao_privacidade": ["invasão", "expor intimidade", "violar privacidade"],
        "exposicao_indesejada": ["exposição pública", "exposição não consentida"],
        "limitacao_acesso": ["barreira", "impedir acesso", "dificultar participação"],
        "discriminacao_identidade": ["discriminar", "preconceito", "negar identidade"]
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

# Construir e exportar o dicionário de palavras-chave
KEYWORDS_DICT = build_keywords_dictionary()