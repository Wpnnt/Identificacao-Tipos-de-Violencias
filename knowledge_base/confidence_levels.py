"""
Define os níveis de confiança, limiares e sistemas de pesos para classificação
de tipos de violência.
"""

from knowledge_base.violence_types import VIOLENCE_TYPES, SEVERITY_LEVEL

# Constantes para níveis de confiança que serão usados para relatar o grau de certeza
# da classificação ao usuário
CONFIDENCE_LEVELS = {
    "VERY_LOW": {"min": 0.00, "max": 0.25, "label": "Muito baixa", "description": "Evidências muito fracas, classificação duvidosa"},
    "LOW": {"min": 0.25, "max": 0.50, "label": "Baixa", "description": "Algumas evidências, mas insuficientes para confirmação"},
    "MODERATE": {"min": 0.50, "max": 0.75, "label": "Moderada", "description": "Evidências suficientes, confiança razoável"},
    "HIGH": {"min": 0.75, "max": 0.90, "label": "Alta", "description": "Evidências fortes, alta confiança na classificação"},
    "VERY_HIGH": {"min": 0.90, "max": 1.00, "label": "Muito alta", "description": "Evidências muito fortes, classificação certa"}
}

# Pesos para critérios de pontuação
# (para usar no cálculo de pontuação dentro de rules.py)
CRITERION_WEIGHTS = {
    # Pesos gerais agrupados por tipo de campo
    "behavior": {
        "critical": 10,    # Comportamento crítico/determinante
        "relevant": 7,     # Comportamento relevante
        "supporting": 4    # Comportamento suportivo
    },
    "frequency": {
        "single": 2,           # Uma única vez
        "few": 4,              # Algumas vezes
        "repeated": 6,         # Repetidamente
        "continuous": 8        # Continuamente
    },
    "context": {
        "critical": 10,    # Contexto determinante (ex: local de trabalho para assédio moral)
        "relevant": 5,     # Contexto relevante
        "supporting": 2    # Contexto menos relevante
    },
    "target": {
        "critical": 10,    # Característica determinante
        "relevant": 7,     # Característica relevante
        "supporting": 3    # Característica complementar
    },
    "impact": {
        "critical": 9,     # Impacto determinante
        "strong": 7,       # Impacto forte
        "moderate": 4,     # Impacto moderado
        "mild": 2          # Impacto leve
    },
    "relationship": {
        "hierarchical": 5, # Relação hierárquica
        "peer": 3,         # Relação entre pares
        "ex_partner": 5,   # Ex-parceiros
        "unknown": 1       # Desconhecido
    }
}

# Limiares de pontuação para classificação
# Define quantos pontos são necessários para confirmar cada tipo de violência
CLASSIFICATION_THRESHOLDS = {
    "microagressoes": {
        "interrupcoes_constantes": 15,
        "questionar_julgamento": 14,
        "comentarios_saude_mental": 10,
        "estereotipos": 12
    },
    "perseguicao": 20,
    "discriminacao_genero": {
        "discriminacao_flagrante": 20,
        "discriminacao_sutil": 17
    },
    "abuso_psicologico": 16,
    "assedio_moral_genero": 30,
    "violencia_sexual": {
        "assedio_sexual": 10,
        "importunacao_sexual": 10,
        "estupro": 10
    }
}

# Pontuações máximas teóricas para cada tipo
# Usado para calcular o nível de confiança na classificação
MAX_POSSIBLE_SCORES = {
    "microagressoes": {
        "interrupcoes_constantes": 34,  # Comportamento(10) + Frequência(8) + Características(7) + Contexto(5) + Impacto(4)
        "questionar_julgamento": 28,    # Comportamento(10) + Frequência(9) + Contexto(5) + Impacto(4)
        "comentarios_saude_mental": 20, # Comportamento(10) + Impacto(7) + Frequência(3)
        "estereotipos": 25              # Comportamento(10) + Características(8) + Contexto(4) + Impacto(3)
    },
    "perseguicao": 35,                  # Comportamento(10) + Frequência(10) + Impacto(8) + Contexto(2) + Agravante(5)
    "discriminacao_genero": {
        "discriminacao_flagrante": 28,  # Comportamento(10) + Características(10) + Frequência(3) + Impacto(5)
        "discriminacao_sutil": 31       # Características(10) + Comportamento(7) + Frequência(8) + Impacto(6)
    },
    "abuso_psicologico": 35,            # Comportamento(10) + Impacto(9) + Frequência(7) + Relação(5) + Agravante(4)
    "assedio_moral_genero": 45,         # Comportamento(10) + Contexto(10) + Características(10) + Frequência(8) + Relação(7)
    "violencia_sexual": {
        "assedio_sexual": 20,           # Comportamento(10) + Impacto(8) + Frequência(2)
        "importunacao_sexual": 20,      # Comportamento(10) + Impacto(7) + Agravante(3)
        "estupro": 15                   # Comportamento(10) + Agravante(5)
    }
}

