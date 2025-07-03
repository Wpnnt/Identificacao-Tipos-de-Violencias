"""
Arquivo de compatibilidade para violence_types.py refatorado.
Este arquivo mantém a compatibilidade com o código existente enquanto
utiliza a nova estrutura modular.
"""

# Importa a nova estrutura refatorada
from .violence_manager import (
    VIOLENCE_TYPES,
    CRITERION_WEIGHTS, 
    SEVERITY_LEVEL,
    SEVERITY_RANKING,
    REPORT_CONTACT,
    get_severity
)

