"""
Módulo de regras para identificação de tipos de violência.

Este módulo contém um sistema modular de regras organizadas por tipo de violência:

- base_engine.py: Classe base com métodos comuns e infraestrutura
- explanation_system.py: Sistema de geração de explicações
- microaggression_rules.py: Regras para microagressões
- sexual_violence_rules.py: Regras para violência sexual
- discrimination_rules.py: Regras para discriminação (gênero, racial, etc.)
- harassment_rules.py: Regras para assédio/perseguição
- digital_violence_rules.py: Regras para violência digital
- violence_rules.py: Classe principal que combina todos os módulos

A classe principal ViolenceRules é exportada para ser usada pelo sistema.
"""

from .violence_rules import ViolenceRules
from .explanation_system import ExplanationSystem

__all__ = ['ViolenceRules', 'ExplanationSystem']