# Fatores agravantes e atenuantes
AGGRAVATING_FACTORS = {
    "power_relation": 3,                # Relação hierárquica de poder
    "recurrence": 3,                    # Padrão sistemático e continuado
    "multiple_impacts": 4,              # Afeta diversos aspectos da vida
    "public_exposure": 2,               # Exposição pública
    "known_vulnerability": 5            # Direcionado a vulnerabilidade conhecida
}

MITIGATING_FACTORS = {
    "immediate_recognition": -3,        # Reconhecimento imediato pelo agressor
    "isolated_episode": -2,             # Episódio isolado sem padrão
    "corrective_measures": -2           # Medidas corretivas já tomadas
}

# Gravidade de cada tipo para resolução de ambiguidades
# Quanto maior o valor, mais grave é considerado o tipo de violência
SEVERITY_RANKING = {
    "violencia_sexual": {
        "estupro": 10,
        "importunacao_sexual": 8,
        "assedio_sexual": 7,
        "outras_condutas_conotacao_sexual": 5
    },
    "perseguicao": 7,
    "abuso_psicologico": 6,
    "assedio_moral_genero": 6,
    "discriminacao_genero": {
        "discriminacao_flagrante": 5,
        "discriminacao_sutil": 4
    },
    "microagressoes": {
        "interrupcoes_constantes": 2,
        "questionar_julgamento": 2,
        "comentarios_saude_mental": 3,
        "estereotipos": 2
    }
}

def get_threshold(violence_type, subtype=None):
    """
    Obtém o limiar de pontuação para um tipo/subtipo de violência.
    
    Args:
        violence_type (str): Tipo principal de violência
        subtype (str, optional): Subtipo específico (se aplicável)
        
    Returns:
        int: Limiar de pontuação para classificação
    """
    if subtype and (violence_type in CLASSIFICATION_THRESHOLDS) and isinstance(CLASSIFICATION_THRESHOLDS[violence_type], dict):
        return CLASSIFICATION_THRESHOLDS[violence_type].get(subtype, 0)
    elif violence_type in CLASSIFICATION_THRESHOLDS:
        if isinstance(CLASSIFICATION_THRESHOLDS[violence_type], dict):
            # Se for um dicionário de subtipos mas nenhum subtipo foi especificado,
            # usa o menor limiar entre os subtipos.
            return min(CLASSIFICATION_THRESHOLDS[violence_type].values())
        else:
            return CLASSIFICATION_THRESHOLDS[violence_type]
    return 0

def get_max_score(violence_type, subtype=None):
    """
    Obtém a pontuação máxima teórica para um tipo/subtipo de violência.
    
    Args:
        violence_type (str): Tipo principal de violência
        subtype (str, optional): Subtipo específico (se aplicável)
        
    Returns:
        int: Pontuação máxima possível
    """
    if subtype and (violence_type in MAX_POSSIBLE_SCORES) and isinstance(MAX_POSSIBLE_SCORES[violence_type], dict):
        return MAX_POSSIBLE_SCORES[violence_type].get(subtype, 0)
    elif violence_type in MAX_POSSIBLE_SCORES:
        if isinstance(MAX_POSSIBLE_SCORES[violence_type], dict):
            # Se for um dicionário de subtipos mas nenhum subtipo foi especificado,
            # usa o maior valor entre os subtipos
            return max(MAX_POSSIBLE_SCORES[violence_type].values())
        else:
            return MAX_POSSIBLE_SCORES[violence_type]
    return 0

