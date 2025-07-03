from experta.rule import Rule
from experta import OR
from .base_engine import BaseViolenceEngine
from ..facts import (
    ViolenceBehavior, KeywordFact, ContextFact, RelationshipFact, 
    ImpactFact, ProcessingPhase
)


class SexualViolenceRulesMixin:
    """
    Mixin contendo regras específicas para identificação de violência sexual.
    """

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="natureza_sexual_nao_consentido"),
            KeywordFact(category="action_type", keyword="natureza_sexual_nao_consentido")
        )
    )
    def detect_assedio_sexual(self):
        """Detecta assédio sexual."""
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "natureza_sexual_nao_consentido":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        reasoning = "O assédio sexual viola a dignidade e liberdade sexual da vítima, criando um ambiente hostil e constrangedor, podendo configurar crime conforme a Lei nº 10.224/2001."
        
        self.create_classification(
            "violencia_sexual", 
            "assedio_sexual", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="contato_fisico_nao_consentido"),
            ViolenceBehavior(behavior_type="ato_obsceno"),
            KeywordFact(category="action_type", keyword="contato_fisico_nao_consentido"),
            KeywordFact(category="action_type", keyword="ato_obsceno")
        )
    )
    def detect_importunacao_sexual(self):
        """Detecta importunação sexual."""
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior in ["contato_fisico_nao_consentido", "ato_obsceno"]:
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
        
        # Verificar contexto, se presente
        contexts = []
        for fact_id in self.get_matching_facts(ContextFact):
            contexts.append(self.facts[fact_id]["location"])
        
        if contexts:
            facts_used["context"] = contexts
        
        # Verificar relacionamento, se presente
        relationships = []
        for fact_id in self.get_matching_facts(RelationshipFact):
            relationships.append(self.facts[fact_id]["type"])
        
        if relationships:
            facts_used["relationship"] = relationships
        
        reasoning = "A importunação sexual constitui crime previsto no artigo 215-A do Código Penal, incluindo toques corporais não consentidos e atos libidinosos em ambiente público, com pena de reclusão de 1 a 5 anos."
        
        self.create_classification(
            "violencia_sexual", 
            "importunacao_sexual", 
            facts_used=facts_used,
            reasoning=reasoning
        )

    @Rule(
        ProcessingPhase(phase="analysis"),
        OR(
            ViolenceBehavior(behavior_type="coercao_sexual"),
            KeywordFact(category="action_type", keyword="coercao_sexual")
        ),
        OR(
            ImpactFact(type="medo_inseguranca"),
            KeywordFact(category="impact", keyword="medo_inseguranca")
        )
    )
    def detect_estupro(self):
        """Detecta situações que podem configurar estupro."""
        facts_used = {}
        
        # Verificar comportamentos identificados
        behaviors = []
        for fact_id in self.get_matching_facts(ViolenceBehavior):
            behavior = self.facts[fact_id]["behavior_type"]
            if behavior == "coercao_sexual":
                behaviors.append(behavior)
        
        if behaviors:
            facts_used["behavior"] = behaviors
            
        # Verificar impactos identificados
        impacts = []
        for fact_id in self.get_matching_facts(ImpactFact):
            impact = self.facts[fact_id]["type"]
            if impact == "medo_inseguranca":
                impacts.append(impact)
        
        if impacts:
            facts_used["impact"] = impacts
            
        reasoning = "A coerção sexual que gera medo e insegurança pode configurar estupro (art. 213 do Código Penal), crime hediondo que requer denúncia imediata às autoridades e atendimento especializado à vítima."
        
        self.create_classification(
            "violencia_sexual", 
            "estupro", 
            facts_used=facts_used,
            reasoning=reasoning
        )
