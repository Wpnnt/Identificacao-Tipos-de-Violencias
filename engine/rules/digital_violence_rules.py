from experta.rule import Rule
from experta import OR
from .base_engine import BaseViolenceEngine
from ..facts import (
    ViolenceBehavior, KeywordFact, ProcessingPhase
)


class DigitalViolenceRulesMixin:
    """
    Mixin contendo regras específicas para identificação de violência digital.
    """

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="cyberbullying"),
            KeywordFact(category="action_type", keyword="cyberbullying")
        )
    )
    def detect_cyberbullying(self):
        """Detecta cyberbullying."""
        self.create_classification("violencia_digital", "cyberbullying", [
            "Identificado comportamento de cyberbullying"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="exposicao_conteudo"),
            KeywordFact(category="action_type", keyword="exposicao_conteudo")
        )
    )
    def detect_exposicao_nao_consentida(self):
        """Detecta exposição não consentida de conteúdo."""
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "exposicao_conteudo":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        reasoning = "A exposição não consentida de conteúdo íntimo configura crime conforme a Lei nº 13.718/2018, com pena de reclusão de 1 a 5 anos, requerendo registro de Boletim de Ocorrência em Delegacia Especializada de Crimes Digitais."
        
        self.create_classification(
            "violencia_digital", 
            "exposicao_nao_consentida", 
            facts_used=facts_used,
            reasoning=reasoning
        )
