from knowledge_base.violence_types import VIOLENCE_TYPES, CRITERION_WEIGHTS
from typing import Dict, List
from knowledge_base.violence_types import CRITERION_WEIGHTS
from typing import Dict, List

CONCEPT_MAPPING = {
    "comportamentos": {
        "interrupcao": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "questionamento_capacidade": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["behavior"]["critical"]},
            "discriminacao_genero": {"discriminacao_sutil": CRITERION_WEIGHTS["behavior"]["relevant"]}
        },
        "comentarios_saude_mental": {
            "microagressoes": {"comentarios_saude_mental": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "piadas_estereotipos": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "perseguicao": {
            "perseguicao": CRITERION_WEIGHTS["behavior"]["critical"]
        },
        "vigilancia": {
            "perseguicao": CRITERION_WEIGHTS["behavior"]["critical"]
        },
        "exclusao": {
            "discriminacao_genero": {
                "discriminacao_flagrante": CRITERION_WEIGHTS["behavior"]["critical"],
                "discriminacao_sutil": CRITERION_WEIGHTS["behavior"]["relevant"]
            }
        },
        "ameaca": {
            "abuso_psicologico": CRITERION_WEIGHTS["behavior"]["critical"],
            "perseguicao": CRITERION_WEIGHTS["behavior"]["relevant"]
        },
        "constrangimento": {
            "abuso_psicologico": CRITERION_WEIGHTS["behavior"]["critical"]
        },
        "humilhacao": {
            "abuso_psicologico": CRITERION_WEIGHTS["behavior"]["critical"],
            "assedio_moral_genero": CRITERION_WEIGHTS["behavior"]["relevant"]
        },
        "pressao_tarefas": {
            "assedio_moral_genero": CRITERION_WEIGHTS["behavior"]["critical"]
        },
        "natureza_sexual_nao_consentido": {
            "violencia_sexual": {"assedio_sexual": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "contato_fisico_nao_consentido": {
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "ato_obsceno": {
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "coercao_sexual": {
            "violencia_sexual": {"estupro": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "comentarios_sobre_peso": {
            "gordofobia": {"discriminacao_direta": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "piadas_sobre_peso": {
            "gordofobia": {"discriminacao_direta": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "exclusao_por_peso": {
            "gordofobia": {"discriminacao_estrutural": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "negacao_acessibilidade": {
            "capacitismo": {"barreiras_fisicas": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "infantilizacao": {
            "capacitismo": {"barreiras_atitudinais": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "cyberbullying": {
            "violencia_digital": {"cyberbullying": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "mensagens_ofensivas": {
            "violencia_digital": {"cyberbullying": CRITERION_WEIGHTS["behavior"]["relevant"]}
        },
        "exposicao_conteudo": {
            "violencia_digital": {"exposicao_nao_consentida": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "zombaria_religiao": {
            "discriminacao_religiosa": {"ofensa_direta": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "impedimento_pratica_religiosa": {
            "discriminacao_religiosa": {"discriminacao_institucional": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "discriminacao_origem": {
            "xenofobia": {"xenofobia_internacional": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "piada_sotaque": {
            "xenofobia": {"discriminacao_regional": CRITERION_WEIGHTS["behavior"]["critical"]}
        }
    },
    "frequencia": {
        "unica_vez": {
            "violencia_sexual": {
                "estupro": CRITERION_WEIGHTS["frequency"]["single"], 
                "importunacao_sexual": CRITERION_WEIGHTS["frequency"]["single"],
                "assedio_sexual": CRITERION_WEIGHTS["frequency"]["single"]
            },
            "discriminacao_genero": {"discriminacao_flagrante": CRITERION_WEIGHTS["frequency"]["single"]}
        },
        "algumas_vezes": {
            "microagressoes": {
                "interrupcoes_constantes": CRITERION_WEIGHTS["frequency"]["few"],
                "estereotipos": CRITERION_WEIGHTS["frequency"]["few"],
                "comentarios_saude_mental": CRITERION_WEIGHTS["frequency"]["few"]
            },
            "violencia_sexual": {"assedio_sexual": CRITERION_WEIGHTS["frequency"]["few"]}
        },
        "repetidamente": {
            "microagressoes": {
                "interrupcoes_constantes": CRITERION_WEIGHTS["frequency"]["repeated"],
                "questionar_julgamento": CRITERION_WEIGHTS["frequency"]["repeated"],
                "estereotipos": CRITERION_WEIGHTS["frequency"]["repeated"]
            },
            "perseguicao": CRITERION_WEIGHTS["frequency"]["repeated"],
            "discriminacao_genero": {"discriminacao_sutil": CRITERION_WEIGHTS["frequency"]["repeated"]},
            "abuso_psicologico": CRITERION_WEIGHTS["frequency"]["repeated"],
            "violencia_digital": {"cyberbullying": CRITERION_WEIGHTS["frequency"]["repeated"]}
        },
        "continuamente": {
            "microagressoes": {
                "interrupcoes_constantes": CRITERION_WEIGHTS["frequency"]["continuous"],
                "questionar_julgamento": CRITERION_WEIGHTS["frequency"]["continuous"]
            },
            "perseguicao": CRITERION_WEIGHTS["frequency"]["continuous"],
            "discriminacao_genero": {"discriminacao_sutil": CRITERION_WEIGHTS["frequency"]["continuous"]},
            "abuso_psicologico": CRITERION_WEIGHTS["frequency"]["continuous"],
            "assedio_moral_genero": CRITERION_WEIGHTS["frequency"]["continuous"],
            "xenofobia": {"discriminacao_regional": CRITERION_WEIGHTS["frequency"]["continuous"]}
        }
    },
    "contexto": {
        "sala_aula": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["context"]["relevant"]},
            "capacitismo": {"barreiras_fisicas": CRITERION_WEIGHTS["context"]["relevant"]}
        },
        "ambiente_administrativo": {
            "microagressoes": {
                "interrupcoes_constantes": CRITERION_WEIGHTS["context"]["relevant"],
                "questionar_julgamento": CRITERION_WEIGHTS["context"]["relevant"]
            }
        },
        "local_trabalho": {
            "assedio_moral_genero": CRITERION_WEIGHTS["context"]["critical"],
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["context"]["relevant"]}
        },
        "espaco_publico_campus": {
            "perseguicao": CRITERION_WEIGHTS["context"]["supporting"],
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["context"]["relevant"]},
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["context"]["supporting"]}
        },
        "ambiente_online": {
            "perseguicao": CRITERION_WEIGHTS["context"]["supporting"],
            "violencia_digital": {
                "cyberbullying": CRITERION_WEIGHTS["context"]["critical"],
                "exposicao_nao_consentida": CRITERION_WEIGHTS["context"]["critical"]
            }
        },
        "redes_sociais": {
            "violencia_digital": {
                "cyberbullying": CRITERION_WEIGHTS["context"]["critical"],
                "exposicao_nao_consentida": CRITERION_WEIGHTS["context"]["critical"]
            }
        },
        "evento_academico": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["context"]["relevant"]},
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["context"]["supporting"]}
        },
        "ambiente_social": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["context"]["relevant"]},
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["context"]["supporting"]},
            "gordofobia": {"discriminacao_direta": CRITERION_WEIGHTS["context"]["relevant"]}
        },
        "local_culto_religioso": {
            "discriminacao_religiosa": {
                "ofensa_direta": CRITERION_WEIGHTS["context"]["critical"],
                "discriminacao_institucional": CRITERION_WEIGHTS["context"]["critical"]
            }
        }
    },
    "caracteristicas_alvo": {
        "genero": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["target"]["relevant"]},
            "discriminacao_genero": {
                "discriminacao_flagrante": CRITERION_WEIGHTS["target"]["critical"],
                "discriminacao_sutil": CRITERION_WEIGHTS["target"]["critical"]
            },
            "assedio_moral_genero": CRITERION_WEIGHTS["target"]["critical"]
        },
        "orientacao_sexual": {
            "discriminacao_genero": {
                "discriminacao_flagrante": CRITERION_WEIGHTS["target"]["critical"],
                "discriminacao_sutil": CRITERION_WEIGHTS["target"]["critical"]
            }
        },
        "raca_etnia": {
            "microagressoes": {
                "interrupcoes_constantes": CRITERION_WEIGHTS["target"]["relevant"],
                "estereotipos": CRITERION_WEIGHTS["target"]["relevant"]
            }
        },
        "condicao_financeira": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["target"]["supporting"]}
        },
        "deficiencia": {
            "microagressoes": {
                "interrupcoes_constantes": CRITERION_WEIGHTS["target"]["relevant"],
                "estereotipos": CRITERION_WEIGHTS["target"]["relevant"]
            },
            "capacitismo": {
                "barreiras_fisicas": CRITERION_WEIGHTS["target"]["critical"],
                "barreiras_atitudinais": CRITERION_WEIGHTS["target"]["critical"]
            }
        },
        "aparencia_fisica": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["target"]["supporting"]},
            "gordofobia": {"discriminacao_direta": CRITERION_WEIGHTS["target"]["critical"]}
        },
        "peso_corporal": {
            "gordofobia": {
                "discriminacao_direta": CRITERION_WEIGHTS["target"]["critical"],
                "discriminacao_estrutural": CRITERION_WEIGHTS["target"]["critical"]
            }
        },
        "origem_regional": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["target"]["supporting"]},
            "xenofobia": {
                "discriminacao_regional": CRITERION_WEIGHTS["target"]["critical"],
                "xenofobia_internacional": CRITERION_WEIGHTS["target"]["relevant"]
            }
        },
        "origem_estrangeira": {
            "xenofobia": {"xenofobia_internacional": CRITERION_WEIGHTS["target"]["critical"]}
        },
        "desempenho_academico": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["target"]["supporting"]}
        },
        "religiao": {
            "discriminacao_religiosa": {
                "ofensa_direta": CRITERION_WEIGHTS["target"]["critical"],
                "discriminacao_institucional": CRITERION_WEIGHTS["target"]["critical"]
            }
        }
    },
    "relacionamento": {
        "superior_hierarquico": {
            "abuso_psicologico": CRITERION_WEIGHTS["relationship"]["hierarchical"],
            "assedio_moral_genero": CRITERION_WEIGHTS["relationship"]["hierarchical"]
        },
        "colega": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["relationship"]["peer"]}
        },
        "subordinado": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["relationship"]["peer"]}
        },
        "desconhecido": {
            "perseguicao": CRITERION_WEIGHTS["relationship"]["unknown"],
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["relationship"]["unknown"]}
        },
        "ex_relacionamento": {
            "perseguicao": CRITERION_WEIGHTS["relationship"]["ex_partner"]
        }
    },
    "impacto": {
        "constrangimento": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["impact"]["mild"]},
            "violencia_sexual": {
                "assedio_sexual": CRITERION_WEIGHTS["impact"]["moderate"],
                "importunacao_sexual": CRITERION_WEIGHTS["impact"]["moderate"]
            },
            "discriminacao_religiosa": {"ofensa_direta": CRITERION_WEIGHTS["impact"]["moderate"]}
        },
        "impacto_participacao": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["impact"]["moderate"]},
            "gordofobia": {"discriminacao_estrutural": CRITERION_WEIGHTS["impact"]["strong"]}
        },
        "danos_emocionais": {
            "microagressoes": {"comentarios_saude_mental": CRITERION_WEIGHTS["impact"]["strong"]},
            "abuso_psicologico": CRITERION_WEIGHTS["impact"]["critical"],
            "assedio_moral_genero": CRITERION_WEIGHTS["impact"]["strong"],
            "violencia_sexual": {"estupro": CRITERION_WEIGHTS["impact"]["critical"]},
            "violencia_digital": {"exposicao_nao_consentida": CRITERION_WEIGHTS["impact"]["critical"]}
        },
        "limitacao_liberdade": {
            "perseguicao": CRITERION_WEIGHTS["impact"]["strong"],
            "capacitismo": {"barreiras_fisicas": CRITERION_WEIGHTS["impact"]["critical"]}
        },
        "prejuizo_desempenho": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["impact"]["moderate"]},
            "discriminacao_genero": {
                "discriminacao_sutil": CRITERION_WEIGHTS["impact"]["strong"],
                "discriminacao_flagrante": CRITERION_WEIGHTS["impact"]["strong"]
            },
            "assedio_moral_genero": CRITERION_WEIGHTS["impact"]["strong"]
        },
        "medo_inseguranca": {
            "perseguicao": CRITERION_WEIGHTS["impact"]["strong"],
            "violencia_sexual": {
                "importunacao_sexual": CRITERION_WEIGHTS["impact"]["strong"],
                "estupro": CRITERION_WEIGHTS["impact"]["critical"]
            },
            "xenofobia": {"xenofobia_internacional": CRITERION_WEIGHTS["impact"]["strong"]}
        },
        "violacao_privacidade": {
            "violencia_sexual": {
                "assedio_sexual": CRITERION_WEIGHTS["impact"]["strong"],
                "importunacao_sexual": CRITERION_WEIGHTS["impact"]["strong"],
                "estupro": CRITERION_WEIGHTS["impact"]["critical"]
            },
            "violencia_digital": {"exposicao_nao_consentida": CRITERION_WEIGHTS["impact"]["critical"]}
        },
        "exposicao_indesejada": {
            "violencia_digital": {"exposicao_nao_consentida": CRITERION_WEIGHTS["impact"]["critical"]}
        },
        "limitacao_acesso": {
            "capacitismo": {"barreiras_fisicas": CRITERION_WEIGHTS["impact"]["critical"]}
        },
        "discriminacao_identidade": {
            "discriminacao_religiosa": {"ofensa_direta": CRITERION_WEIGHTS["impact"]["strong"]},
            "xenofobia": {"xenofobia_internacional": CRITERION_WEIGHTS["impact"]["strong"]}
        }
    }
}

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
    Versão simplificada que adiciona apenas as variações mais essenciais.
    """
    expanded = {category: list(words) for category, words in keywords.items()}
    
    # Dicionário SIMPLIFICADO de variações por palavra-chave
    variations = {
        # Action type - APENAS variações principais
        "interrupcao": ["interromper", "cortar fala"],
        "questionamento_capacidade": ["duvidar", "questionar capacidade"],
        "perseguicao": ["perseguir", "stalking", "vigiar"],
        "ameaca": ["ameaçar", "intimidar"],
        "humilhacao": ["humilhar", "ridicularizar"],
        "comentarios_saude_mental": ["histérico", "emocional", "louco"],
        "piadas_estereotipos": ["piada ofensiva", "zoação"],
        "xingamento": ["xingar", "ofender", "insultar"],
        "ofensa": ["ofender", "insultar"],
        "insulto": ["xingar", "ofender"],
        "coercao_sexual": ["estupro", "forçar"],
        
        # Gordofobia - simplificado
        "comentarios_sobre_peso": ["gordofobia", "gordo", "peso"],
        
        # Discriminação racial - adicionado
        "insulto_racial": ["racismo", "macaco", "racial", "negro"],
        
        # Frequency - simplificado
        "repetidamente": ["várias vezes", "frequentemente"],
        "continuamente": ["sempre", "constantemente"],
        
        # Target - simplificado
        "raca_etnia": ["negro", "preto", "cor da pele", "raça"],
        "genero": ["mulher", "homem", "feminino"],
        
        # Context - simplificado
        "espaco_publico_campus": ["campus", "rua", "público"],
        
        # Impact - simplificado
        "medo_inseguranca": ["medo", "insegurança"]
    }
    
    # Aplicar apenas as variações principais
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