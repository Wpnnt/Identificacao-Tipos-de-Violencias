"""
Sistema de pesos e critérios para avaliação de violências.
"""
from typing import Dict, Any


class CriterionWeights:
    """Classe para gerenciar pesos dos critérios de avaliação."""
    
    BEHAVIOR = {
        "critical": 10,    # Comportamento crítico/determinante
        "relevant": 7,     # Comportamento relevante
        "supporting": 4    # Comportamento suportivo
    }
    
    FREQUENCY = {
        "single": 2,       # Uma única vez
        "few": 4,          # Algumas vezes
        "repeated": 6,     # Repetidamente
        "continuous": 8    # Continuamente
    }
    
    CONTEXT = {
        "critical": 10,    # Contexto determinante
        "relevant": 5,     # Contexto relevante
        "supporting": 2    # Contexto menos relevante
    }
    
    TARGET = {
        "critical": 10,    # Característica determinante
        "relevant": 7,     # Característica relevante
        "supporting": 3    # Característica complementar
    }
    
    IMPACT = {
        "critical": 9,     # Impacto determinante
        "strong": 7,       # Impacto forte
        "moderate": 4,     # Impacto moderado
        "mild": 2          # Impacto leve
    }
    
    RELATIONSHIP = {
        "hierarchical": 5, # Relação hierárquica
        "peer": 3,         # Relação entre pares
        "ex_partner": 5,   # Ex-parceiros
        "unknown": 1       # Desconhecido
    }

    @classmethod
    def get_weight(cls, category: str, level: str) -> int:
        """Retorna o peso para uma categoria e nível específicos."""
        category_weights = getattr(cls, category.upper(), {})
        return category_weights.get(level, 0)

    @classmethod
    def get_all_weights(cls) -> Dict[str, Dict[str, int]]:
        """Retorna todos os pesos organizados por categoria."""
        return {
            "behavior": cls.BEHAVIOR,
            "frequency": cls.FREQUENCY,
            "context": cls.CONTEXT,
            "target": cls.TARGET,
            "impact": cls.IMPACT,
            "relationship": cls.RELATIONSHIP
        }
