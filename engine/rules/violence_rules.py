from .base_engine import BaseViolenceEngine
from .microaggression_rules import MicroaggressionRulesMixin
from .sexual_violence_rules import SexualViolenceRulesMixin
from .discrimination_rules import DiscriminationRulesMixin
from .harassment_rules import HarassmentRulesMixin
from .digital_violence_rules import DigitalViolenceRulesMixin


class ViolenceRules(
    BaseViolenceEngine,
    MicroaggressionRulesMixin,
    SexualViolenceRulesMixin,
    DiscriminationRulesMixin,
    HarassmentRulesMixin,
    DigitalViolenceRulesMixin
):
    """
    Motor de regras completo para identificação de tipos de violência.
    
    Esta classe combina todas as especializações de regras em um único motor,
    herdando de:
    - BaseViolenceEngine: Infraestrutura básica e métodos comuns
    - MicroaggressionRulesMixin: Regras para microagressões
    - SexualViolenceRulesMixin: Regras para violência sexual
    - DiscriminationRulesMixin: Regras para discriminação (gênero, racial, etc.)
    - HarassmentRulesMixin: Regras para assédio/perseguição
    - DigitalViolenceRulesMixin: Regras para violência digital
    """
    
    def __init__(self):
        """
        Inicializa o motor de regras completo.
        """
        super().__init__()
        print("🔧 Motor de regras ViolenceRules inicializado com todos os módulos")
    
    def get_loaded_modules(self):
        """
        Retorna informações sobre os módulos carregados.
        """
        modules = [
            "BaseViolenceEngine - Infraestrutura básica",
            "MicroaggressionRulesMixin - Regras de microagressões",
            "SexualViolenceRulesMixin - Regras de violência sexual",
            "DiscriminationRulesMixin - Regras de discriminação",
            "HarassmentRulesMixin - Regras de assédio/perseguição",
            "DigitalViolenceRulesMixin - Regras de violência digital"
        ]
        return modules