def resolve_ambiguity(classifications):
    """
    Resolve ambiguidades quando múltiplos tipos de violência são identificados.
    
    Esta função implementa os critérios de especificidade e gravidade para decidir
    qual classificação deve ter precedência quando há sobreposição.
    
    Args:
        classifications (list): Lista de dicionários com classificações identificadas
                               [{'type': 'tipo', 'subtype': 'subtipo', 'score': pontuação, ...}]
    
    Returns:
        dict: A classificação com maior prioridade
    """
    if not classifications:
        return None
    
    if len(classifications) == 1:
        return classifications[0]
    
    # Ordena as classificações por:
    # 1. Pontuação (decrescente)
    # 2. Se empatar, por gravidade (decrescente)
    def get_severity(classification):
        vtype = classification['violence_type']
        subtype = classification.get('subtype')
        
        if vtype in SEVERITY_RANKING:
            if isinstance(SEVERITY_RANKING[vtype], dict) and subtype:
                return SEVERITY_RANKING[vtype].get(subtype, 0)
            elif isinstance(SEVERITY_RANKING[vtype], (int, float)):
                return SEVERITY_RANKING[vtype]
        return 0
    
    # Primeiro critério: pontuação
    sorted_by_score = sorted(classifications, key=lambda x: x['score'], reverse=True)
    
    # Se há diferença significativa de pontuação (>20% entre o primeiro e segundo)
    if len(sorted_by_score) > 1 and sorted_by_score[0]['score'] > 0 and \
       (sorted_by_score[0]['score'] - sorted_by_score[1]['score']) / sorted_by_score[0]['score'] > 0.2:
        return sorted_by_score[0]
    
    # Se a pontuação é próxima, verificamos a gravidade
    sorted_by_severity = sorted(sorted_by_score, key=get_severity, reverse=True)
    
    # Retorna o de maior gravidade
    return sorted_by_severity[0]

def should_report_multiple(classifications, ambiguity_threshold=0.1):
    """
    Determina se múltiplas classificações devem ser relatadas ao usuário.
    
    Args:
        classifications (list): Lista de dicionários com classificações identificadas
        ambiguity_threshold (float): Diferença percentual mínima entre pontuações para
                                    considerar como classificações distintas
    
    Returns:
        tuple: (bool, float) - Indicador se deve relatar múltiplas classificações e
                              nível de ambiguidade (0.0-1.0)
    """
    if len(classifications) <= 1:
        return False, 0.0
    
    # Ordenar por pontuação
    sorted_by_score = sorted(classifications, key=lambda x: x['score'], reverse=True)
    
    # Verificar a diferença relativa entre as duas maiores pontuações
    top_score = sorted_by_score[0]['score']
    second_score = sorted_by_score[1]['score']
    
    if top_score > 0:
        relative_diff = (top_score - second_score) / top_score
        ambiguity_level = 1.0 - min(relative_diff, 1.0)  # 1.0 = totalmente ambíguo
        
        # Se a diferença é pequena, relatar múltiplas classificações
        if relative_diff < ambiguity_threshold:
            return True, ambiguity_level
    
    return False, 0.0

def get_confidence_level_label(confidence):
    """
    Converte um valor numérico de confiança em uma descrição textual.
    
    Args:
        confidence (float): Nível de confiança entre 0.0 e 1.0
        
    Returns:
        str: Descrição textual do nível de confiança
    """
    for level, data in CONFIDENCE_LEVELS.items():
        if data['min'] <= confidence <= data['max']:
            return data['label']
    return "Indeterminado"

def get_confidence_description(confidence):
    """
    Retorna uma descrição mais detalhada sobre o que significa um determinado
    nível de confiança.
    
    Args:
        confidence (float): Nível de confiança entre 0.0 e 1.0
        
    Returns:
        str: Descrição explicativa do significado deste nível de confiança
    """
    for level, data in CONFIDENCE_LEVELS.items():
        if data['min'] <= confidence <= data['max']:
            return data['description']
    return "Nível de confiança indeterminado"

