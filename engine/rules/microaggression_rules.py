from experta.rule import Rule
from experta import OR
from .base_engine import BaseViolenceEngine
from ..facts import (
    ViolenceBehavior, KeywordFact, FrequencyFact, TargetFact, ProcessingPhase
)


class MicroaggressionRulesMixin:
    """
    Mixin contendo regras específicas para identificação de microagressões.
    """

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="interrupcao"),
            KeywordFact(category="action_type", keyword="interrupcao")
        ),
        OR(
            FrequencyFact(value="repetidamente"),
            FrequencyFact(value="continuamente"),
            KeywordFact(category="frequency", keyword="repetidamente"),
            KeywordFact(category="frequency", keyword="continuamente")
        )
    )
    def detect_interrupcoes_constantes(self):
        """Detecta interrupções constantes como microagressão."""
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "interrupcao":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        # Verificar frequências identificadas
        frequencies = []
        for fact_id in self.get_matching_facts(FrequencyFact):
            freq = self.facts[fact_id]["value"]
            if freq in ["repetidamente", "continuamente"]:
                frequencies.append(freq)
        
        if frequencies:
            facts_used["frequency"] = frequencies
            
        reasoning = "A interrupção sistemática e repetida de falas é uma forma sutil mas danosa de microagressão, que pode silenciar vozes e diminuir a participação de determinados grupos em ambientes acadêmicos ou profissionais."
        
        self.create_classification(
            "microagressoes", 
            "interrupcoes_constantes", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="questionamento_capacidade"),
            KeywordFact(category="action_type", keyword="questionamento_capacidade")
        ),
        OR(
            TargetFact(characteristic="genero"),
            KeywordFact(category="target", keyword="genero")
        )
    )
    def detect_questionar_julgamento(self):
        """Detecta questionamento de capacidade baseado em gênero."""
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "questionamento_capacidade":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        # Verificar características do alvo
        targets = []
        for fact_id in self.get_matching_facts(TargetFact):
            target = self.facts[fact_id]["characteristic"]
            if target == "genero":
                targets.append(target)
        
        if targets:
            facts_used["target"] = targets
            
        reasoning = "O questionamento recorrente da capacidade baseado em gênero é uma forma de discriminação que afeta a confiança da vítima e reforça estereótipos prejudiciais no ambiente acadêmico ou profissional."
        
        self.create_classification(
            "microagressoes", 
            "questionar_julgamento", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="comentarios_saude_mental"),
            KeywordFact(category="action_type", keyword="comentarios_saude_mental")
        )
    )
    def detect_comentarios_saude_mental(self):
        """Detecta comentários relacionados à saúde mental como microagressão."""
        self.create_classification("microagressoes", "comentarios_saude_mental", [
            "Identificados comentários relacionados à saúde mental"
        ])

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="piadas_estereotipos"),
            KeywordFact(category="action_type", keyword="piadas_estereotipos")
        )
    )
    def detect_estereotipos(self):
        """Detecta piadas ou comentários baseados em estereótipos."""
        self.create_classification("microagressoes", "estereotipos", [
            "Identificadas piadas ou comentários baseados em estereótipos"
        ])