# Mapeamento de opções do formulário para critérios de classificação
FORM_OPTION_MAPPING = {
    "action_type": {
        "Interrupções durante fala ou participação": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "Questionamento constante de suas decisões/capacidades": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["behavior"]["critical"]},
            "discriminacao_genero": {"discriminacao_sutil": CRITERION_WEIGHTS["behavior"]["relevant"]}
        },
        "Comentários sobre seu estado emocional ou saúde mental": {
            "microagressoes": {"comentarios_saude_mental": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "Piadas ou comentários sobre estereótipos": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "Perseguição ou vigilância constante": {
            "perseguicao": CRITERION_WEIGHTS["behavior"]["critical"]
        },
        "Exclusão ou restrição de participação": {
            "discriminacao_genero": {
                "discriminacao_flagrante": CRITERION_WEIGHTS["behavior"]["critical"],
                "discriminacao_sutil": CRITERION_WEIGHTS["behavior"]["relevant"]
            }
        },
        "Ameaças, constrangimentos ou humilhações": {
            "abuso_psicologico": CRITERION_WEIGHTS["behavior"]["critical"]
        },
        "Pressão para realizar tarefas desnecessárias/exorbitantes": {
            "assedio_moral_genero": CRITERION_WEIGHTS["behavior"]["critical"]
        },
        "Comportamentos de natureza sexual não consentidos": {
            "violencia_sexual": {"assedio_sexual": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "Contato físico não consentido": {
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "Ato obsceno ou de caráter sexual": {
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["behavior"]["critical"]}
        },
        "Coerção ou violência para atos sexuais": {
            "violencia_sexual": {"estupro": CRITERION_WEIGHTS["behavior"]["critical"]}
        }
    },
    "frequency": {
        "Uma única vez": {
            "violencia_sexual": {"estupro": CRITERION_WEIGHTS["frequency"]["single"], 
                                "importunacao_sexual": CRITERION_WEIGHTS["frequency"]["single"],
                                "assedio_sexual": CRITERION_WEIGHTS["frequency"]["single"]},
            "discriminacao_genero": {"discriminacao_flagrante": CRITERION_WEIGHTS["frequency"]["single"]}
        },
        "Algumas vezes": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["frequency"]["few"],
                              "estereotipos": CRITERION_WEIGHTS["frequency"]["few"],
                              "comentarios_saude_mental": CRITERION_WEIGHTS["frequency"]["few"]},
            "violencia_sexual": {"assedio_sexual": CRITERION_WEIGHTS["frequency"]["few"]}
        },
        "Repetidamente": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["frequency"]["repeated"],
                             "questionar_julgamento": CRITERION_WEIGHTS["frequency"]["repeated"],
                             "estereotipos": CRITERION_WEIGHTS["frequency"]["repeated"]},
            "perseguicao": CRITERION_WEIGHTS["frequency"]["repeated"],
            "discriminacao_genero": {"discriminacao_sutil": CRITERION_WEIGHTS["frequency"]["repeated"]},
            "abuso_psicologico": CRITERION_WEIGHTS["frequency"]["repeated"]
        },
        "Continuamente": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["frequency"]["continuous"],
                              "questionar_julgamento": CRITERION_WEIGHTS["frequency"]["continuous"]},
            "perseguicao": CRITERION_WEIGHTS["frequency"]["continuous"],
            "discriminacao_genero": {"discriminacao_sutil": CRITERION_WEIGHTS["frequency"]["continuous"]},
            "abuso_psicologico": CRITERION_WEIGHTS["frequency"]["continuous"],
            "assedio_moral_genero": CRITERION_WEIGHTS["frequency"]["continuous"]
        }
    },
    "context": {
        "Sala de aula": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["context"]["relevant"]}
        },
        "Ambiente administrativo": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["context"]["relevant"],
                              "questionar_julgamento": CRITERION_WEIGHTS["context"]["relevant"]}
        },
        "Local de trabalho/estágio": {
            "assedio_moral_genero": CRITERION_WEIGHTS["context"]["critical"],
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["context"]["relevant"]}
        },
        "Espaço público no campus": {
            "perseguicao": CRITERION_WEIGHTS["context"]["supporting"],
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["context"]["relevant"]},
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["context"]["supporting"]}
        },
        "Ambiente online": {
            "perseguicao": CRITERION_WEIGHTS["context"]["supporting"]
        },
        "Evento acadêmico": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["context"]["relevant"]},
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["context"]["supporting"]}
        },
        "Ambiente social relacionado à universidade": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["context"]["relevant"]},
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["context"]["supporting"]}
        }
    },
    "target": {
        "Gênero": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["target"]["relevant"]},
            "discriminacao_genero": {"discriminacao_flagrante": CRITERION_WEIGHTS["target"]["critical"],
                                    "discriminacao_sutil": CRITERION_WEIGHTS["target"]["critical"]},
            "assedio_moral_genero": CRITERION_WEIGHTS["target"]["critical"]
        },
        "Orientação sexual ou identidade de gênero": {
            "discriminacao_genero": {"discriminacao_flagrante": CRITERION_WEIGHTS["target"]["critical"],
                                   "discriminacao_sutil": CRITERION_WEIGHTS["target"]["critical"]}
        },
        "Raça ou etnia": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["target"]["relevant"],
                              "estereotipos": CRITERION_WEIGHTS["target"]["relevant"]}
        },
        "Condição financeira": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["target"]["supporting"]}
        },
        "Deficiência física ou mental": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["target"]["relevant"],
                              "estereotipos": CRITERION_WEIGHTS["target"]["relevant"]}
        },
        "Aparência física": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["target"]["supporting"]}
        },
        "Origem regional": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["target"]["supporting"]}
        },
        "Desempenho acadêmico": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["target"]["supporting"]}
        }
    },
    "relationship": {
        "Superior hierárquico": {
            "abuso_psicologico": CRITERION_WEIGHTS["relationship"]["hierarchical"],
            "assedio_moral_genero": CRITERION_WEIGHTS["relationship"]["hierarchical"]
        },
        "Colega de mesma hierarquia": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["relationship"]["peer"]}
        },
        "Subordinado": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["relationship"]["peer"]}
        },
        "Desconhecido": {
            "perseguicao": CRITERION_WEIGHTS["relationship"]["unknown"],
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["relationship"]["unknown"]}
        },
        "Pessoa com quem teve relacionamento anterior": {
            "perseguicao": CRITERION_WEIGHTS["relationship"]["ex_partner"]
        }
    },
    "impact": {
        "Constrangimento ou desconforto momentâneo": {
            "microagressoes": {"estereotipos": CRITERION_WEIGHTS["impact"]["mild"]},
            "violencia_sexual": {"assedio_sexual": CRITERION_WEIGHTS["impact"]["moderate"],
                                "importunacao_sexual": CRITERION_WEIGHTS["impact"]["moderate"]}
        },
        "Impacto na participação em atividades": {
            "microagressoes": {"interrupcoes_constantes": CRITERION_WEIGHTS["impact"]["moderate"]}
        },
        "Danos emocionais ou psicológicos": {
            "microagressoes": {"comentarios_saude_mental": CRITERION_WEIGHTS["impact"]["strong"]},
            "abuso_psicologico": CRITERION_WEIGHTS["impact"]["critical"],
            "assedio_moral_genero": CRITERION_WEIGHTS["impact"]["strong"],
            "violencia_sexual": {"estupro": CRITERION_WEIGHTS["impact"]["critical"]}
        },
        "Interferência em sua liberdade de ir e vir": {
            "perseguicao": CRITERION_WEIGHTS["impact"]["strong"]
        },
        "Prejuízos ao seu desempenho acadêmico/profissional": {
            "microagressoes": {"questionar_julgamento": CRITERION_WEIGHTS["impact"]["moderate"]},
            "discriminacao_genero": {"discriminacao_sutil": CRITERION_WEIGHTS["impact"]["strong"],
                                   "discriminacao_flagrante": CRITERION_WEIGHTS["impact"]["strong"]},
            "assedio_moral_genero": CRITERION_WEIGHTS["impact"]["strong"]
        },
        "Medo ou sentimento de insegurança": {
            "perseguicao": CRITERION_WEIGHTS["impact"]["strong"],
            "violencia_sexual": {"importunacao_sexual": CRITERION_WEIGHTS["impact"]["strong"],
                               "estupro": CRITERION_WEIGHTS["impact"]["critical"]}
        },
        "Violação de intimidade ou privacidade": {
            "violencia_sexual": {"assedio_sexual": CRITERION_WEIGHTS["impact"]["strong"],
                               "importunacao_sexual": CRITERION_WEIGHTS["impact"]["strong"],
                               "estupro": CRITERION_WEIGHTS["impact"]["critical"]}
        }
    }
}